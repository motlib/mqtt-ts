'''Sensor implementation for the load average values.'''


from sensors.sbase import SensorBase


class LoadAvg(SensorBase):
    def sampleValues(self):
        with open('/proc/loadavg', 'r') as f:
            data = f.read().split(' ')[0:3]

        load = [float(v) for v in data]
            
        return [
            self.new_event(load[0], '', 'load_1m'),
            self.new_event(load[0], '', 'load_5m'),
            self.new_event(load[0], '', 'load_15m'),
        ]
