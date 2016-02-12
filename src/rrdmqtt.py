from argparse import ArgumentParser
import json
import logging
import os
import subprocess
from time import sleep
import yaml

from utils.mqttman import MQTTManager
from utils.rrdman import RRDManager

class RrdMqtt():
    def __init__(self):
        self.setup_args()
        self.setup_logging()
        self.load_config()

        self.mqtt = MQTTManager(self.cfg['mqtt']['broker'])

        self.rrd = RRDManager(
            datadir=self.cfg['rrdmqtt']['datadir'],
            graphdir=self.cfg['rrdmqtt']['graphdir'])

        for name, signal in self.signals.items():
            # Check if the rrd file exists and create if necessary
            self.rrd.check_rrd(name)

            # subscribe topics
            self.mqtt.add_topic(signal['topic'])
            self.mqtt.set_timeout(signal['topic'], signal['timeout'])


        
    def setup_args(self):
        parser = ArgumentParser()

        parser.add_argument(
            '-c', '--cfg',
            help='Path to the configuration file.',
            default='rrdmqtt.yaml')

        parser.add_argument(
            '-v', '--verbose',
            help='Enable verbose logging output.',
            action='store_true');

        self.args = parser.parse_args()
    

    def setup_logging(self):
        '''Set up the logging framework.'''

        if self.args.verbose:
            level = logging.DEBUG
        else:
            level = logging.WARNING
        
        logging.basicConfig(
            level=level,
            format='%(asctime)s %(levelname)s: %(message)s')

        
    def load_config(self):
        cfgfile = self.args.cfg

        try:
            with open(cfgfile, 'r') as f:
                self.cfg = yaml.load(f)

            # for convenient access...
            self.signals = self.cfg['rrdmqtt']['signals']
            self.graphs = self.cfg['rrdmqtt']['graphs']
        except:
            msg = "Failed to load config file '{0}'."
            logging.exception(msg.format(cfgfile))

        
    def update_signal(self, signal):
        sigcfg = self.signals[signal]
        
        try:
            status = self.mqtt.get_status(sigcfg['topic'])
            payload = self.mqtt.get_payload(sigcfg['topic'])

            if payload != None:
                data = json.loads(payload)

                self.rrd.update_rrd(signal, data['value'])
            
            else:
                logging.warning('No data received.')
            
        except:
            msg = "Failed to update rrdfile '{0}'."
            logging.exception(msg.format(filepath))

            
    def create_graphs(self):
        for name,graph in self.graphs.items():

            # take the default settings and update them with the
            # actual config of the graph
            graphcfg = self.cfg['rrdmqtt']['graphconfig'].copy()
            graphcfg.update(graph)

            self.rrd.create_graphs(
                name,
                graph=graphcfg,
                signalopts=self.signals)
            
            
    def run(self):
        graph_int = self.cfg['rrdmqtt']['graphconfig']['interval']
        cnt = graph_int
        
        while True:
            self.mqtt.tick()
            
            for signal in self.signals.keys():
                self.update_signal(signal)

            if cnt > 0:
                cnt -= 1
            else:
                self.create_graphs()
                cnt = graph_int
                
            sleep(1)
        
            
if __name__ == '__main__':
    rrdmqtt = RrdMqtt()

    rrdmqtt.run()


    
