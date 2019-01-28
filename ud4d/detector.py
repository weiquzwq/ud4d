import subprocess
import time

from ud4d import config as u_config
from ud4d.logger import logger


class UDevDetector(object):
    _process = None

    @classmethod
    def start(cls):
        cls._process = subprocess.Popen(
            [u_config.UDEVADM_PATH, 'monitor', '-u', '--subsystem-match=usb', '--environment'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        time.sleep(1)
        assert cls.is_running(), 'udevadm not running'
        logger.info('udevadm process up')

    @classmethod
    def stop(cls):
        if cls._process and cls.is_running():
            cls._process.kill()
            cls._process = None
            logger.info('udevadm process down')
        else:
            logger.warn('udevadm process already down without killing')

    @classmethod
    def is_running(cls) -> bool:
        return not bool(cls._process.poll())

    @classmethod
    def read_line(cls) -> str:
        return cls._process.stdout.readline().decode(u_config.CHARSET)
