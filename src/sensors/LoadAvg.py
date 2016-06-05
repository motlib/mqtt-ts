from sensors.SensorBase import SensorBase, SensorEvent



class LoadAvg(SensorBase):
    
    def __init__(self, scfg):
        SensorBase.__init__(self, 
            scfg=scfg)
        
        
    def sampleValues(self, valuetype=None):
        with open('/proc/loadavg', 'r') as f:
            line = f.read()
            data = line.split(' ')
            load = float(data[2])
            
        return [
            SensorEvent(self.getName(), load, '', 'system_load')
        ]
