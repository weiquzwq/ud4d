import subprocess


# check: udevadm is runnable?
assert not subprocess.check_call(['udevadm', '--version']), 'udevadm started failed. Is your system linux?'

# encoding
CHARSET = 'utf-8'

# udevadm path
UDEVADM_PATH = subprocess.check_output(['which', 'udevadm']).decode(CHARSET).strip()

# default device image
DEVICE_IMAGE_NAME = 'williamfzc/adb_tester:0.1'

# default server port
DEFAULT_SERVER_PORT = 9410

# simple mode will not create container
SIMPLE_MODE = True
