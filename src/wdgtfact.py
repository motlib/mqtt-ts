import logging

from apps.datedisp import DateTimeApp
from apps.cycle import CycleIndicatorApp
from apps.rpitemp import RPiTemperature
from apps.mqttsub import MQTTSubscriberApp

class WidgetFactory():

    def _create_instance(self, name):
        tbl = {
            'DateTimeApp': DateTimeApp,
            'CycleIndicatorApp': CycleIndicatorApp,
            'RPiTemperature': RPiTemperature,
            'MQTTSubscriberApp': MQTTSubscriberApp,
        }
        
        return tbl[name]()


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
