import sys
import time
from transitions import Machine
from transitions.extensions.states import add_state_features, Timeout

import devices

#Countdown to ignition (secs)
CNTDWN = 10
#Timeouts (secs)
IGN_TO = 10
S1_TO = 3
S2_TO = 6

@add_state_features(Timeout)
class CustomStateMachine(Machine):
    pass

class Rocket(object):
    def __init__(self, devices):
        self.devices = devices

    def precheck(self):
        # check correct devices are present
        if 'BRN' not in self.devices:
            print('BRN missing')
            return False 
        if 'IGN' not in self.devices:
            print('IGN missing')
            return False
        if 'VLV1' not in self.devices:
            print('VLV1 missing')
            return False

        # check BRN status
        if self.devices['BRN'].access('read') != 0:
            print('Error: burn wire open')
            return False
        return True

    def countdown(self, seconds=CNTDWN):
        print('Launching in:')
        while seconds > 0:
            print('T-' + str(seconds))
            time.sleep(1)
            seconds -= 1

    def enable_ign(self):
        print('starting ignition!')

    def disable_ign(self):
        print('disabling ignition!')

    def open_vlv(self):
        print('opening ox valve!')

    def close_vlv(self):
        print('closing ox valve!')

    def cleanup(self):
        print('Error: cleaning up')
        self.disable_ign()
        self.close_vlv()

#TODO: separate state configurations for readability
states = [
        {'name': 'staging', 'on_exit': 'countdown'},
        {'name': 'ignition', 'on_enter': 'enable_ign', 'on_exit': 'disable_ign', 'timeout': IGN_TO, 'on_timeout': 'ign_to'},
        {'name': 'stage_1', 'on_enter': 'open_vlv', 'timeout': S1_TO, 'on_timeout': 's1_to'},
        {'name': 'stage_2', 'on_exit': 'close_vlv', 'timeout': S2_TO, 'on_timeout': 's2_to'},
        {'name': 'post'},
        {'name': 'error', 'on_enter': 'cleanup'}
]

#all async transitions
transitions = [
        {'trigger': 'start_ign', 'source': 'staging', 'dest': 'ignition', 'conditions': 'precheck'},
        {'trigger': 'open_burnwire', 'source': 'ignition', 'dest': 'stage_1'},
        {'trigger': 'ign_to', 'source': 'ignition', 'dest': 'error'},
        {'trigger': 'nom_pressure', 'source': 'stage_1', 'dest': 'stage_2'},
        {'trigger': 's1_to', 'source': 'stage_1', 'dest': 'error'},
        {'trigger': 'done', 'source': 'stage_2', 'dest': 'post'},
        {'trigger': 's2_to', 'source': 'stage_2', 'dest': 'error'}
]

#TODO: handle transitions to error state
def launch(devices):
    rocket = Rocket(devices)
    machine = CustomStateMachine(model=rocket, states=states, transitions=transitions, initial='staging')

    print(rocket.state)

    rocket.start_ign()
    print(rocket.state)
    time.sleep(3)

    rocket.open_burnwire()
    print(rocket.state)
    time.sleep(2)

    rocket.nom_pressure()
    print(rocket.state)
    time.sleep(3)

    rocket.done()
    print(rocket.state)
