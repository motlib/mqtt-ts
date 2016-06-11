'''Script to publish sensor values (events) to a MQTT broker.'''


import logging

from pub.evtpub import MqttPublisher
from pub.task import SensorTask
from utils.cmdlapp import CmdlApp
from utils.sched import Scheduler


class MqttPublish(CmdlApp):
    def __init__(self):
        # we are a cmd-line tool with config file
        CmdlApp.__init__(self)

        self.cmdlapp_config(
            has_cfgfile=True,
            reload_on_hup=True)


    def create_sensor_tasks(self, scheduler, publisher):
        '''Create sensor classes according to the configuration.'''

        for sname, scfg in self.cfg['sensors'].items():
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

        while True:
            mqttcfg = self.cfg['mqtt']

            publisher = MqttPublisher(
                broker=mqttcfg['broker'],
                node_name=mqttcfg['node_name'],
                topic_prefix=mqttcfg['topic_prefix'])

            self.sched = Scheduler()

            self.create_sensor_tasks(self.sched, publisher)
        
            self.sched.run()


    def on_reload(self):
        msg = 'Stopping scheduler due to SIGHUP signal.'
        logging.info(msg)

        self.sched.stop()

        CmdlApp.on_reload(self)


if __name__ == '__main__':
    MqttPublish().run()

