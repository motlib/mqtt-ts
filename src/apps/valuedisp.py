from apps.baseapp import BaseApp

class ValueDisplayApp(BaseApp):
    def __init__(self, label='Label', unit='Unit'):
        self.set_value(-1)
        self.set_label(label)
        self.set_fmt('{val:8.1f}')
        self.set_unit(unit)
        self.set_update_indicator(False)

        self.updated = False

    def set_update_indicator(self, uind):
        '''Set the update indicator.'''
        self.uind = uind
        

    def set_value(self, value):
         '''Set the value to display.'''
         self.value = value
         self.updated = True

        
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
        
        fmt_str = '{lbl:>30} : '
        if self.uind:
            fmt_str += '{uind} '
        fmt_str += self.fmt + ' {unit}'

        if self.updated:
            self.updated = False
            uind = '*'
        else:
            uint = ' '
        
        tstr = fmt_str.format(
            lbl=self.label,
            uint=uind,
            val=self.value,
            unit=self.unit)
        
        self.wnd.addstr(0, 0, tstr)
        
