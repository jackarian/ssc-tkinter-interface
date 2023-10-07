from flask import Flask
# from mygpio import MyGpio
import json

server = Flask(__name__)


class Server:
    gpio = None

    def __init__(self, gpio):
        Server.gpio = gpio
        self.app = server

    def run(self):
        self.app.run(host='0.0.0.0')

    @staticmethod
    @server.route('/')
    def index():
        Server.gpio.print()
        return json.dumps({
            "operation": "door_opening",
            "status": "opened"
        })

