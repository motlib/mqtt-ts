import curses


class ScreenManager():
    def __init__(self, stdscr):
        self.stdscr = stdscr

        self.apps = []

        curses.curs_set(False)

        
    def add_app(self, height, width, y, x, app):
        wnd = curses.newwin(height, width, y, x)

        app.wnd = wnd
        
        self.apps.append(app)

        
    def update(self):
        self.stdscr.clear()
        self.stdscr.refresh()
        
        for app in self.apps:
            app.update()
            app.wnd.refresh()
