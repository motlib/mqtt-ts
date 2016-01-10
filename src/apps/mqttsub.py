import paho.mqtt.client as paho
import json

MQTT_BROKER = 'bpi1'
topics = {
    '/sensors/rpi2/cputemp/temperature': { 'lbl': 'rpi2 CPU Temperature', 'val': 0 },
    '/sensors/rpi2/BMP180/pressure': { 'lbl': 'Air Pressure', 'val': 0 },
    '/sensors/rpi2/HTU21D/temperature': { 'lbl': 'Temperature', 'val': 0 },
    '/sensors/rpi2/HTU21D/relative humidity': { 'lbl': 'Humidity', 'val': 0 },
    '/sensors/rpi2/TSL2561/luminosity': { 'lbl': 'Luminosity', 'val': 0 },
    }

class MQTTSubscriberApp():

    def __init__(self):
        mqttclt = paho.Client()
        mqttclt.on_message = self.on_message
        # mqttclt.on_publish = on_publish

        mqttclt.connect(MQTT_BROKER, port=1883, keepalive=60)

        for t in topics.keys():
            mqttclt.subscribe(t, 0)

        mqttclt.loop_start()

        self.mqttclt = mqttclt
        self.temp = 0

        
    def on_message(self, mosq, obj, msg):
        try:
            data = json.loads(msg.payload.decode('utf-8'))
            topics[msg.topic]['val'] = data['value']
        except Exception as e:
            #print(e)
            pass
        

    def update(self):
        y = 0
        for t in topics.values():
            pstr = '{lbl:>30}: {val:4.1f}'.format(
                lbl=t['lbl'],
                val=t['val'])

            self.wnd.addstr(y, 0, pstr)

            y += 1
