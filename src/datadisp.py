from argparse import ArgumentParser
import curses
import logging
import sys
from time import sleep
import yaml

from utils.wdgtfact import WidgetFactory
from utils.scrman import ScreenManager
from utils.mqttman import MQTTManager
from utils.cmdlapp import CmdlApp


MQTT_BROKER = '192.168.0.21'

class DataDisp(CmdlApp):
    '''Main class for the MQTT data display application.'''
    
    def setup_args(self):
        '''Override functoin from CmdlApp. Add additional arguments to
        command-line parser.
        '''

        CmdlApp.setup_args(self)

        self.parser.add_argument(
            '-c', '--cfg',
            help='Path to the YAML config file.',
            default='datadisp.yaml')
    
        
    def load_config(self):
        '''Load the configuration file.

        The file is specified by command line argument `logfile`.

        '''
        
        msg = "Reading config file '{0}'."
        logging.debug(msg.format(self.args.cfg))

        try:
            with open(self.args.cfg, 'r') as f:
                self.cfg = yaml.load(f)
        except:
            msg = "Failed to load config file '{0}'."
            logging.error(msg.format(self.args.cfg))
            sys.exit(1)

            
    def curses_main(self, stdscr):
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


    def main_fct(self):
        '''Main function to be called by CmdlApp base class.'''

        curses.wrapper(self.curses_main)

        
if __name__ == '__main__':
    DataDisp().run()
    

