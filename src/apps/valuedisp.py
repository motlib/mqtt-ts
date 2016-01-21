from apps.baseapp import BaseApp

class ValueDisplayApp(BaseApp):
     def __init__(self):
        self.val = None
        self.lbl = 'Unspecified'

        
    def set_value(self, val):
         '''Set the value to display.'''
         self.val = val

        
    def set_label(self, lbl):
        self.lbl = lbl

     def set_fmt(self, fmt):
          self.fmt = fmt
        
        
    def update(self):
        self.val = self.get_value()

        tstr = '{lbl:>30}: {val:3.1f}°C'.format(
            lbl='Core Temperature',
            val=self.temp)
        
        self.wnd.addstr(0, 0, tstr)
