import json

from devices import (
    BurnWire, 
    Igniter, 
    DelugePump, 
    MainOxValve, 
    MotorPressure
    )

class_helpers = {
    'BRN': BurnWire,
    'IGN': Igniter,
    'DLG': DelugePump,
    'VLV1': MainOxValve,
    'P1': MotorPressure,
    }

class DeviceFactory(object):
    '''Factory for creating dict of device objects from device list.'''

    def __init__(self):
        self.class_helpers = class_helpers

    def build(self, device_list):
        def get(device, key):
            value = None
            if key in device:
                value = device[key]
            return value

        devices = {}
        for device in device_list:
            name = get(device, 'name')
            id = get(device, 'id')
            info = get(device, 'info')
            config = get(device, 'config')
            if name not in devices.keys():
                if name in self.class_helpers.keys():
                    devices[name] = self.class_helpers[name](config, id, info)
                else:
                    print(f'Device {name} does not exist.')
            else:
                print(f'Device {name} already exists.')

        return devices
