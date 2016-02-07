import paho.mqtt.client as paho
import json
import logging

from apps.baseapp import BaseApp
from apps.valuedisp import ValueDisplayApp

MQTT_BROKER = '192.168.0.21'

#topics = {
#    '/sensors/rpi2/cputemp/temperature': {
#        'lbl': 'rpi2 CPU Temperature',
#        'unit': '°C'
#    },
#    '/sensors/rpi2/BMP180/pressure': {
#        'lbl': 'Air Pressure',
#        'unit': 'hPa'
#    },
#    '/sensors/rpi2/HTU21D/temperature': {
#        'lbl': 'Temperature',
#        'unit': '°C'
#    },
#    '/sensors/rpi2/HTU21D/relative humidity': {
#        'lbl': 'Humidity',
#        'unit': '% RH'
#    },
#    '/sensors/rpi2/TSL2561/luminosity': {
#        'lbl': 'Luminosity',
#        'unit': 'Lx'
#    },
#    '/sensors/rpi2/room/temperature': {
#        'lbl': 'Room',
#        'unit': '°C'
#    },
#    '/sensors/rpi2/outside/temperature': {
#        'lbl': 'Outside',
#        'unit': '°C'
#    },
#}

CONN_ERR_LIMIT = 5


STAT_DISCONNECT = 'D'
STAT_TIMEOUT = 'T'
STAT_UPDATED = 'U'
STAT_VALID = 'V'

class MQTTSubscriber():
    def __init__(self):
        self.connected = False
        self.topics = {}

        
    def add_topic(self, topic, timeout=0):
        self.topics[topic] = {
            'payload': None,
            'status': 'N',
            'timeout': timeout,
            'received': 0,
        }

        if self.connected == True:
            self.mqttclt.subscribe(topic, 0)

        
    def get_payload(self, topic):
        tdata = self.topics[topic]

        if tdata['status'] == STAT_UPDATED:
            tdata['status'] = STAT_VALID
        
        return tdata['payload']

    
    def get_status(self, topic):
        return self.topics[topic]['status']

    
    def tick(self):
        if not self.connected:
            self.mqtt_connect()

        for tdata in self.topics.values():
            if tdata['timeout'] != 0:
                if tdata['received'] > 0:
                    tdata['received'] -= 1
                else:
                    tdata['status'] = STAT_TIMEOUT

                    
    def mqtt_connect(self):
        try:
            self.conn_err = 0

            self.mqttclt = paho.Client()
            self.mqttclt.on_message = self.on_message
            self.mqttclt.on_disconnect = self.on_disconnect
            self.mqttclt.on_connect = self.on_connect
            
            self.mqttclt.connect(MQTT_BROKER, port=1883, keepalive=60)
            
            for topic in self.topics.keys():
                self.mqttclt.subscribe(topic, 0)

            self.mqttclt.loop_start()
        except:
            logging.exception('Failed to extablish connection to MQTT broker.')

            
    def on_message(self, mosq, obj, msg):
        try:
            self.topics[msg.topic]['payload'] = msg.payload.decode('utf-8')
            self.topics[msg.topic]['status'] = STAT_UPDATED
        except Exception as e:
            msg = "Failed to parse MQTT message in topic '{0}'."
            logging.warn(msg.format(msg.topic))

            
    def on_connect(self, client, userdata, flags, rc):
        self.connected = True

        
    def on_disconnect(client, userdata, rc):
        self.connected = False

        msg = 'Unexpected MQTT disconnect with reason {0}.'
        logging.warning(msg.format(rc))

        # mark all topics as error
        for topic in self.topics.values():
            topic['status'] = STAT_DISCONNECT


            
class MQTTSubscriberApp(ValueDisplayApp):
    def __init__(self,
            mqtt,
            topic,
            label='Label',
            unit='Unit'):
        
        ValueDisplayApp.__init__(self, label, unit)
        
        self.mqtt = mqtt
        self.topic = topic
        
        self.mqtt.add_topic(topic)


    def on_update(self):
        # status needs to be retrieved first because get_payload
        # resets status.
        status = self.mqtt.get_status(self.topic)
        payload = self.mqtt.get_payload(self.topic)
        
        if payload != None:
            data = json.loads(payload)
            self.set_value(data['value'])
        else:
            self.set_value(0)

