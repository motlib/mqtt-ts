import paho.mqtt.client as paho
import json
import logging

from apps.baseapp import BaseApp


MQTT_BROKER = '192.168.0.21'

topics = {
    '/sensors/rpi2/cputemp/temperature': { 'lbl': 'rpi2 CPU Temperature'},
    '/sensors/rpi2/BMP180/pressure': { 'lbl': 'Air Pressure' },
    '/sensors/rpi2/HTU21D/temperature': { 'lbl': 'Temperature' },
    '/sensors/rpi2/HTU21D/relative humidity': { 'lbl': 'Humidity' },
    '/sensors/rpi2/TSL2561/luminosity': { 'lbl': 'Luminosity' },
    }

CONN_ERR_LIMIT = 5


class MQTTSubscriberApp(BaseApp):

    def __init__(self):
        self.mqtt_connect()

        for t in topics.values():
            t['updated'] = False
            t['val'] = 0
        
        
    def mqtt_connect(self):
        try:
            self.conn_err = 0

            self.mqttclt = paho.Client()
            self.mqttclt.on_message = self.on_message
            self.mqttclt.on_disconnect = self.on_disconnect
            
            self.mqttclt.connect(MQTT_BROKER, port=1883, keepalive=60)
            
            for t in topics.keys():
                self.mqttclt.subscribe(t, 0)

            self.mqttclt.loop_start()
        except:
            logging.exception('Failed to extablish connection to MQTT broker.')

        
    def on_message(self, mosq, obj, msg):
        self.conn_err = 0
        
        try:
            data = json.loads(msg.payload.decode('utf-8'))
            topics[msg.topic]['val'] = data['value']
            topics[msg.topic]['updated'] = True
        except Exception as e:
            msg = "Failed to parse MQTT message in topic '{0}'."
            logging.warn(msg.format(msg.topic))

        
    def on_disconnect(client, userdata, rc):
        if rc != MQTT_ERR_SUCCESS:
            logging.warning('MQTT client unexpected disconnect. Trying to reconnect.')
            
            self.conn_err += 1
            if self.conn_err < CONN_ERR_LIMIT:
                self.mqtt_connect()
            else:
                # giving up, 
                pass
        else:
            # disconnect was requested by API, do nothing
            pass
            
    def update(self):
        for y, t in enumerate(topics.values()):

            if t['updated']:
                upd = '*'
                t['updated'] = False
            else:
                upd = ' '
            
            pstr = '{lbl:>30}: {val:4.1f} {upd}'.format(
                lbl=t['lbl'],
                val=t['val'],
                upd=upd)

            self.wnd.addstr(y, 0, pstr)

            y += 1
