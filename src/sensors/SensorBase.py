'''
Created on Mar 8, 2015

@author: andreas
'''

import logging
import json
from datetime import datetime


class SensorError(Exception):
    '''Base class for all kind of errors related to accessing a sensor.'''
    pass


class ChecksumError(SensorError):
    '''Checksum mismatch error.'''
    pass


def evt_from_json(jsonstr):
    data = json.loads(jsonstr)

    return SensorEvent(**data)


class SensorEvent():
    def __init__(self, sensorname, value, unit, quantity):
        self._sensorname = sensorname
        self._value = value
        self._unit = unit
        self._quantity = quantity

        self._timestamp = datetime.utcnow()
    
    
    def getValue(self):
        return self._value
 
    
    def getUnit(self):
        return self._unit
    
    
    def getQuantity(self):
        return self._quantity
    
    
    def getTimestamp(self):
        return self._timestamp


    def getSensorName(self):
        return self._sensorname

    
    def __str__(self):
        '''Convert the event to a string representation.'''

        fmt = '{s} {q} = {v} {u}'
        return fmt.format(
            s=self._sensorname,
            q=self._quantity, 
            v=self._value, 
            u=self._unit)


    def toJSON(self):
    
        value = {
            'timestamp': self.getTimestamp().isoformat(),
            'sensor_name': self.getSensorName(),
            'quantity': self.getQuantity(),
            'unit': self.getUnit(),
            'value': self.getValue(),
        }
    
        return json.dumps(value, sort_keys=True, indent=4)


class SensorBase(object):
    def __init__(self, sensor_name):
        
        self._sensor_name = sensor_name
        self._description = ''
        
        # set up a logger
        self._logger = logging.getLogger(
            "Sensor_'{0}'".format(
                sensor_name))
                
    def getName(self):
        return self._sensor_name
    
    def getDescription(self):
        return self._description
    
    def setDescription(self):
        self._description = ''
        
    def __str__(self):
        return "Sensor_{0}".format(
            self._sensor_name)
        
    def sampleValues(self):
        pass
        

        
class I2CSensorBase(SensorBase):
    def __init__(self, sensor_name, bus, address):
        
        SensorBase.__init__(self, sensor_name)
        
        assert(bus is not None)
        
        self._address = address
        self._bus = bus
