
from apps.datedisp import DateTimeApp
from apps.cycle import CycleIndicatorApp
from apps.rpitemp import RPiTemperature
from apps.mqttsub import MQTTSubscriberApp

def init_apps(scrman, mqtt):
    scrman.add_app(
        height=1, width=45, y=0, x=0,
        app=DateTimeApp())
    
    scrman.add_app(
        height=1, width=2, y=0, x=40,
        app=CycleIndicatorApp())

    scrman.add_app(
        height=1, width=52, y=3, x=0,
        app=RPiTemperature(label='CPU rpi3'))

    topic = '/sensors/rpi2/cputemp/temperature'
    mqtt.add_topic(topic, timeout=10)
    scrman.add_app(
        height=1, width=52, y=4, x=0,
        app=MQTTSubscriberApp(
            mqtt=mqtt,
            topic=topic,
            label='CPU rpi2',
            unit='°C'))

    topic = '/sensors/rpi2/room/temperature'
    mqtt.add_topic(topic, timeout=10)
    scrman.add_app(
        height=1, width=52, y=6, x=0,
        app=MQTTSubscriberApp(
            mqtt=mqtt,
            topic=topic,
            label='Temp. Inside',
            unit='°C'))

    topic = '/sensors/rpi2/outside/temperature'
    mqtt.add_topic(topic, timeout=10)
    scrman.add_app(
        height=1, width=52, y=7, x=0,
        app=MQTTSubscriberApp(
            mqtt=mqtt,
            topic=topic,
            label='Temp. Outside',
            unit='°C'))

    topic = '/sensors/rpi2/HTU21D/relative humidity'
    mqtt.add_topic(topic, timeout=10)
    scrman.add_app(
        height=1, width=52, y=9, x=0,
        app=MQTTSubscriberApp(
            mqtt=mqtt,
            topic=topic,
            label='Hum. Inside',
            unit='% RH'))


    topic = '/sensors/rpi2/BMP180/pressure'
    mqtt.add_topic(topic, timeout=10)
    scrman.add_app(
        height=1, width=52, y=10, x=0,
        app=MQTTSubscriberApp(
            mqtt=mqtt,
            topic=topic,
            label='Air Pressure',
            unit='mbar'))

    topic = '/sensors/rpi2/TSL2561/luminosity'
    mqtt.add_topic(topic, timeout=10)
    scrman.add_app(
        height=1, width=52, y=11, x=0,
        app=MQTTSubscriberApp(
            mqtt=mqtt,
            topic=topic,
            label='Luminosity',
            unit='Lx'))


    
