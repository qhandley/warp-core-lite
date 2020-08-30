import os
import sys
import json
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from smbus2 import SMBus

from devices import (Valve, Igniter)

_SUPPORTED_DEVICE_TYPES = ('DIN', 'DOUT', 'I2C',)
_DEVICE_ID_LOOKUP_TABLE = {
        0: Valve,
        1: Igniter
        }

class DigitalInputDeviceHandler(object):
    def __init__(self):
        self.id_lookup_table = id_lookup
        self.dev_cls = None
        self._is_configured = False

    def get_dev_cls(self, id_):
        cls = self.id_lookup_table.get(id_)
        if not cls:
            raise ValueError(id_)
        return cls

    def configure(self, dev):
        dev_id = dev.get('id')
        self.dev_cls = self.get_dev_cls(dev_id)

    def create(self, config, id_):
        _dev_cls = Valve
        pass


class DigitalOutputDeviceHandler(object):
    def __init__(self, id_lookup):
        self.id_lookup_table = id_lookup
        self.dev_config = None
        self.dev_cls = None
        self.dev = None
        self._is_configured = False

    def get_dev_cls(self, id_):
        cls = self.id_lookup_table.get(id_)
        if not cls:
            raise ValueError(id_)
        return cls

    def configure(self, dev):
        dev_name = dev.get('name')
        dev_id = dev.get('id')
        dev_info = dev.get('info')
        self.dev_cls = self.get_dev_cls(dev_id)
        self.dev_config = dev.get('config')
        self.dev = self.dev_cls(dev_name, dev_id, dev_info)
        self._is_configured = True

    def create(self):
        dev_pin = self.dev_config.get('pin')
        dev_active_high = self.dev_config.get('active_high')
        dev_initial_val = False if self.dev_config.get('initial_value') == 'low' else True
        core_obj = DigitalOutputDevice(dev_pin, dev_active_high, dev_initial_val)
        self.dev.activate(core_obj)
        return self.dev  

class DeviceFactory(object):
    ''' '''
    def __init__(self, dev_handlers=None):
        if dev_handlers:
            self._dev_handlers = dev_handlers
        else:
            self._dev_handlers = {}

    def register_dev_type(self, type_, handler):
        self._dev_handlers[type_] = handler

    def get_dev_handler(self, type_):
        handler = self._dev_handlers.get(type_)
        if not handler:
            raise ValueError(type_)
        return handler

    def create_dev(self, dev):
        dev_type = dev.get('io_type')
        handler_cls = self.get_dev_handler(dev_type)
        handler = handler_cls(_DEVICE_ID_LOOKUP_TABLE) 
        handler.configure(dev)
        return handler.create()


if __name__ == '__main__':
    factory = DeviceFactory()
    factory.register_dev_type('DOUT', DigitalOutputDeviceHandler) 

    with open('defconfig.json', 'r') as conf:
        defconfig = json.load(conf)

    device_list = defconfig['io_device_list']

    valve = factory.create_dev(device_list[3])
    valve.read()
    valve.write()
    valve.read()

