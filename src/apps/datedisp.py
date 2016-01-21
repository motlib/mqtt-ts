from datetime import datetime

from apps.baseapp import BaseApp

class DateTimeApp(BaseApp):
    def update(self):
        now = datetime.now()
        txt = now.strftime('%A, %d of %B %Y %H:%M')
        
        self.wnd.addstr(0, 0, txt)
