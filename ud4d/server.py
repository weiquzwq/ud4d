from flask import Flask, request
from ud4d.docker_manager import DeviceContainerManager


app = Flask(__name__)


@app.route('/')
def welcome():
    return 'Welcome to ud4d :)'


@app.route('/api/device')
def device():
    """ serial_no -> device_name
    
    eg: 
    REQUEST GET: http://127.0.0.1:9410/api/device?serial_no=123456F
    SUCCESS RESPONSE: /dev/bus/usb/001/010
    NOT FOUND RESPONSE: null
    """
    serial_no = request.args.get('serial_no')
    return DeviceContainerManager.query(serial_no)
