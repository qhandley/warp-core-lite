from gpiozero import DigitalInputDevice, DigitalOutputDevice
from smbus2 import SMBus

enable_keywords = ('enable', 'on', '1', 'high')
disable_keywords = ('disable', 'off', '0', 'off')

class DigitalOutputDriver(object):
    def __init__(self, config):
        self.core = self.dout_init(config)

    def dout_init(self, config):
        pin = config['pin']
        active_high = config['active_high']
        initial_value = config['initial_value']
        return DigitalOutputDevice(pin, active_high, initial_value)

    def access(self, command, payload=None):
        if command == 'read':
            return self._read()
        elif command == 'write':
            return self._write(payload)
        else:
            return None

    def _read(self):
        return self.core.value

    def _write(self, value=None):
        if value in enable_keywords:
            self.core.on()
        elif value in disable_keywords:
            self.core.off()
        return value

    def __repr__(self):
        return f"<devices.{self.__class__.__name__} object>"


class DigitalInputDriver(object):
    def __init__(self, config):
        self.core = self.din_init(config)

    def din_init(self, config):
        pin = config['pin']
        pull_up = config['pull_up']
        return DigitalInputDevice(pin, pull_up)

    def access(self, command, payload=None):
        if command == 'read':
            return self._read()
        else:
            return None

    def _read(self):
        return self.core.value

    def __repr__(self):
        return f"<devices.{self.__class__.__name__} object>"


class I2CDriver(object):
    def __init__(self, config):
        self.core = self.i2c_init(config)

    def i2c_init(self, config):
        channel = config['channel']
        return SMBus(channel)

    def access(self, command, payload=None):
        pass

    def _read(self):
        pass 

    def _write(self, value=None):
        pass

    def __repr__(self):
        return f"<devices.{self.__class__.__name__} object>"


class BurnWire(DigitalInputDriver):
    pass


class Igniter(DigitalOutputDriver):
    pass


class DelugePump(DigitalOutputDriver):
    pass


class MainOxValve(DigitalOutputDriver):
    pass


class MotorPressure(I2CDriver):
    def __init__(self, config):
        self.addr = config['address']
        super().__init__(config)
