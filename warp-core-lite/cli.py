import os
import sys
import logging
import argparse
import json

import pyfiglet
import bcolors as b
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import confirm

import drivers

_BANNER = pyfiglet.figlet_format('Warp-Core Lite', font = 'slant') 
_VERSION = '1.0.0'
_DEFAULT_CONFIG_NAME = 'configs/defconfig.json'

log = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser(
            description='OSU Hybrid Rocket test and launch application.')

    parser.add_argument('-f', '--file', dest='config_file', metavar='PATH',
            help='path to load config file instead of default')
    parser.add_argument('-d', '--disable-logging', dest='disable_logging',
            action='store_true', help='disable logging')
    parser.add_argument('-t', '--test-id', dest='test_id', metavar='ID',
            help='unique test ID to prefix log files (overriden by -d flag)')
    parser.add_argument('--version', action='version', version=_VERSION)
    
    return parser.parse_args()

def run_interactive():
    parser = argparse.ArgumentParser(prog='')
    subparsers = parser.add_subparsers(help='sub-command help', dest='sub_cmd')

    open_valve_parser = subparsers.add_parser('open', help='open valve sub-command')
    open_valve_parser.add_argument('valve', choices=['VLV1', 'VLV2'], 
            help='Select a valve to open')

    close_valve_parser = subparsers.add_parser('close', help='close valve sub-command')
    close_valve_parser.add_argument('valve', choices=['VLV1', 'VLV2'],
            help='Select a valve to close')

    status_parser = subparsers.add_parser('status', help='status sub-command')
    launch_parser = subparsers.add_parser('launch', help='launch sub-command')

    session = PromptSession()

    while True:
        try:
            response = session.prompt('> ')
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        if response == '' or response.isspace():
            continue

        try:
            args = parser.parse_args(response.split())
        except SystemExit:
            continue

        if args.sub_cmd == 'open':
            print('open')

        if args.sub_cmd == 'close':
            print('close')

        if args.sub_cmd == 'status':
            print('status')

        if args.sub_cmd == 'launch':
            if(confirm('confirm launch initiation.')):
                print('starting launch sequence...')
            else:
                print('cancelling launch sequence...')

    print('Ending session...')

def run():
    args = parse_args()
    factory = drivers.DeviceFactory()
    devices = []

    if args.disable_logging:
        pass 

    if args.test_id:
        pass

    if args.config_file:
        config_path = args.config_file
    else:
        config_path = _DEFAULT_CONFIG_NAME
        
    print(b.WAITMSG + 'Loading configuration file: ' + config_path + b.END)
    with open(config_path, 'r') as conf:
        defconfig = json.load(conf)
    device_list = defconfig.get('io_device_list')

    for device in device_list:
        devices.append(factory.create_device(device))

    print(b.WAITMSG + 'Devices loaded.' + b.END)

    run_interactive()
    return 0

if __name__ == "__main__":
    sys.exit(run())
