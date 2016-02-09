import paho.mqtt.client as paho
import json
import logging

from apps.baseapp import BaseApp
from apps.valuedisp import ValueDisplayApp

            
class MQTTSubscriberApp(ValueDisplayApp):
    def __init__(self,
            mqtt,
            topic,
            label='Label',
            unit='Unit'):
        
        ValueDisplayApp.__init__(self, label, unit)
        
        self.mqtt = mqtt
        self.topic = topic
        

    def on_update(self):
        # status needs to be retrieved first because get_payload
        # resets status.
        status = self.mqtt.get_status(self.topic)
        payload = self.mqtt.get_payload(self.topic)

        try:
            data = json.loads(payload)
            value = data['value']
        except:
            value = 0
            status = 'E'

        self.set_value(value)
        self.set_status_flag(status)

        
