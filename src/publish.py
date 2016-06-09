'''Script to publish sensor values (events) to a MQTT broker.'''


import logging
import paho.mqtt.publish as mqtt_pub
import time
import os

from utils.cmdlapp import CmdlApp

class MqttPublish(CmdlApp):
    def __init__(self):
        # we are a cmd-line tool with config file
        CmdlApp.__init__(self)
        self.cmdlapp_config(has_cfgfile=True)


    def get_sensor_class(self, name):
        '''Instanciate the sensor classes based on the config.'''

        name_parts = name.split('.')

        mod_name = '.'.join(name_parts[0:-1])

        item = __import__(mod_name)
        for name in name_parts[1:]:
            item = getattr(item, name)
        
        return item


    def create_sensors(self):
        '''Create sensor classes according to the configuration.'''

        sensors = []

        for sname, scfg in self.cfg['sensors'].items():
            # add sensor name to config structure
            scfg['sensor_name'] = sname

            msg = "Instanciate sensor class '{sensor_class}' for sensor " \
                "'{sensor_name}'."
            logging.info(msg.format(**scfg))

            scls = self.get_sensor_class(scfg['sensor_class'])
            sinst = scls(scfg)

            sensors.append(sinst)

        return sensors


    def get_mqtt_path(self, evt):
        data = {
            'prefix': self.cfg['mqtt']['topic_prefix'],
            'node': self.cfg['mqtt']['node_name'],
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
                mqtt_pub.single(
                    topic=self.get_mqtt_path(evt),
                    payload=evt.toJSON(),
                    hostname=self.cfg['mqtt']['broker'])
            except:
                logging.exception('Publish of MQTT value failed.')
        
    
    def main_fct(self):
        '''Set up the sensors and publish cyclic updates of the sensor
        values to the MQTT broker.'''

        self.sensors = self.create_sensors()

        while True:
            evts = self.sample_sensors()
            self.publish_events(evts)

            #TODO: better scheduling, best per sensor
            time.sleep(5)


if __name__ == '__main__':
    MqttPublish().run()

