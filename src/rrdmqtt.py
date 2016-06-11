'''Use rrdtool to plot graphics from sensor values received by MQTT.'''

import json
import logging
import os
import subprocess
from time import sleep

from utils.mqttman import MQTTManager
from rrd.rrdman import RRDManager
from utils.cmdlapp import CmdlApp


class RrdMqtt(CmdlApp):
    def __init__(self):
        CmdlApp.__init__(self)
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
        
        try:
            status = self.mqtt.get_status(sigcfg['topic'])
            payload = self.mqtt.get_payload(sigcfg['topic'])

            if payload != None:
                data = json.loads(payload)

                self.rrd.update_rrd(signal, data['value'])
            
            else:
                logging.debug('No data received.')
            
        except:
            msg = "Failed to update rrdfile '{0}'."
            logging.exception(msg.format(filepath))


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
        
            graph_int = self.cfg['rrdmqtt']['graphconfig']['interval']
            cnt = graph_int
            
            # TODO: Use scheduler class
            self.stop_flag = False
            while not self.stop_flag:
                self.mqtt.tick()
            
                for sig in self.sig_cfg.keys():
                    self.update_signal(sig)

                if cnt > 0:
                    cnt -= 1
                else:
                    self.create_graphs()
                    cnt = graph_int
                
                sleep(1)


    def on_reload(self):
        CmdlApp.on_reload(self)
        self.stop_flag = True


if __name__ == '__main__':
    RrdMqtt().run()

