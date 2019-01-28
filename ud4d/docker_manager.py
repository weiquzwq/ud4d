import docker

from ud4d import config as u_config
from ud4d.logger import logger


# device image name
device_image_name = u_config.DEVICE_IMAGE_NAME
logger.info('device image name: %s', device_image_name)

# docker client
client = docker.from_env()

# check
try:
    device_image = client.images.get(device_image_name)
except docker.errors.ImageNotFound as e:
    logger.error('device image not found: %s, you should build it first', device_image_name)
    raise e


class DeviceContainer(object):
    """ android device container object """
    def __init__(self, serial_no, device_name):
        self.serial_no = serial_no
        self.device_name = device_name
        self.container = client.containers.run(
            device_image,
            detach=True,
            # container name
            name='android_device_' + serial_no,
            # bind devices
            devices=['{}:{}:rwm'.format(device_name, device_name)],
            # keep it running
            tty=True,
        )


class DeviceContainerManager(object):
    _container_dict = dict()

    @classmethod
    def add(cls, device_container: DeviceContainer):
        cls._container_dict[device_container.serial_no] = device_container
        logger.info('device container [%s] running', device_container.serial_no)

    @classmethod
    def remove(cls, serial_no):
        if serial_no in cls._container_dict:
            cls._container_dict[serial_no].container.remove(force=True)
            del cls._container_dict[serial_no]
            logger.info('device container [%s] removed', serial_no)
        else:
            logger.warn('device container [%s] not existed', serial_no)

    @classmethod
    def remove_all(cls):
        """ remove all containers """
        for each_serial_no in cls._container_dict:
            cls.remove(each_serial_no)
