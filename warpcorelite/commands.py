import threading
import time

from prompt_toolkit.shortcuts import confirm

import subscale

def status(devices):
    '''Print status information.'''

    for key in devices:
        dev_state = devices[key].access('read')
        print(f'{key}: {dev_state}')


def launch(devices):
    '''Initiate launch sequence.'''

    if(confirm('Confirm launch sequence.')):
        #t = threading.Thread(target=subscale.launch, args=(devices,)).start()
        #t.join()
        subscale.launch(devices)
    else:
        print('Launch aborted.')
