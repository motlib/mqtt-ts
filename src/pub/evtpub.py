'''Publish sensor events to MQTT broker.'''


import logging
import paho.mqtt.publish as mqtt_pub
import paho.mqtt.client as mqtt
import socket


class MqttPublisher():
    '''Publish sensor events to an MQTT broker.'''

    def __init__(self, broker, topic_prefix='/sensors'):
        '''Initialize a MqttPublisher instance.'''

        self.broker = broker
        # TODO: Choose between hostname and fqdn
        self.node_name = socket.gethostname()
        self.topic_prefix = topic_prefix


    def get_topic(self, evt):
        '''Generate the MQTT topic for the event.'''

        data = {
            'prefix': self.topic_prefix,
            'node': self.node_name,
            'sensor': evt.getSensorName(),
            'quantity': evt.getQuantity(),
            }

        path_tmpl = '{prefix}/{node}/{sensor}/{quantity}'
    
        return path_tmpl.format(**data)


    def publish_event(self, evt):
        '''Publish a single sensor event.'''

        # The publish might fail, e.g. due to network problems. Just log 
        # the exception and try again next time.
        try:
            topic = self.get_topic(evt)

            msg = "Publishing to topic '{0}'."
            logging.debug(msg.format(topic))

            # This fixes the protocol version to MQTT v3.1, because
            # the current version of the MQTT broker available in
            # raspbian does not support MQTT v3.1.1.
            mqtt_pub.single(
                topic=topic,
                payload=evt.toJSON(),
                hostname=self.broker,
                protocol=mqtt.MQTTv31)
        except:
            logging.exception('Publish of MQTT value failed.')


    def publish_events(self, evts):
        '''Publish a list of sensor events.'''

        for evt in evts:
            self.publish_event(evt)
