'''Simple scheduler.'''

from datetime import datetime, timedelta
from time import sleep
import logging

class Task():
    '''Base class for scheduler tasks.'''

    def __init__(self, interval, offset=0, name='', fct=None):
        self.interval = interval
        self.offset = offset
        self.name = name
        self.fct = fct
        

    def run(self):
        if self.fct != None:
            self.fct()
        else:
            msg = "Running dummy task function for task '{0}'."
            logging.warning(msg.format(self.name))


class Scheduler():
    def __init__(self, max_delay=2):
        '''Initialize the scheduler.

        The max_delay parameter can be used to limit the maximum sleep
        time. This can be useful, if the scheduler shall be stopped
        interactively to ensure that is responds in time.'''

        self.max_delay = max_delay

        self.tasks = []
        self.debug_log = False
        self.stop_flag = False

        # Time tolerance to schedule tasks. If a task is to be
        # scheduled in less than sched_tolerance, it is executed
        # directly to prevent very short delays that are not exact.
        self.sched_tolerance = 0.05


    def add_task(self, task):
        '''Add a task to be scheduled / executed by the scheduler.'''

        self.tasks.append(task)


    def find_next_task(self):
        '''Returns the task next to execute.'''

        now = datetime.now()
        min_delay = None
        min_task = None
        
        # find task with minimum delay
        for task in self.tasks:
            # do not schedule tasks which have the interval set to 0. 
            if task.interval == 0:
                continue
            d = (task.next_run - now).total_seconds()
            
            if (min_delay == None) or (d < min_delay):
                min_delay = d
                min_task = task
                
        if self.debug_log == True:
            msg = "Next task is '{0}' with {1}s delay."
            logging.debug(msg.format(min_task.name, min_delay))

        return (min_task, min_delay)
        
    
    def run(self):
        '''Run the scheduler. 

        This contain an infinite loop in which tasks are executed.'''

        if len(self.tasks) == 0:
            # TODO: Is there a better exception type?
            raise Exception('No tasks scheduled. Scheduler has nothing to do.')

        self.init_tasks()

        while not self.stop_flag:
            (task, delay) = self.find_next_task()

            if delay <= self.sched_tolerance:
                self.run_task(task)
            else:
                # Limit the maximum sleep time to max_delay. 
                delay = min(delay, self.max_delay)

                if self.debug_log == True:
                    msg = 'Scheduler sleeping for {0}s.'
                    logging.debug(msg.format(delay))

                sleep(delay)

            
    def run_task(self, task):
        if self.debug_log == True:
            msg = "Running task '{0}'."
            logging.debug(msg.format(task.name))

        task.run()

        task.next_run += timedelta(seconds=task.interval)

        now = datetime.now()

        while task.next_run < now:
            msg = "Skipping task '{0}' due to overrun."
            logging.warning(msg.format(task.name))
            task.next_run += timedelta(seconds=task.interval)


    def init_tasks(self):
        now = datetime.now()

        for task in self.tasks:
            task.next_run = now + timedelta(seconds=task.offset)

    def stop(self):
        self.stop_flag = True


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s')

    s = Scheduler()
    s.add_task(Task(interval=3.21, offset=0.7, name="T_1"))
    s.add_task(Task(interval=2.651, offset=0.9, name="T_2"))

    s.run()
