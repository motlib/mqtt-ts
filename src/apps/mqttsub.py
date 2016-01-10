import paho.mqtt.client as paho
import json

MQTT_BROKER = 'bpi1'
MQTT_TOPIC = '/sensors/rpi2/cputemp/temperature'


class MQTTSubscriberApp():

    def __init__(self):
        mqttclt = paho.Client()
        mqttclt.on_message = self.on_message
        # mqttclt.on_publish = on_publish

        mqttclt.connect(MQTT_BROKER, port=1883, keepalive=60)

        mqttclt.subscribe(MQTT_TOPIC, 0)

        mqttclt.loop_start()

        self.mqttclt = mqttclt
        self.temp = 0

        
    def on_message(self, mosq, obj, msg):
        try:
            data = json.loads(msg.payload.decode('utf-8'))
            self.temp = data['value']
        except Exception as e:
            print(e)
        

    def update(self):
        pstr = '{lbl:>30}: {val:4.1f}°C'.format(
            lbl='rpi2 CPU Temperature',
            val=self.temp)

        self.wnd.addstr(0, 0, pstr)

        
