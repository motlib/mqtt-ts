'''Script to publish sensor values (events) to a MQTT broker.'''

import logging
import time
import os

import paho.mqtt.publish as publish
from sensorconfig import config, get_sensors

from utils.cmdlapp import CmdlApp

class MqttPublish(CmdlApp):
    def get_mqtt_path(self, evt):
        data = {
            'prefix': config['mqtt_topic_prefix'],
            'node': config['node_name'],
            'sensor': evt.getSensorName(),
            'quantity': evt.getQuantity(),
            }

        path_tmpl = '{prefix}/{node}/{sensor}/{quantity}'
    
        return path_tmpl.format(**data)

    def sample_sensors(self):
        all_evts = []

        for sensor in self.sensors:
            msg = "Reading sensor '{0}'."
            logging.debug(msg.format(sensor.getName()))

            try:
                sevts = sensor.sampleValues()

                all_evts.extend(sevts)
            except:
                msg = "Failed to sample sensor values of sensor '{0}'."
                logging.exception(msg.format(sensor.getName()))
        
        return all_evts


    def publish_events(self, evts):
        logging.debug('Publishing data.')

        for evt in evts:
            # The publish might fail, e.g. due to network problems. Just log 
            # the exception and try again next time.
            try:
                publish.single(
                    topic=self.get_mqtt_path(evt),
                    payload=evt.toJSON(),
                    hostname=config['mqtt_broker'])
            except:
                logging.exception('Publish of MQTT value failed.')
        
    
    def main_fct(self):
        '''Set up the sensors and publish cyclic updates of the sensor
        values to the MQTT broker.'''

        logging.info('Setting up sensors')
        self.sensors = get_sensors()
        logging.debug('Sensors initialized.')


        while True:
            evts = self.sample_sensors()
            self.publish_events(evts)

            #time.sleep(config['sample_interval'])
            time.sleep(5)


if __name__ == '__main__':
    MqttPublish().run()

