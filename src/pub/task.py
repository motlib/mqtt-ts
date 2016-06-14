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
            interval=0, 
            name='task_' + scfg['sensor_name'])
        
        self.scfg = scfg
        self.publisher = publisher

        # Create an instance of the sensor class
        args = [scfg]
        self.sensor = get_instance_by_name(
            scfg['sensor_class'],
            *args)

        if 'interval' in scfg:
            itype = 'configured'
            self.interval = scfg['interval']
        else:
            itype = 'default'
            self.interval = self.sensor.get_default_interval()
        
        msg = "Created sensor instance '{sensor_name}' from class " \
            "'{sensor_class}'. Using {itype} sampling interval {ival}s." 
        logging.info(msg.format(
                sensor_name=scfg['sensor_name'],
                sensor_class=scfg['sensor_class'],
                itype=itype,
                ival=self.interval))


    def run(self):
        msg = "Reading sensor '{0}'."
        logging.debug(msg.format(self.sensor.getName()))

        try:
            sevts = self.sensor.sample()
            
            self.publisher.publish_events(sevts)
        except:
            msg = "Failed to sample sensor values of sensor '{0}'."
            logging.exception(msg.format(self.sensor.getName()))
