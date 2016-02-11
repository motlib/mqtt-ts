import paho.mqtt.client as paho
import json
import logging


STAT_DISCONNECT = 'D'
STAT_TIMEOUT = 'T'
STAT_UPDATED = 'U'
STAT_VALID = ' '


class MQTTManager():
    '''Class to manage reception of MQTT messages.

    This automatically reconnects to the broker if the connection is
    lost. Also checks for timeout conditions of the subscribed topics.

    All times (timeout time) are measured based on the call cycle of
    the tick() function. Usually this can be called once per second.

    '''

    inst = None
    
    def get_instance():
        '''Return the one created instance of the MQTTManager.

        This is similar to a singleton pattern. You create one
        instance of the manager as usual and then everywhere retrieve
        that instance by calling the get_instance() function.

        '''
        
        if MQTTManager.inst == None:
            raise ValueError('Instance has not yet been created!')
        
        return MQTTManager.inst
    
    
    def __init__(self, broker):
        self.connected = False
        self.topics = {}
        self.broker = broker

        MQTTManager.inst = self

        
    def add_topic(self, topic, timeout=0):
        '''Add a topic to subscribe. Optionally takes the timeout time for
        this topic.

        '''
        
        self.topics[topic] = {
            'payload': None,
            'status': 'N',
            'timeout': timeout,
            'received': timeout,
        }

        if self.connected == True:
            self.mqttclt.subscribe(topic, 0)

            
    def set_timeout(self, topic, timeout):
        '''Sets the timeout time for a topic.'''
        
        self.topics[topic]['timeout'] = timeout
            
        
    def get_payload(self, topic):
        '''Get the last received payload for the given topic.

        This also resets the receive status from updated to valid. So
        get_status needs to be called before calling this function.'''
        
        tdata = self.topics[topic]

        if tdata['status'] == STAT_UPDATED:
            tdata['status'] = STAT_VALID
        
        return tdata['payload']

    
    def get_status(self, topic):
        '''Return the receive status of a topic.

        Must be called before calling get_payload.'''
        
        return self.topics[topic]['status']

    
    def tick(self):
        '''Execute regular maintenance tasks. Reconnects to the broker
        if the connection is lost. Checks the timeout status of the
        subscribed topics.'''
        
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
        '''Callback function for the mqtt client. Called on message reception.'''
        
        try:
            topic = self.topics[msg.topic]
            topic['payload'] = msg.payload.decode('utf-8')
            topic['status'] = STAT_UPDATED
            topic['received'] = topic['timeout']
            
        except Exception as e:
            msg = "Failed to parse MQTT message in topic '{0}'."
            logging.warn(msg.format(msg.topic))

            
    def on_connect(self, client, userdata, flags, rc):
        '''Callback function for the mqtt client. Called when a connection to 
        the broker is established.'''

        self.connected = True

        
    def on_disconnect(client, userdata, rc):
        '''Callback function for the mqtt client. Called when the connection to
        the broker is closed or lost.'''
        
        self.connected = False

        msg = 'Unexpected MQTT disconnect with reason {0}.'
        logging.warning(msg.format(rc))

        # set all topics to error state
        for topic in self.topics.values():
            topic['status'] = STAT_DISCONNECT
