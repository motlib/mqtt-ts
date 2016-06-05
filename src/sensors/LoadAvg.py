from sensors.SensorBase import SensorBase, SensorEvent



class LoadAvg(SensorBase):
    
    def __init__(self, sensor_name):
        SensorBase.__init__(self, 
            sensor_name=sensor_name)
        
        
    def sampleValues(self, valuetype=None):
        with open('/proc/loadavg', 'r') as f:
            line = f.read()
            data = line.split(' ')
            load = float(data[2])
            
        return [
            SensorEvent(self.getName(), load, '', 'system_load')
        ]
