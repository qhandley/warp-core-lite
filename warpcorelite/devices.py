from gpiozero import DigitalInputDevice, DigitalOutputDevice
from smbus2 import SMBus

enable_keywords = ('enable', 'on', '1', 'high')
disable_keywords = ('disable', 'off', '0', 'low')

class DigitalOutputDriver(object):
    def __init__(self, config):
        pin = config['pin']
        active_high = config['active_high']
        initial_value = config['initial_value']
        self.core = DigitalOutputDevice(pin, active_high, initial_value)

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
        pin = config['pin']
        pull_up = config['pull_up']
        self.core = DigitalInputDevice(pin, pull_up)

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
        channel = config['channel']
        self.addr = config['address']
        self.core = SMBus(channel)

    def access(self, command, payload=None):
        #TODO
        pass

    def _read(self):
        #TODO
        pass 

    def _write(self, value=None):
        #TODO
        pass

    def __repr__(self):
        return f"<devices.{self.__class__.__name__} object>"


class BurnWire(DigitalInputDriver):
    def __init__(self, config, id, info):
        self.id = id
        self.info = info
        super().__init__(config)


class Igniter(DigitalOutputDriver):
    def __init__(self, config, id, info):
        self.id = id
        self.info = info
        super().__init__(config)


class DelugePump(DigitalOutputDriver):
    def __init__(self, config, id, info):
        self.id = id
        self.info = info
        super().__init__(config)


class MainOxValve(DigitalOutputDriver):
    def __init__(self, config, id, info):
        self.id = id
        self.info = info
        super().__init__(config)


class MotorPressure(I2CDriver):
    def __init__(self, config, id, info):
        self.id = id
        self.info = info
        super().__init__(config)
