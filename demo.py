from ud4d.detector import UDevDetector, UEvent
from ud4d.logger import logger


if __name__ == '__main__':
    UDevDetector.start()
    logger.info('udev started')

    first_event = UDevDetector.read_event()
    logger.info(first_event)
    logger.info(UEvent(first_event).ACTION)

    UDevDetector.stop()
    logger.info('udev stopped')
