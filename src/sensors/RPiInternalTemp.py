from sensors.SensorBase import SensorBase, SensorEvent



class RPiInternalTemp(SensorBase):
    
        
    def sampleValues(self, valuetype=None):
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = int(f.read())
        
        temp = temp / 1000.0    
        
        return [
            SensorEvent(self.getName(), temp, 'degree celsius', 'temperature')
        ]
