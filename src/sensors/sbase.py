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

    
    def fromJson(strdata):
        '''Convert a JSON string back to a SensorEvent instance.'''
        
        data = json.loads(strdata)

        return SensorEvent(
            sensorname=data['sensor_name'],
            value=data['value'],
            unit=data['unit'],
            quantity=data['quantity'])


class SensorBase(object):
    def __init__(self, scfg):
        self._sensor_name = scfg['sensor_name']
        self._description = scfg.get('description', '')

        self.scfg = scfg
        

    def getName(self):
        '''Returns the sensor name.'''

        return self.scfg['sensor_name']

    
    def getDescription(self):
        '''Returns the sensor description.'''

        return self.scfg['description']

    
    def __str__(self):
        '''Return a string describing the sensor.'''

        text = "Sensor '{0}' of type '{1}'"
        return text.format(
            self.getName(),
            self.__class__.__name__)
        

    def sample(self):
        '''Sample the sensor values for this instance. 

        This function needs to be overridden in subclasses to actually
        sample values.'''

        raise Exception('This function needs to be implemented in subclasses.')
        

    def new_event(self, value, unit, quantity):
        '''Create a new SensorEvent instance.'''

        return SensorEvent(self.getName(), value, unit, quantity)

        
class I2CSensorBase(SensorBase):
    def __init__(self, sensor_name, bus, address):
        
        SensorBase.__init__(self, sensor_name)
        
        assert(bus is not None)
        
        self._address = address
        self._bus = bus
