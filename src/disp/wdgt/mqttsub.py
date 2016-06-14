import json

from disp.wdgt.valuedisp import ValueDisplayApp
from utils.mqttman import MQTTManager
            
class MQTTSubscriberApp(ValueDisplayApp):
    def __init__(self):
        ValueDisplayApp.__init__(self)
        
        self.mqtt = MQTTManager.get_instance()

        self.topic = None
        self.timeout = 0
        

    def set_timeout(self, timeout):
        self.timeout = timeout
        
        if self.topic != None:
            self.mqtt.set_timeout(self.topic, timeout)

            
    def set_topic(self, topic):
        self.topic = topic
        
        self.mqtt.add_topic(topic, self.timeout)
        
        
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

        
