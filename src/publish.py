#!/usr/bin/env python3

'''Script to publish sensor values (events) to a MQTT broker.'''


import logging
import socket

from pub.evtpub import MqttPublisher
from pub.task import SensorTask
from utils.clsinst import get_instance_by_name
from utils.cmdlapp import CmdlApp
from utils.sched import Scheduler


class MqttPublish(CmdlApp):
    def __init__(self):
        # we are a cmd-line tool with config file
        CmdlApp.__init__(self)

        self.cmdlapp_config(
            has_cfgfile=True,
            reload_on_hup=True)


    def create_sensor(self, scfg):
        # Create an instance of the sensor class
        args = [scfg]
        sensor = get_instance_by_name(
            scfg['sensor_class'],
            *args)

        msg = ("Created sensor instance '{sensor_name}' from class " 
            "'{sensor_class}'. ")
        logging.info(msg.format(
                sensor_name=scfg['sensor_name'],
                sensor_class=scfg['sensor_class']))

        return sensor


    def create_sensor_task(self, scfg):
        '''Create a sensor and a sensor task and schedule it for
        execution.'''

        sensor = self.create_sensor(scfg)
        
        if 'interval' in scfg:
            itype = 'configured'
            ival = scfg['interval']
        else:
            itype = 'default'
            ival = sensor.get_default_interval()

        s_task = SensorTask(
            sensor=sensor, 
            publisher=self.publisher, 
            interval=ival)

        self.sched.add_task(s_task)
            
        msg = "Scheduled '{sensor_name}' with {itype} sampling interval {ival}s." 
        logging.info(msg.format(
                sensor_name=sensor.getName(),
                itype=itype,
                ival=ival))
        

    def create_sensor_tasks(self):
        '''Create sensor tasks according to the configuration.'''

        hostname = socket.gethostname()

        for sname, scfg in self.cfg['sensors'].items():
            scfg['sensor_name'] = sname

            # Check if the sensor shall be created on this host and
            # create if necessary.

            # TODO: Currently dangerous, because it's case-sensitive
            # and ignores domain name.
            if hostname in scfg['nodes'] or 'localhost' in scfg['nodes']:

                self.create_sensor_task(scfg)

    
    def main_fct(self):
        '''Set up the sensors and publish cyclic updates of the sensor
        values to the MQTT broker.'''

        while True:
            mqttcfg = self.cfg['mqtt']

            self.publisher = MqttPublisher(
                broker=mqttcfg['broker'],
                topic_prefix=mqttcfg['topic_prefix'])

            self.sched = Scheduler()

            self.create_sensor_tasks()
        
            self.sched.run()


    def on_reload(self):
        msg = 'Stopping scheduler due to SIGHUP signal.'
        logging.info(msg)

        self.sched.stop()

        CmdlApp.on_reload(self)


if __name__ == '__main__':
    MqttPublish().run()

