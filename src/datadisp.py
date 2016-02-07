from time import sleep
import curses
import logging
import sys

from appreg import init_apps
from scrman import ScreenManager
from apps.mqttsub import MQTTSubscriber


def setup_logging():
    logging.basicConfig(
        filename='datadisp.log',
        filemode='a',
        level=logging.WARNING,
        format='%(asctime)s %(levelname)s: %(message)s')


def main(stdscr):
    try:
        setup_logging()
        
        scrman = ScreenManager(stdscr)
        mqtt = MQTTSubscriber()

        
        init_apps(scrman, mqtt)

        # endless loop for data display
        while True:
            mqtt.tick()
            scrman.update()
                
            sleep(1)
    except Exception as e:
        print(e)
        logging.exception('Main loop failed')
        sys.exit(1)

        
if __name__ == '__main__':
    curses.wrapper(main)
