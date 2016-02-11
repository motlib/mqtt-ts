from argparse import ArgumentParser
import curses
import logging
import sys
from time import sleep
import yaml

from wdgtfact import WidgetFactory
from scrman import ScreenManager
from utils.mqttman import MQTTManager


MQTT_BROKER = '192.168.0.21'

class DataDisp():
    '''Main class for the data display application.'''
    
    def setup_args(self):
        parser = ArgumentParser()

        parser.add_argument(
            '-l', '--logfile',
            help='Path to the logfile.',
            default='datadisp.log')

        parser.add_argument(
            '-c', '--cfg',
            help='Path to the YAML config file.',
            default='datadisp.yaml')

        self.args = parser.parse_args()
    

    def setup_logging(self):
        '''Set up the logging framework.'''
        
        logging.basicConfig(
            filename=self.args.logfile,
            filemode='a',
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s: %(message)s')

        logging.info('Starting up')

        
    def load_config(self):
        cfgfile = self.args.cfg

        try:
            with open(cfgfile, 'r') as f:
                self.cfg = yaml.load(f)
        except:
            msg = "Failed to load config file '{0}'."
            logging.exception(msg.format(cfgfile))

            
    def run(self, stdscr):
        try:
            self.setup_args()
            
            self.setup_logging()
            self.load_config()
            
            self.scrman = ScreenManager(stdscr)
            self.mqtt = MQTTManager(self.cfg['mqtt']['broker'])

            wdgtfactory = WidgetFactory()
            wdgtcfg = self.cfg['datadisp']['widgets']
            widgets = wdgtfactory.create_widgets(wdgtcfg)
            self.scrman.add_widgets(widgets)
    
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
