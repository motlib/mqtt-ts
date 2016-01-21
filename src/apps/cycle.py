
from apps.baseapp import BaseApp

class CycleIndicatorApp(BaseApp):
    def __init__(self):
        self.cycle = 0
        self.cycles = '/-\|'
        
    def update(self):
        self.wnd.addstr(0, 0, self.cycles[self.cycle])
        
        self.cycle += 1
        self.cycle %= len(self.cycles)
