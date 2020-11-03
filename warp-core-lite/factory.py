import json

from gpiozero import DigitalInputDevice, DigitalOutputDevice
from smbus2 import SMBus

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
    '''Factory for creating device objects from device list.

    Devices are mapped to their respective class helper
    and core I/O implementation.
    '''
    def __init__(self, device_list):
        self.device_list = device_list
        self.class_helpers = class_helpers

    def build(self):
        def get(device, key):
            value = None
            if key in device:
                value = device[key]
            return value

        devices = {}
        for device in self.device_list:
            name = get(device, 'name')
            config = get(device, 'config')
            devices[name] = self.class_helpers[name](config)

        return devices
