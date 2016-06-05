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
            self.load_config()
            
            self.scrman = ScreenManager(stdscr)
            self.mqtt = MQTTManager(self.cfg['mqtt']['broker'])

            wdgtfactory = WidgetFactory()
            wdgtcfg = self.cfg['datadisp']['widgets']
            widgets = wdgtfactory.create_widgets(wdgtcfg)
            self.scrman.add_widgets(widgets)

            logging.info('Set up screen. Everything is ready to show some data.')
        except:
            curses.endwin()
            logging.exception('Failed to set up screen.')
            sys.exit(1)
            
        try:
            # endless loop for data display
            while True:
                self.mqtt.tick()
                self.scrman.update()
                    
                sleep(1)
        except Exception as e:
            curses.endwin()
            logging.exception('Main loop failed')
            sys.exit(1)


    def main_fct(self):
        '''Main function to be called by CmdlApp base class.'''

        curses.wrapper(self.curses_main)

        
if __name__ == '__main__':
    DataDisp().run()
    

