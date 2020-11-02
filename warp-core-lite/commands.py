def warp_open(args, devices):
    ''' '''
    if args.device == 'VLV1':
        print(f"Opening VLV1")
        vlv1 = devices.get('VLV1')
        vlv1.write('open')

    if args.device == 'VLV2':
        print(f"Opening VLV2")


def warp_close(args, devices):
    ''' '''
    pass


def warp_status(args, devices):
    ''' '''
    pass


def warp_launch(args, devices):
    ''' '''
    if(confirm('Confirm launch initiation.')):
        print('Launching...')
    else:
        print('Launch aborted.')
