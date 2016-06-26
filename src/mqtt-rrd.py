#!/usr/bin/env python3

'''Use rrdtool to plot graphics from sensor values received by MQTT.'''


import json
import logging

from utils.mqttman import MQTTManager
from rrd.rrdman import RRDManager
from utils.cmdlapp import CmdlApp
from utils.sched import Scheduler, Task
from sensors.sbase import SensorEvent

class RrdMqtt(CmdlApp):
    def __init__(self):
        '''Initialize the instance.

        This configures the command-line application with
        configuration file and handler for the SIGHUP signal.

        '''
        
        super().__init__()
        
        self.cmdlapp_config(
            has_cfgfile=True,
            reload_on_hup=True)

        self.stop_flag = False
       

    def load_cfgfile(self):
        '''Override load_config from CmdlApp base class.'''
        
        CmdlApp.load_cfgfile(self)
        
        # for convenient access...
        self.sig_cfg = self.cfg['rrdmqtt']['signals']
        self.graphs = self.cfg['rrdmqtt']['graphs']

        
    def update_signal(self, signal):
        sigcfg = self.sig_cfg[signal]

        # TODO: Currenly bad implemented. We update every time we have
        # a payload. But that does not mean that we just received a
        # new value.
        
        try:
            status = self.mqtt.get_status(sigcfg['topic'])
            payload = self.mqtt.get_payload(sigcfg['topic'])

            if payload != None:
                evt = SensorEvent.fromJson(payload)

                self.rrd.update_rrd(signal, evt.getValue())
            
            else:
                logging.debug('No data received.')
            
        except:
            msg = "Failed to update rrdfile '{0}'."
            logging.exception(msg.format(filepath))


    def update_all_signals(self):
        '''Task implementation to update signal values in rrd
        databases.'''

        for sig in self.sig_cfg.keys():
            self.update_signal(sig)

            
    def create_graphs(self):
        for name,graph in self.graphs.items():

            # take the default settings and update them with the
            # actual config of the graph
            graphcfg = self.cfg['rrdmqtt']['graphconfig'].copy()
            graphcfg.update(graph)

            self.rrd.create_graphs(
                name,
                graph=graphcfg,
                signalopts=self.sig_cfg)

            
    def generate_graph_configs(self):
        self.graphs = []

        # First we patch each graph config with default values, if
        # they do not yet exist in the graph config.
        defcfg = selrf.cfg['rrdmqtt']['graphconfig']
        
        for grname,grcfg in self.cfg['rrdmqtt']['graphs'].items():

            grcfg.setdefault('width', defcfg['width'])
            grcfg.setdefault('height', defcfg['height'])
            grcfg.setdefault('timespans', defcfg['timespans'])
        
        
    def initialize(self):
        self.mqtt = MQTTManager(self.cfg['mqtt']['broker'])

        self.rrd = RRDManager(
            datadir=self.cfg['rrdmqtt']['datadir'],
            graphdir=self.cfg['rrdmqtt']['graphdir'])

        for name, signal in self.sig_cfg.items():
            # Check if the rrd file exists and create if necessary
            self.rrd.check_rrd(name)

            # subscribe topics
            self.mqtt.add_topic(signal['topic'])
            self.mqtt.set_timeout(signal['topic'], signal['timeout'])


    def main_fct(self):
        while True:
            self.initialize()
        
            sched = Scheduler()

            sched.add_task(Task(
                    interval=1, 
                    name='mqtt_tick', 
                    fct=self.mqtt.tick))

            sched.add_task(Task(
                    interval=self.cfg['rrdmqtt']['graphconfig']['interval'],
                    name='create_graphs',
                    fct=self.create_graphs))

            sched.add_task(Task(
                    interval=1,
                    name='upd_signals',
                    fct=self.update_all_signals))
                     
            sched.run()


    def on_reload(self):
        CmdlApp.on_reload(self)
        self.stop_flag = True


if __name__ == '__main__':
    RrdMqtt().run()

