import os
import time
import logging
import argparse
import gpiozero

import pyfiglet
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import confirm

import devices

BANNER = pyfiglet.figlet_format('Warp-Core Lite', font = 'slant') 
VERSION = '1.0.0'

DEFAULT_CONFIG_NAME = 'defconfig.yml'

log = logging.getLogger(__name__)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def parse_args():
    desc = 'OSU Hybrid Rocket test and launch application.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-c', '--config-path', dest='path', metavar='PATH', help='Path to load config file instead of default')
    parser.add_argument('-d', '--disable-logging', dest='disable_log', action='store_true', help='Disable logging')
    parser.add_argument('-t', '--test-id', dest='test_id', metavar='ID', help='Unique test ID to prefix log files (overriden by -d flag)')
    
    return parser.parse_args()

def run():
    print(BANNER)
    print('Version ' + VERSION)

    args = parse_args()
    #configure_logger(args.disable_log)

    if args.path != None:
        config_path = args.path
    else:
        config_path = DEFAULT_CONFIG_NAME
        
    print(bcolors.OKBLUE + 'Loading configuration file ' + config_path + '...' + bcolors.ENDC)

    rocket = devices.configure(config_path)

    print('Loaded device IDs:') 
    for device_id, device_obj in rocket.items():
        print(device_id) 
        print(device_obj)

    print('Burn Wire status:')
    print(rocket['BNW'].is_active)

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

if __name__ == "__main__":
    run()
