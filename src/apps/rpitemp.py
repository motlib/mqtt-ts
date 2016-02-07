from apps.valuedisp import ValueDisplayApp

class RPiTemperature(ValueDisplayApp):
    def __init__(self, label='CPU Temperature'):
        ValueDisplayApp.__init__(self, label)
        self.set_unit('°C')

        
    def on_update(self):
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            tstr = f.read()

        self.set_value(int(tstr) / 1000)

        
