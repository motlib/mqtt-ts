#!/usr/bin/env python3

'''Script to display values received from an MQTT broker.'''

from argparse import ArgumentParser
import curses
import logging
import sys
from time import sleep
import yaml

from disp.wdgtfact import WidgetFactory
from disp.scrman import ScreenManager
from utils.mqttman import MQTTManager
from utils.cmdlapp import CmdlApp


class DataDisp(CmdlApp):
    '''Main class for the MQTT data display application.'''

    def __init__(self):
        CmdlApp.__init__(self)

        self.cmdlapp_config(has_cfgfile=True)
    

    def curses_main(self, stdscr):
        try:
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


    def main_fct(self):
        '''Main function to be called by CmdlApp base class.'''

        curses.wrapper(self.curses_main)

        
if __name__ == '__main__':
    DataDisp().run()
    

