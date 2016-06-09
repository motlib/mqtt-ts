'''Simple scheduler.'''

from datetime import datetime, timedelta
from time import sleep
import logging

class Task():
    def __init__(self, interval, offset=0, name='', fct=None):
        self.interval = interval
        self.offset = offset
        self.name = name
        self.fct = fct
        

    def run(self):
        if self.fct != None:
            self.fct()
        else:
            print("Running task '{0}'.".format(self.name))


class Scheduler():
    def __init__(self):
        self.tasks = []


    def add_task(self, task):
        self.tasks.append(task)


    def find_next_task(self):
        '''Returns the task next to execute.'''

        now = datetime.now()
        min_delay = None
        min_task = None
        
        # find task with minimum delay
        for task in self.tasks:
            d = (task.next_run - now).total_seconds()
            
            if (min_delay == None) or (d < min_delay):
                min_delay = d
                min_task = task
                
        #msg = "Next task is '{0}' with {1}s delay."
        #logging.debug(msg.format(min_task.name, min_delay))

        return (min_task, min_delay)
        
    
    def run(self):
        '''Run the scheduler. 

        This contain an infinite loop in which tasks are executed.'''

        self.init_tasks()

        while True:
            (task, delay) = self.find_next_task()

            if delay <= 0:
                self.run_task(task)
            else:
                #msg = 'Scheduler sleeping for {0}s.'
                #logging.debug(msg.format(delay))
                sleep(delay)

            
    def run_task(self, task):
        msg = "Running task '{0}'."
        logging.debug(msg.format(task.name))

        task.run()

        task.next_run += timedelta(seconds=task.interval)

        now = datetime.now()

        if task.next_run < now:
            msg = "Skipping task '{0}' due to overrun."
            logging.warning(msg.format(task.name))

        while task.next_run < now:
            task.next_run += timedelta(seconds=task.interval)


    def init_tasks(self):
        now = datetime.now()

        for task in self.tasks:
            task.next_run = now + timedelta(seconds=task.offset)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s')

    s = Scheduler()
    s.add_task(Task(interval=3.21, offset=0.7, name="T_1"))
    s.add_task(Task(interval=2.651, offset=0.9, name="T_2"))

    s.run()
