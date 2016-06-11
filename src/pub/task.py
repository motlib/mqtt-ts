'''Task implementation to read sensor and publish events.'''


import logging

from utils.sched import Task
from utils.clsinst import get_instance_by_name


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

        msg = "Created sensor instance '{sensor_name}' from class " \
            "'{sensor_class}'."
        logging.info(msg.format(**scfg))


    def run(self):
        msg = "Reading sensor '{0}'."
        logging.debug(msg.format(self.sensor.getName()))

        try:
            sevts = self.sensor.sample()
            
            self.publisher.publish_events(sevts)
        except:
            msg = "Failed to sample sensor values of sensor '{0}'."
            logging.exception(msg.format(self.sensor.getName()))
