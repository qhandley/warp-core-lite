import logging
import yaml
from abc import ABC, abstractmethod 
from gpiozero import (
        DigitalInputDevice, 
        DigitalOutputDevice,
        )
from smbus2 import SMBus

class IDevice(ABC):
    '''Base class interface for io devices.'''
    def __init__(self, name, id_, info):
        self.name = name
        self.id = id_
        self.info = info
        self.core = None

    def __repr__(self):
        return f"<drivers.{self.__class__.__name__} object>"

    @abstractmethod
    def activate(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass


class Valve(IDevice):
    def __init__(self, name, id_, info):
        super().__init__(name, id_, info)

    def activate(self, core):
        self.core = core

    def read(self):
        print('valve read')
        val = self.core.value
        print(val)

    def write(self):
        print('valve write')
        print('on')
        self.core.on()

    def __repr__(self):
        return f"<drivers.{self.__class__.__name__} object>"


class Igniter(IDevice):
    def __init__(self, name, id_, info):
        super().__init__(name, id_, info)

    def activate(self, core):
        self.core = core

    def read(self):
        print('valve read')

    def write(self):
        print('valve write')

    def __repr__(self):
        return f"<drivers.{self.__class__.__name__} object>"


def pull_end_devices(end_device_key, end_device_dict, io_type):
    end_device_list = []
    if end_device_key in end_device_dict:
        end_device_list = end_device_dict[end_device_key]
    else:
        log.warning('No %s %s devices were discovered.', end_device_key, io_type)

    return end_device_list


def configure_digital_inputs(configured_devices, input_devices):
    digital_inputs = pull_end_devices('digital', input_devices, 'input')

    for gpio in digital_inputs:
        try:
            configured_devices[gpio['id']] = DigitalInputDevice(gpio['pin'], gpio['pull-up'])
        except gpiozero.GPIOPinInUse:
            log.error('Pin %s is already in use and cannot be assigned to %s!', gpio['pin'], gpio['name'])


def configure_digital_outputs(configured_devices, output_devices):
    digital_outputs = pull_end_devices('digital', output_devices, 'output')

    for gpio in digital_outputs:
        try:
            configured_devices[gpio['id']] = DigitalOutputDevice(gpio['pin'])
        except gpiozero.GPIOPinInUse:
            log.error('Pin %s is already in use and cannot be assigned to %s!', gpio['pin'], gpio['name'])


def configure_i2c_inputs(configured_devices, input_devices):
    i2c_inputs = pull_end_devices('i2c', input_devices, 'input')

    #Add i2c configuration later


def load_config(config_file):
    config = {}
    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError:
            log.error('Configuration file %s could not be found.', config_file)
            print(yaml.YAMLError)

    return config


def configure(config_file):
    config = load_config(config_file)
    configured_devices = {}

    all_devices = config['devices']
    input_devices = all_devices['input']
    output_devices = all_devices['output']

    configure_digital_inputs(configured_devices, input_devices)
    configure_digital_outputs(configured_devices, output_devices)
    #configure_i2c_inputs(configured_devices, input_devices)

    return configured_devices
