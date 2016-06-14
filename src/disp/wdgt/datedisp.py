from datetime import datetime

from disp.wdgt.baseapp import BaseApp

class DateTimeApp(BaseApp):
    def __init__(self):
        BaseApp.__init__(self)
        
    def update(self):
        now = datetime.now()
        txt = now.strftime('%A, %d of %B %Y %H:%M')
        
        self.wnd.addstr(0, 0, txt)
