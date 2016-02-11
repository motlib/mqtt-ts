from apps.valuedisp import ValueDisplayApp

class RPiTemperature(ValueDisplayApp):
    '''Display the local CPU temperature of the RPi.'''
    
    def __init__(self):
        ValueDisplayApp.__init__(self)
        
        self.set_label('CPU Temp.')
        self.set_unit('°C')

        
    def on_update(self):
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            tstr = f.read()

        self.set_value(int(tstr) / 1000)

        
