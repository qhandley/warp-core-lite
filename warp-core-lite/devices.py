from gpiozero import DigitalInputDevice, DigitalOutputDevice
from smbus2 import SMBus

def dout_init(config):
    pin = config['pin']
    active_high = config['active_high']
    initial_value = config['initial_value']
    return DigitalOutputDevice(pin, active_high, initial_value)


def din_init(config):
    pin = config['pin']
    pull_up = config['pull_up']
    return DigitalInputDevice(pin, pull_up)


def i2c_init(config):
    channel = config['channel']
    return SMBus(channel)


class BurnWire():
    def __init__(self, config, core_init):
        self.core = core_init(config)

    def access(self, command, payload=None):
        pass
        #TODO

    def read(self):
        pass

    def write(self, value=None):
        pass

    def __repr__(self):
        return f"<devices.{self.__class__.__name__} object>"
    

class Igniter():
    def __init__(self, config, core_init):
        self.core = core_init(config)

    def access(self, command, payload=None):
        pass
        #TODO

    def read(self):
        pass

    def write(self, value=None):
        pass

    def __repr__(self):
        return f"<devices.{self.__class__.__name__} object>"


class DelugePump():
    def __init__(self, config, core_init):
        self.core = core_init(config)

    def access(self, command, payload=None):
        pass
        #TODO

    def read(self):
        pass

    def write(self, value=None):
        pass

    def __repr__(self):
        return f"<devices.{self.__class__.__name__} object>"


class MainOxValve():
    def __init__(self, config, core_init):
        self.core = core_init(config)

    def access(self, command, payload=None):
        pass
        #TODO

    def read(self):
        return self.core.value()

    def write(self, value=None):
        pass

    def __repr__(self):
        return f"<devices.{self.__class__.__name__} object>"


class MotorPressure():
    def __init__(self, config, core_init):
        self.addr = config['address']
        self.core = core_init(config)

    def access(self, command, payload=None):
        pass
        #TODO

    def read(self):
        pass

    def write(self, value=None):
        pass

    def __repr__(self):
        return f"<devices.{self.__class__.__name__} object>"
