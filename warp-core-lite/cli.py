import os
import time
import logging
import argparse
import gpiozero

import pyfiglet
from prompt_toolkit import PromptSession
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

def run_prompt():
    session = PromptSession()

    while True:
        try:
            response = session.prompt('> ')
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        else:
            tokens = response.split()

            if tokens[0] == 'help':
                print('Print out commands and options.')

            elif tokens[0] == 'list':
                print('Pretty print configured devices and their current state.')

            elif tokens[0] == 'toggle':
                print('Toggle configured output devices.')

            elif tokens[0] == 'launch':
                if(confirm('Confirm launch initiation.')):
                    print('Starting launch sequence...')
                else:
                    print('Cancelling launch sequence...')

            else:
                print('Invalid response: {}'.format(response))

    print('Ending session...')

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
    run_prompt()

if __name__ == "__main__":
    run()
