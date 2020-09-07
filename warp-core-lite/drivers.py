import os
import sys
import json
from devices import (
        BurnWire,
        Igniter,
        DelugePump,
        MainOxValve, 
        MotorPressure
        )

_SUPPORTED_DEVICE_TYPES = ('DIN', 'DOUT', 'I2C',)
_DEVICE_ID_LOOKUP_TABLE = {
        0: BurnWire,
        1: Igniter,
        2: DelugePump,
        3: MainOxValve,
        4: MotorPressure,
        }

class DeviceFactory(object):
    '''Factory for creating configured device objects.
   
    Devices are mapped by their unique ID's to their 
    respective class implementation and then configured.
    '''
    def __init__(self):
        self._dev_lookup = _DEVICE_ID_LOOKUP_TABLE

    def set_lookup_table(self, lookup):
        self._dev_lookup = lookup

    def get_dev_lookup(self, dev_id):
        device = self._dev_lookup.get(dev_id)
        if not device:
            raise ValueError(dev_id)
        return device

    def create_device(self, dev):
        dev_name = dev.get('name')
        dev_id = dev.get('id')
        dev_info = dev.get('info')
        dev_type = dev.get('type')
        dev_config = dev.get('config')

        device = self.get_dev_lookup(dev_id)
        return device(dev_name, dev_id, dev_info, dev_type, dev_config)


if __name__ == '__main__':
    devices = []
    factory = DeviceFactory(_DEVICE_ID_LOOKUP_TABLE)

    with open('defconfig.json', 'r') as conf:
        defconfig = json.load(conf)
    device_list = defconfig['io_device_list']

    for device in device_list:
       devices.append(factory.create_device(device))
