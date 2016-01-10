from time import sleep
import curses

from appreg import init_apps
from scrman import ScreenManager

def main(stdscr):
    scrman = ScreenManager(stdscr)

    init_apps(scrman)

    # endless loop for data display
    while True:
        scrman.update()
                
        sleep(1)
        
if __name__ == '__main__':
    curses.wrapper(main)
