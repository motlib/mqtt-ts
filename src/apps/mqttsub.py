import paho.mqtt.client as paho
import json
import logging

from apps.baseapp import BaseApp


MQTT_BROKER = '192.168.0.21'

topics = {
    '/sensors/rpi2/cputemp/temperature': {
        'lbl': 'rpi2 CPU Temperature',
        'unit': '°C'
    },
    '/sensors/rpi2/BMP180/pressure': {
        'lbl': 'Air Pressure',
        'unit': 'hPa'
    },
    '/sensors/rpi2/HTU21D/temperature': {
        'lbl': 'Temperature',
        'unit': '°C'
    },
    '/sensors/rpi2/HTU21D/relative humidity': {
        'lbl': 'Humidity',
        'unit': '% RH'
    },
    '/sensors/rpi2/TSL2561/luminosity': {
        'lbl': 'Luminosity',
        'unit': 'Lx'
    },
    '/sensors/rpi2/room/temperature': {
        'lbl': 'Room',
        'unit': '°C'
    },
    '/sensors/rpi2/outside/temperature': {
        'lbl': 'Outside',
        'unit': '°C'
    },
}

CONN_ERR_LIMIT = 5


class MQTTSubscriberApp(BaseApp):
    def __init__(self):
        # self.mqtt_connect()
        self.connected = False

        for t in topics.values():
            t['updated'] = False
            t['value'] = 0
        
         
    def mqtt_connect(self):
        try:
            self.conn_err = 0

            self.mqttclt = paho.Client()
            self.mqttclt.on_message = self.on_message
            self.mqttclt.on_disconnect = self.on_disconnect
            self.mqttclt.on_connect = self.on_connect
            
            self.mqttclt.connect(MQTT_BROKER, port=1883, keepalive=60)
            
            for t in topics.keys():
                self.mqttclt.subscribe(t, 0)

            self.mqttclt.loop_start()
        except:
            logging.exception('Failed to extablish connection to MQTT broker.')

        
    def on_message(self, mosq, obj, msg):
        try:
            data = json.loads(msg.payload.decode('utf-8'))
            topics[msg.topic]['value'] = data['value']
            topics[msg.topic]['updated'] = True
        except Exception as e:
            msg = "Failed to parse MQTT message in topic '{0}'."
            logging.warn(msg.format(msg.topic))

            
    def on_connect(self, client, userdata, flags, rc):
        self.connected = True

        
    def on_disconnect(client, userdata, rc):
        self.connected = False
        
        #if rc != MQTT_ERR_SUCCESS:
        #    logging.warning('MQTT client unexpected disconnect. Trying to reconnect.')
        #    
        #    self.conn_err += 1
        #    if self.conn_err < CONN_ERR_LIMIT:
        #        self.mqtt_connect()
        #    else:
        #        # giving up, 
        #        pass
        #else:
        #    # disconnect was requested by API, do nothing
        #    pass

        
    def update(self):
        if not self.connected:
            self.mqtt_connect()
            
        for y, t in enumerate(topics.values()):

            if t['updated']:
                upd = '*'
                t['updated'] = False
            else:
                upd = ' '
            
            pstr = '{lbl:>30}: {upd} {val:6.1f} {unit}'.format(
                lbl=t['lbl'],
                val=t['value'],
                unit=t['unit'],
                upd=upd)

            self.wnd.addstr(y, 0, pstr)

