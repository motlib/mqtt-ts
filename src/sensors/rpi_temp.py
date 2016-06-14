'''Read the cpu temperature of the Raspberry Pi.'''


from sensors.sbase import SensorBase


# TODO: Rename to generic thermal zone sensor
class RPiInternalTemp(SensorBase):
    def sample(self):
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read())
        
        temp = temp / 1000.0    
        
        return [
            self.new_event(temp, 'degree celsius', 'temperature')
        ]
