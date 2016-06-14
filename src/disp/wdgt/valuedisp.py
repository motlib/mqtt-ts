from disp.wdgt.baseapp import BaseApp

class ValueDisplayApp(BaseApp):
    def __init__(self):
        BaseApp.__init__(self)
        
        self.set_value(-1)
        self.set_label('Label')
        self.set_fmt('{val:8.1f}')
        self.set_unit('Unit')
        self.set_status_flag(' ')


    def set_status_flag(self, stat):
        '''Set the status flag.'''
        
        self.stat = stat
        

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
        
        fmt_str = '{lbl:>15} {stat} : '
        fmt_str += self.fmt + ' {unit}'
        
        tstr = fmt_str.format(
            lbl=self.label,
            stat=self.stat,
            val=self.value,
            unit=self.unit)
        
        self.wnd.addstr(0, 0, tstr)
        
