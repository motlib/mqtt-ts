from apps.baseapp import BaseApp

class ValueDisplayApp(BaseApp):
    def __init__(self):
        self.set_value(-1)
        self.set_label('Unspecified')
        self.set_fmt('{val:8.1f}')
        self.set_unit('#')

        
    def set_value(self, value):
         '''Set the value to display.'''
         self.value = value

        
    def set_label(self, lbl):
        self.label = lbl

        
    def set_fmt(self, fmt):
        self.fmt = fmt

          
    def set_unit(self, unit):
        self.unit = unit


    def on_update(self):
        pass
        
        
    def update(self):
        self.on_update()
        
        fmt_str = '{lbl:>30}: ' + self.fmt + ' {unit}'
        
        tstr = fmt_str.format(
            lbl=self.label,
            val=self.value,
            unit=self.unit)
        
        self.wnd.addstr(0, 0, tstr)
