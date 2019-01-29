import subprocess


# check: udevadm is runnable?
assert not subprocess.check_call(['udevadm', '--version']), 'udevadm started failed. Is your system linux?'

CHARSET = 'utf-8'
UDEVADM_PATH = subprocess.check_output(['which', 'udevadm']).decode(CHARSET).strip()
DEVICE_IMAGE_NAME = 'williamfzc/adb_tester:0.1'
DEFAULT_SERVER_PORT = 9410
