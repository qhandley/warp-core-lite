from interface import implements, Interface
from gpiozero import (
        DigitalInputDevice, 
        DigitalOutputDevice,
        )
from smbus2 import SMBus

class DeviceInterface(Interface):
    def read(self):
        pass

    def write(self, value=None):
        pass


class BurnWire(implements(DeviceInterface)):
    def __init__(self, name, id_, info, type_, config=None):
        self.name = name
        self.id = id_
        self.info = info
        self.type = type_

    def read(self):
        pass

    def write(self, value=None):
        pass
    

class Igniter(implements(DeviceInterface)):
    def __init__(self, name, id_, info, type_, config=None):
        self.name = name
        self.id = id_
        self.info = info
        self.type = type_

    def read(self):
        pass

    def write(self, value=None):
        pass


class DelugePump(implements(DeviceInterface)):
    def __init__(self, name, id_, info, type_, config=None):
        self.name = name
        self.id = id_
        self.info = info
        self.type = type_

    def read(self):
        pass

    def write(self, value=None):
        pass


class MainOxValve(implements(DeviceInterface)):
    def __init__(self, name, id_, info, type_, config=None):
        self.name = name
        self.id = id_
        self.info = info
        self.type = type_
        if config:
            dev_pin = config.get('pin')
            dev_active_high = config.get('active_high')
            dev_initial_value = config.get('initial_value')
            self.core = DigitalOutputDevice(dev_pin, dev_active_high, dev_initial_value)

    def read(self):
        return self.core.value()

    def write(self, value=None):
        if value == 'open':
            self.core.on()
        elif value == 'close':
            self.core.off()

    def __repr__(self):
        return f"<devices.{self.__class__.__name__} object>"


class MotorPressure(implements(DeviceInterface)):
    def __init__(self, name, id_, info, type_, config=None):
        self.name = name
        self.id = id_
        self.info = info
        self.type = type_

    def read(self):
        pass

    def write(self, value=None):
        pass
