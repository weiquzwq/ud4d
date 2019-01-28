import contextlib
import threading

from ud4d.detector import UDevDetector
from ud4d.docker_manager import DeviceContainerManager
from ud4d.logger import logger
from ud4d.event import UEventManager, UEvent


UD4D_STATUS = False


@contextlib.contextmanager
def safe_ud4d():
    UDevDetector.start()
    logger.info('udev detector started')
    yield UDevDetector
    DeviceContainerManager.remove_all()
    logger.info('all device container removed')
    UDevDetector.stop()
    logger.info('udev detector stopped')


def start_ud4d():
    global UD4D_STATUS
    UD4D_STATUS = True

    def inner():
        UDevDetector.start()
        while UD4D_STATUS:
            first_event = UDevDetector.read_event()
            event_object = UEvent(first_event)
            UEventManager.add_event(event_object)
        UDevDetector.stop()

    threading.Thread(target=inner).start()


def stop_ud4d():
    global UD4D_STATUS
    UD4D_STATUS = False
