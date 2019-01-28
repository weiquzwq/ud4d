from ud4d.detector import UDevDetector
from ud4d.logger import logger


if __name__ == '__main__':
    UDevDetector.start()
    logger.info('udev started')

    UDevDetector.read_line()

    UDevDetector.stop()
    logger.info('udev stopped')
