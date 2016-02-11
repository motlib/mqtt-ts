from time import sleep
import curses
import logging
import sys
from argparse import ArgumentParser

from appreg import init_apps
from scrman import ScreenManager
from utils.mqttman import MQTTManager


MQTT_BROKER = '192.168.0.21'

class DataDisp():

    def setup_args(self):
        parser = ArgumentParser()
        parser.add_argument(
            '-l', '--logfile',
            help='Path to the logfile.',
            default='datadisp.log')

        self.args = parser.parse_args()
    

    def setup_logging(self):
        '''Set up the logging framework.'''
        
        logging.basicConfig(
            filename=self.args.logfile,
            filemode='a',
            level=logging.WARNING,
            format='%(asctime)s %(levelname)s: %(message)s')


    def run(self, stdscr):
        try:
            self.setup_args()
            
            self.setup_logging()
            
            self.scrman = ScreenManager(stdscr)
            self.mqtt = MQTTManager(MQTT_BROKER)
            
            init_apps(self.scrman, self.mqtt)
    
            # endless loop for data display
            while True:
                self.mqtt.tick()
                self.scrman.update()
                    
                sleep(1)
        except Exception as e:
            print(e)
            logging.exception('Main loop failed')
            sys.exit(1)

        
if __name__ == '__main__':
    datadisp = DataDisp()
    
    curses.wrapper(datadisp.run)
