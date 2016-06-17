'''System info related sensor implementations.'''


from sensors.sbase import SensorBase
from datetime import datetime


class NetTraffic(SensorBase):
    '''Measures the average rx and tx throughput of a network interface.'''

    def __init__(self, scfg):
        super().__init__(scfg)

        self.device = scfg['device']

        self.lasttime = None
        self.old_tx = None
        self.old_rx = None


    def get_file_value(self, filename):
        with open(filename, 'r') as f:
            val = float(f.read())                 

        return val


    def sample(self):

        patht = '/sys/class/net/{dev}/statistics/{stat}'

        rx = self.get_file_value(patht.format(
                dev=self.device, stat='rx_bytes'))

        tx = self.get_file_value(patht.format(
                dev=self.device, stat='tx_bytes'))
        
        t = datetime.now()

        evts = []
        if self.old_rx is not None:
            
            val = (rx - self.old_rx) / ((t - self.lasttime).total_seconds())

            # TODO: I need bytes per second!
            evts.append(
                self.new_event(val, 'bytes per second', 'rx_throughput'))

        if self.old_tx is not None:
            val = (tx - self.old_tx) / ((t - self.lasttime).total_seconds())

            # TODO: I need bytes per second!
            evts.append(
                self.new_event(val, 'bytes per second', 'tx_throughput'))

        self.old_rx = rx
        self.old_tx = tx
        self.lasttime = t

        return evts
