

import logging

from disp.wdgt.datedisp import DateTimeApp
from disp.wdgt.cycle import CycleIndicatorApp
from disp.wdgt.rpitemp import RPiTemperature
from disp.wdgt.mqttsub import MQTTSubscriberApp
from utils.clsinst import get_instance_by_name

class WidgetFactory():


    def _create_instance(self, name):
        return get_instance_by_name(name)


    def create_widget(self, name, cfg):
        msg = "Create widget '{0}' from class '{1}'."
        logging.debug(msg.format(name, cfg['class']))
            
        inst = self._create_instance(cfg['class'])
    
        attrs = [key for key in cfg.keys() if key != 'class']
    
        for attr in attrs:
            func = getattr(inst, 'set_' + attr)
            func(cfg[attr])

        return inst
    

    def create_widgets(self, wdgtcfg):
        widgets = []
        
        for name,cfg in wdgtcfg.items():
            widgets.append(
                self.create_widget(name, cfg))
            
        return widgets
