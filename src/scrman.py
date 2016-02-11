import curses


class ScreenManager():
    def __init__(self, stdscr):
        self.stdscr = stdscr

        self.widgets = []

        curses.curs_set(False)

        
    def add_widget(self, wdgt):
        wnd = curses.newwin(
            wdgt.height,
            wdgt.width,
            wdgt.y,
            wdgt.x)

        wdgt.wnd = wnd
        
        self.widgets.append(wdgt)

        
    def add_widgets(self, widgets):
        for wdgt in widgets:
            self.add_widget(wdgt)

        
    def update(self):
        self.stdscr.clear()
        self.stdscr.refresh()
        
        for wdgt in self.widgets:
            wdgt.update()
            wdgt.wnd.refresh()
