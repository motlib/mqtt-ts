'''Task implementation to read sensor and publish events.'''


import logging

from utils.sched import Task


class SensorTask(Task):
    '''Task that samples a sensor and publishes the sensor events. 

    The task can be scheduled in regular intervals with the Scheduler
    class.'''

    def __init__(self, sensor, publisher, interval):
        Task.__init__(
            self, 
            name='sensor_task_' + sensor.getName())

        self.sensor = sensor
        self.publisher = publisher
        self.interval = interval


    def run(self):
        '''Sample the sensor and publish the sensor events.'''

        msg = "Reading sensor '{0}'."
        logging.debug(msg.format(self.sensor.getName()))

        try:
            sevts = self.sensor.sample()
            
            self.publisher.publish_events(sevts)
        except:
            msg = "Failed to sample sensor values of sensor '{0}'."
            logging.exception(msg.format(self.sensor.getName()))
