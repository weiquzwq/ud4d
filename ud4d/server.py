from flask import Flask, request
from ud4d.docker_manager import DeviceContainerManager


app = Flask(__name__)


@app.route('/')
def welcome():
    return 'Welcome to ud4d :)'


@app.route('/api/device')
def device():
    serial_no = request.args.get('serial_no')
    return DeviceContainerManager.query(serial_no)
