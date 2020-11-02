from prompt_toolkit.shortcuts import confirm

def status():
    '''Print status information.'''

    print("Temp status")
    #TODO

def launch():
    '''Initiate launch sequence.'''

    if(confirm('Confirm launch sequence.')):
        print('Launching...')
    else:
        print('Launch aborted.')
    #TODO
