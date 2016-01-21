from apps.baseapp import BaseApp

class RPiTemperature(BaseApp):
    def __init__(self):
        self.temp = None

    def get_temp(self):
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            tstr = f.read()

        self.temp = int(tstr) / 1000

        
    def update(self):
        self.get_temp()

        tstr = '{lbl:>30}: {val:3.1f}°C'.format(
            lbl='Core Temperature',
            val=self.temp)
        
        self.wnd.addstr(0, 0, tstr)
