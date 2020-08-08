import logging
import yaml
import gpiozero

log = logging.getLogger(__name__)

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
            configured_devices[gpio['id']] = gpiozero.DigitalInputDevice(gpio['pin'], gpio['pull-up'])
        except gpiozero.GPIOPinInUse:
            log.error('Pin %s is already in use and cannot be assigned to %s!', gpio['pin'], gpio['name'])

def configure_digital_outputs(configured_devices, output_devices):
    digital_outputs = pull_end_devices('digital', output_devices, 'output')

    for gpio in digital_outputs:
        try:
            configured_devices[gpio['id']] = gpiozero.DigitalOutputDevice(gpio['pin'])
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
