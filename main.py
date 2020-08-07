import os
import time
import logging
import argparse
import gpiozero

import yaml
import pyfiglet
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import confirm

banner = pyfiglet.figlet_format('Warp-Core Lite', font = 'slant') 
version = '1.0.0'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def pull_end_devices(end_device_key, end_device_dict, io_type):
    end_device_list = []
    if end_device_key in end_device_dict:
        end_device_list = end_device_dict[end_device_key]
    else:
        logging.warning('No %s %s devices were discovered.', end_device_key, io_type)

    return end_device_list

def configure_digital_inputs(configured_devices, input_devices):
    digital_inputs = pull_end_devices('digital', input_devices, 'input')

    for gpio in digital_inputs:
        try:
            configured_devices[gpio['id']] = gpiozero.DigitalInputDevice(gpio['pin'])
        except gpiozero.GPIOPinInUse:
            logging.error('Pin %s is already in use and cannot be assigned to %s!', gpio['pin'], gpio['name'])

def configure_digital_outputs(configured_devices, output_devices):
    digital_outputs = pull_end_devices('digital', output_devices, 'output')

    for gpio in digital_outputs:
        try:
            configured_devices[gpio['id']] = gpiozero.DigitalOutputDevice(gpio['pin'])
        except gpiozero.GPIOPinInUse:
            logging.error('Pin %s is already in use and cannot be assigned to %s!', gpio['pin'], gpio['name'])

def configure_i2c_inputs(configured_devices, input_devices):
    i2c_inputs = pull_end_devices('i2c', input_devices, 'input')

    #Add i2c configuration later

def configure_devices(config, configured_devices):
    all_devices = config['devices']
    input_devices = all_devices['input']
    output_devices = all_devices['output']

    configure_digital_inputs(configured_devices, input_devices)
    configure_digital_outputs(configured_devices, output_devices)
    #configure_i2c_inputs(configured_devices, input_devices)

def load_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError:
            logging.error('Configuration file %s could not be found.', config_file)
            print(yaml.YAMLError)

    return config

if __name__ == '__main__':
    print(banner)
    print('Version ' + version)

    target_config_path = os.path.join(os.getcwd(), 'config.yaml')

    #Load and parse cmd args, if any

    print(bcolors.OKBLUE + 'Loading configuration file ' + target_config_path 
            + '...' + bcolors.ENDC)

    devices = {}
    configure_devices(load_config(target_config_path), devices)

    print(devices)

'''
    answer = prompt('> ')
    if answer == 'launch':
        if(confirm('Confirm launch initiation. (y/n)')):
            print('Weeeee!!')
        else:
            print('Loser')
    else:
        print('You said: %s' % answer)
    
'''
