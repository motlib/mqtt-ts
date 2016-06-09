'''Read the temperature from a DS1820 onewire sensor.'''


from sensors.sbase import SensorBase, SensorEvent


class W1ThermSensor(SensorBase):
    
    def __init__(self, scfg):
        SensorBase.__init__(self, scfg)

        self.sensor_id = scfg['w1_id']
        
        
    def sample(self):
        file = '/sys/bus/w1/devices/{0}/w1_slave'.format(
            self.sensor_id)
        
        with open(file, 'r') as f:
            data = f.read()

        lines = data.split('\n')
        td = lines[1].split(' ')[9]
        td2 = td.split('=')[1]

        temp = float(td2) / 1000.0 
        
        return [
            self.new_event(temp, 'degree celsius', 'temperature')
        ]
