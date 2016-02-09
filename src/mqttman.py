import paho.mqtt.client as paho
import json
import logging

from apps.baseapp import BaseApp
from apps.valuedisp import ValueDisplayApp


STAT_DISCONNECT = 'D'
STAT_TIMEOUT = 'T'
STAT_UPDATED = 'U'
STAT_VALID = ' '


class MQTTManager():
    def __init__(self, broker):
        self.connected = False
        self.topics = {}
        self.broker = broker

        
    def add_topic(self, topic, timeout=0):
        self.topics[topic] = {
            'payload': None,
            'status': 'N',
            'timeout': timeout,
            'received': timeout,
        }

        if self.connected == True:
            self.mqttclt.subscribe(topic, 0)

            
    def set_timeout(self, topic, timeout):
        self.topics[topic]['timeout'] = timeout
            
        
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

        self.check_timeout()

            
    def check_timeout(self):
        '''Check timeout status of all topics.'''
        
        for tdata in self.topics.values():
            if tdata['timeout'] != 0:
                if tdata['received'] > 0:
                    tdata['received'] -= 1
                else:
                    tdata['status'] = STAT_TIMEOUT

                    
    def mqtt_connect(self):
        '''Connect to the MQTT broker and subscribe to all registered topics.'''
        
        try:
            self.conn_err = 0

            self.mqttclt = paho.Client()
            self.mqttclt.on_message = self.on_message
            self.mqttclt.on_disconnect = self.on_disconnect
            self.mqttclt.on_connect = self.on_connect
            
            self.mqttclt.connect(
                self.broker,
                port=1883,
                keepalive=60)
            
            for topic in self.topics.keys():
                self.mqttclt.subscribe(topic, 0)

            self.mqttclt.loop_start()
        except:
            logging.exception('Failed to extablish connection to MQTT broker.')

            
    def on_message(self, mosq, obj, msg):
        try:
            topic = self.topics[msg.topic]
            topic['payload'] = msg.payload.decode('utf-8')
            topic['status'] = STAT_UPDATED
            topic['received'] = topic['timeout']
            
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


        
