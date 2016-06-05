import logging
from sensors.LoadAvg import LoadAvg

def get_sensors():
    '''Set up the sensors.'''

    sensors = [
        LoadAvg('LoadAvg')
        ]

    return sensors


config = {
    # node name as used in the mqtt topic path
    'node_name': 'yytp',
    
    # Hostname of the MQTT broker
    'mqtt_broker': 'bpi1.fritz.box',

    # The topic name is constructed from sensor name and measured quantity 
    # (temperature, pressure, ...). The prefix is prepended to the topic path.
    'mqtt_topic_prefix': '/sensors',
}

