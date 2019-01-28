import subprocess
import time

from ud4d import config as u_config
from ud4d.logger import logger


class UDevDetector(object):
    """ udevadm process management """
    _process = None

    @classmethod
    def start(cls):
        cls._process = subprocess.Popen(
            [u_config.UDEVADM_PATH, 'monitor', '-u', '--subsystem-match=usb', '--environment'],
            stdout=subprocess.PIPE,
        )
        time.sleep(1)
        assert cls.is_running(), 'udevadm not running'
        logger.info('udevadm process up')

        # ignore unused header
        cls.read_event()

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

    @classmethod
    def read_event(cls) -> list:
        event_content = []
        new_line = cls.read_line().strip()
        while new_line:
            event_content.append(new_line)
            new_line = cls.read_line().strip()
        return event_content


class UEvent(object):
    """ convert udev info (str) into object """
    def __init__(self, udev_info_list):
        for each_arg in udev_info_list[1:]:
            name, value = each_arg.split('=')
            self.__dict__[name] = value

    def is_android(self) -> bool:
        return 'ID_SERIAL_SHORT' in self.__dict__

    def get_serial_no(self) -> str:
        assert self.is_android(), 'device not android'
        return self.ID_SERIAL_SHORT

    def get_dev_name(self) -> str:
        if hasattr(self, 'DEVNAME'):
            return self.DEVNAME
        logger.info('no device name found, return device path instand')
        return self.DEVPATH

    def get_event_id(self) -> str:
        return self.USEC_INITIALIZED

    def get_action_name(self) -> str:
        return self.ACTION


class UEventManager(object):
    """ manage events about android, ignore everything else """
    _event_dict = dict()

    @classmethod
    def add_event(cls, uevent: UEvent):
        event_id = uevent.get_event_id()
        action = uevent.get_action_name()

        # only 'bind' and 'unbind'
        if action == 'bind':
            cls._event_dict[event_id] = uevent
            logger.info('event id [%s] added', event_id)
        elif action == 'unbind' and event_id in cls._event_dict:
            del cls._event_dict[event_id]
            logger.info('event id [%s] ended', event_id)
        else:
            # ignore other events
            pass

    @classmethod
    def get_event_dict(cls):
        return cls._event_dict
