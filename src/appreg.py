
from apps.datedisp import DateTimeApp
from apps.cycle import CycleIndicatorApp
from apps.rpitemp import RPiTemperature
from apps.mqttsub import MQTTSubscriberApp

def init_apps(scrman, mqtt):
    scrman.add_app(
        height=1, width=45, y=0, x=0,
        app=DateTimeApp())
    
    scrman.add_app(
        height=1, width=2, y=0, x=52,
        app=CycleIndicatorApp())

    scrman.add_app(
        height=1, width=52, y=3, x=0,
        app=RPiTemperature(label='CPU rpi3'))

    
    scrman.add_app(
        height=1, width=52, y=4, x=0,
        app=MQTTSubscriberApp(
            mqtt=mqtt,
            topic='/sensors/rpi2/cputemp/temperature',
            label='CPU rpi2',
            unit='°C'))

    scrman.add_app(
        height=1, width=52, y=6, x=0,
        app=MQTTSubscriberApp(
            mqtt=mqtt,
            topic='/sensors/rpi2/room/temperature',
            label='Temp. Inside',
            unit='°C'))

    scrman.add_app(
        height=1, width=52, y=7, x=0,
        app=MQTTSubscriberApp(
            mqtt=mqtt,
            topic='/sensors/rpi2/outside/temperature',
            label='Temp. Outside',
            unit='°C'))

    scrman.add_app(
        height=1, width=52, y=9, x=0,
        app=MQTTSubscriberApp(
            mqtt=mqtt,
            topic='/sensors/rpi2/HTU21D/relative humidity',
            label='Hum. Outside',
            unit='% RH'))

    scrman.add_app(
        height=1, width=52, y=10, x=0,
        app=MQTTSubscriberApp(
            mqtt=mqtt,
            topic='/sensors/rpi2/BMP180/pressure',
            label='Air Pressure',
            unit='mbar'))

    scrman.add_app(
        height=1, width=52, y=11, x=0,
        app=MQTTSubscriberApp(
            mqtt=mqtt,
            topic='/sensors/rpi2/TSL2561/luminosity',
            label='Luminosity',
            unit='Lx'))


    
