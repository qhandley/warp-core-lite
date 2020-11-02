import argparse
import json
import logging
import os
import sys

import bcolors as b
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import confirm
import pyfiglet

from factory import DeviceFactory

_BANNER = pyfiglet.figlet_format('Warp-Core Lite', font = 'slant') 
_VERSION = '1.0.0'
_DEFAULT_CONFIG_NAME = '../defconfig.json'

devices = {}

log = logging.getLogger(__name__)


def parse_args():
    '''Parse command-line arguments.'''

    parser = argparse.ArgumentParser(
            description='OSU Hybrid Rocket test and launch application.')
    parser.add_argument('-f', '--file', dest='config_file', metavar='PATH',
            help='path to load config file instead of default')
    parser.add_argument('-d', '--disable-logging', dest='disable_logging',
            action='store_true', help='disable logging')
    parser.add_argument('--launch-id', dest='launch_id', metavar='ID',
            help='unique launch ID to prefix log files (overriden by -d flag)')
    parser.add_argument('-s', '--server', dest='port', metavar='PORT',
            help='run as server in non-interactive mode')
    parser.add_argument('--version', action='version', version=_VERSION)
    
    return parser.parse_args()


def run_interactive(launch_id):
    '''
    Flow:
    1. Setup interactive command parser and session prompt
    2. Prompt user for input
    3. Parse user input
    4. Execute subparser's control function
    5. Loop from step 2
    '''

    parser = argparse.ArgumentParser(prog='')
    subparsers = parser.add_subparsers(help='sub-command help', dest='sub_cmd')

    open_parser = subparsers.add_parser('open', help='open valve')
    open_parser.add_argument('device', choices=['VLV1', 'VLV2'], 
            help='Select a device to open')
    open_parser.set_defaults(func=commands.warp_open)

    close_parser = subparsers.add_parser('close', help='close valve')
    close_parser.add_argument('device', choices=['VLV1', 'VLV2'],
            help='Select a device to close')
    close_parser.set_defaults(func=commands.warp_close)

    status_parser = subparsers.add_parser('status', help='print status information')
    status_parser.set_defaults(func=commands.warp_status)

    launch_parser = subparsers.add_parser('launch', help='commence launch (with confirmation)')
    launch_parser.set_defaults(func=commands.warp_launch)

    session = PromptSession()
    prompt = f"({launch_id})> "

    while True:
        try:
            response = session.prompt(prompt)
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

        try: 
            args.func(args, devices)
        except:
            print('function does not exist')

    print('Ending session...')


def run():
    '''Run program either in interactive mode (default) or as server.'''

    args = parse_args()

    if args.disable_logging:
        # TODO
        pass 

    if args.launch_id:
        launch_id = args.launch_id
    else:
        launch_id = 0x0

    if args.config_file:
        config_path = args.config_file
    else:
        config_path = _DEFAULT_CONFIG_NAME

    print(b.WAITMSG + 'Loading configuration file: ' + config_path + b.END)

    with open(config_path) as f:
        config = json.load(f)

    factory = DeviceFactory(config['DeviceList'])
    devices = factory.build()

    print(b.OK + 'Devices loaded.' + b.END)

    if args.port:
        # TODO
        pass
    else:
        run_interactive(launch_id)
        pass


if __name__ == "__main__":
    sys.exit(run())
