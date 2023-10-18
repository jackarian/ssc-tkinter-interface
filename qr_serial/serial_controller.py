import threading
from pathlib import Path

import yaml
from serial.threaded import ReaderThread, Protocol
import serial
from qrcode.qr_interface import QrCodeReader
from rest.restclient import SscClient


class SerialReaderProtocolRaw(Protocol):
    listener: SscClient = None
    buffer = []

    def connection_made(self, transport):
        """Called when reader thread is started"""
        print("Connected, ready to receive data...")

    def data_received(self, data):
        """Called with snippets received from the serial port"""

        try:
            c = str(data.decode('utf-8'))
            self.buffer.append(c)
            #   print(data)
            if data == b'\n':
                # print("Find end message")
                # print(self.buffer)
                payload = ''.join(v for v in self.buffer)
                print(payload)
                self.listener.sendPayload(payload.rstrip('\r\n'))
                # print(self.buffer)

                self.buffer = []

        except Exception as e:
            print(e)


class QrCodeSerialController(QrCodeReader):
    def __init__(self, label=None, controller=None):
        self.controller: SscClient = controller
        self.reader: ReaderThread = None
        self._configureFromFile()
        self.serial: serial.Serial = serial.Serial(
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            port='/dev/ttyUSB0',
            timeout=None
        )
        self.thread = None
        self.stopEvent: threading.Event = None

    def _configureFromFile(self):
        home = str(Path.home())
        with open(r'' + home + '/config/usb.yaml') as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            self.config = yaml.load(file, Loader=yaml.FullLoader)
            for item, doc in self.config.items():
                print(item, ":", doc)

    def startCapture(self):
        # self.stopEvent = threading.Event()
        # self.thread = threading.Thread(target=self._readerLoop, args=[self.serial])
        # self.thread.start()
        # Initiate ReaderThread
        SerialReaderProtocolRaw.listener = self.controller
        print(self.serial)
        self.reader = ReaderThread(self.serial, SerialReaderProtocolRaw)
        # Start reader
        self.reader.start()

    def _readerLoop(self, serial):
        try:
            if not self.serial.is_open:
                serial.open()
            while not self.stopEvent.is_set():
                c = str(serial.read())
                print(c)
        except Exception as e:
            print("[INFO] caught a RuntimeError %s", e)

    def onClose(self):
        if self.reader is not None:
            self.reader.close()


if __name__ == '__main__':
    myserial = QrCodeSerialController()
    myserial.startCapture()
