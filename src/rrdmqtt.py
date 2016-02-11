from argparse import ArgumentParser
import json
import logging
import os
import subprocess
from time import sleep, mktime
import datetime

from mqttman import MQTTManager

MQTT_BROKER='bpi1'
#MQTT_BROKER = '192.168.0.21'

class RrdMqtt():
    def __init__(self):
        self.setup_args()
        self.setup_logging()

        self.mqtt = MQTTManager(MQTT_BROKER)

        self.topics = {
            '/sensors/rpi2/BMP180/pressure': 'pressure',
            '/sensors/rpi2/outside/temperature': 'temp_out',
            '/sensors/rpi2/HTU21D/relative humidity': 'hum_rel',
            '/sensors/rpi2/BMP180/pressure': 'pressure',
        }

        for topic in self.topics.keys():
            self.mqtt.add_topic(topic)

        
    def setup_args(self):
        parser = ArgumentParser()

        parser.add_argument(
            '-d', '--datadir',
            help='Path to the rrd data files.')
        
        parser.add_argument(
            '-g', '--graphdir',
            help='Path to the generated graphics files.')

        self.args = parser.parse_args()
    

    def setup_logging(self):
        '''Set up the logging framework.'''
        
        logging.basicConfig(
            #filename=self.args.logfile,
            #filemode='a',
            level=logging.WARNING,
            format='%(asctime)s %(levelname)s: %(message)s')

        
    def create_rrd(self, topic):
        filepath = self.get_rrdfile(topic)
        
        cmd = [
            'rrdtool',
            'create',
            filepath,
            # one minute steps
            '--step', '60',  
            'DS:value:GAUGE:120:U:U',
            # average over 5 values (5 minutes), store 288 = 24h
            'RRA:AVERAGE:0.5:5:288',
            # average over 20 values (20 minutes), store 2160 = 30d
            'RRA:AVERAGE:0.5:20:2160'
        ]

        subprocess.check_call(cmd)
        
        
    def update_topic(self, topic):
        filepath = self.get_rrdfile(topic)

        if not os.path.isfile(filepath):
            self.create_rrd(topic)
        
        try:
            status = self.mqtt.get_status(topic)
            payload = self.mqtt.get_payload(topic)

            logging.debug(
                'Status: ' + str(status)
                + '; Payload: ' + str(payload))
            
            if payload != None:
                data = json.loads(payload)

                value = 'N:' + str(data['value'])
            
                cmd = [
                    'rrdtool',
                    'update',
                    filepath,
                    value
                ]
                subprocess.check_call(cmd)
            
                logging.info("Updated rrd '{0}'.".format(filepath))
            else:
                logging.warning('No data received.')
            
        except:
            msg = "Failed to update rrdfile '{0}'."
            logging.exception(msg.format(filepath))


    def get_rrdfile(self, topic):
        filename = self.topics[topic] + '.rrd'
        filepath = os.path.join(self.args.datadir, filename)

        return filepath


    def get_graphfile(self, topic, duration):
        filename = self.topics[topic] + '.png'
        filepath = os.path.join(self.args.graphdir, filename)

        return filepath
    
    
    def create_graph(self, topic):
        now = datetime.datetime.utcnow()
        delta = datetime.timedelta(hours=6)
        start = int(mktime((now - delta).timetuple()))

        graphname = self.get_graphfile(topic, '6h')
        rrdname = self.get_rrdfile(topic)
        
        cmd = [
            'rrdtool',
            'graph',
            graphname,
            '--start', str(start),
            '-w', '1024',
            '-h', '768',
            'DEF:value=' + rrdname + ':value:AVERAGE',
            'LINE2:value#FF0000'
        ]

        subprocess.check_call(cmd)

        msg = "Created graph '{0}'."
        logging.info(msg.format(graphname))
    
                                
    def run(self):

        cnt = 0
        while True:
            self.mqtt.tick()
            
            for topic in self.topics.keys():
                self.update_topic(topic)

            cnt += 1
            if cnt == 60:
                cnt = 0
                for topic in self.topics.keys():
                    self.create_graph(topic)
                
            sleep(1)
        
            
            
if __name__ == '__main__':
    rrdmqtt = RrdMqtt()

    rrdmqtt.run()


    
