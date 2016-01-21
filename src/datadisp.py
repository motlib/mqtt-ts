from time import sleep
import curses
import logging
import sys

from appreg import init_apps
from scrman import ScreenManager


def setup_logging():
    try:
        logging.basicConfig(
            filename='/var/log/datadisp.log',
            filemode='a',
            level=logging.WARNING)
    except:
        pass    
        


def main(stdscr):
    try:
        setup_logging()
        
        scrman = ScreenManager(stdscr)

        init_apps(scrman)

        # endless loop for data display
        while True:
            scrman.update()
                
            sleep(1)
    except Exception as e:
        print(e)
        logging.exception('Main loop failed')
        sys.exit(1)

if __name__ == '__main__':
    curses.wrapper(main)
