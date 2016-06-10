'''Script to publish sensor values (events) to a MQTT broker.'''


import logging
import paho.mqtt.publish as mqtt_pub
import time
import os

from utils.cmdlapp import CmdlApp
from utils.sched import Scheduler, Task
from utils.clsinst import get_instance_by_name


class MqttPublisher():
    def __init__(self, cfg):
        self.cfg = cfg

    def get_mqtt_path(self, evt):
        data = {
            'prefix': self.cfg['mqtt']['topic_prefix'],
            'node': self.cfg['mqtt']['node_name'],
            'sensor': evt.getSensorName(),
            'quantity': evt.getQuantity(),
            }

        path_tmpl = '{prefix}/{node}/{sensor}/{quantity}'
    
        return path_tmpl.format(**data)


    def publish_events(self, evts):
        for evt in evts:
            # The publish might fail, e.g. due to network problems. Just log 
            # the exception and try again next time.
            try:
                topic = self.get_mqtt_path(evt)

                msg = "Publishing to topic '{0}'."
                logging.debug(msg.format(topic))

                mqtt_pub.single(
                    topic=topic,
                    payload=evt.toJSON(),
                    hostname=self.cfg['mqtt']['broker'])
            except:
                logging.exception('Publish of MQTT value failed.')


class SensorTask(Task):
    '''Task that samples a sensor and publishes the sensor events. 

    The task can be scheduled in regular intervals with the Scheduler
    class.'''

    def __init__(self, scfg, publisher):
        Task.__init__(
            self, 
            interval=scfg['interval'], 
            name='task_' + scfg['sensor_name'])
        
        self.scfg = scfg
        self.publisher = publisher

        # Create an instance of the sensor class
        args = [scfg]
        self.sensor = get_instance_by_name(
            scfg['sensor_class'],
            *args)


    def run(self):
        msg = "Reading sensor '{0}'."
        logging.debug(msg.format(self.sensor.getName()))

        try:
            sevts = self.sensor.sample()
            
            self.publisher.publish_events(sevts)
        except:
            msg = "Failed to sample sensor values of sensor '{0}'."
            logging.exception(msg.format(sensor.getName()))
        

class MqttPublish(CmdlApp):
    def __init__(self):
        # we are a cmd-line tool with config file
        CmdlApp.__init__(self)
        self.cmdlapp_config(has_cfgfile=True)


    def create_sensor_tasks(self, scheduler, publisher):
        '''Create sensor classes according to the configuration.'''

        for sname, scfg in self.cfg['sensors'].items():
            # add sensor name to config structure
            scfg['sensor_name'] = sname

            # Take the sensor interval, default interval or 5s
            scfg['interval'] = scfg.get(
                'interval', 
                self.cfg['mqtt'].get('interval', 5))

            s_task = SensorTask(scfg, publisher)

            scheduler.add_task(s_task)

    
    def main_fct(self):
        '''Set up the sensors and publish cyclic updates of the sensor
        values to the MQTT broker.'''

        publisher = MqttPublisher(self.cfg)

        sched = Scheduler()

        self.create_sensor_tasks(sched, publisher)
        
        sched.run()


if __name__ == '__main__':
    MqttPublish().run()

