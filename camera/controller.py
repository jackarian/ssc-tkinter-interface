import threading
from time import sleep

# import adafruit_vl53l0x
import board
# import busio
import cv2 as cv
from pyzbar import pyzbar
import numpy as np

from qrcode.qr_interface import QrCodeReader
from picamera2 import Picamera2
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory

from rest.restclient import SscClient


class CameraController(QrCodeReader):
    def __init__(self, label=None, controller=None):
        self.fps=30
        self.thread = None
        self.stopEvent = None
        self.frame = None
        self.panel = label
        self.cap = None
        self.detector = None
        self.cam = None
        # self.factory = PiGPIOFactory(host='localhost')
        # self.red = LED(19, pin_factory=self.factory)
        # self.green = LED(26, pin_factory=self.factory)
        self.webcamActive = False
        # self.i2c = busio.I2C(board.SCL, board.SDA)
        # self.sensor = adafruit_vl53l0x.VL53L0X(self.i2c)
        # self.sensor.measurement_timing_budget = 200000
        self.controller: SscClient = controller

    @staticmethod
    def rescale_frame(frame, percent=75):
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv.resize(frame, dim, interpolation=cv.INTER_AREA)

    def startCapture(self):
        if not self.webcamActive:
         self.cam = Picamera2() 
         config = self.cam.create_still_configuration()
         self.cam.configure(config)
         self.cam.start()       
         # self.detector = cv.QRCodeDetector()
         # start a thread that constantly pools the video sensor for
         # the most recently read frame
         self.stopEvent = threading.Event()
         self.thread = threading.Thread(target=self.videoLoop, args=())
         self.thread.start()

    @staticmethod
    def decode(frame):
        # Find barcodes and QR codes
        decodedObjects = pyzbar.decode(frame)
        # Print results
        for obj in decodedObjects:
            print('Type : ', obj.type)
            print('Data : ', obj.data, '\n')
        return decodedObjects

    def videoLoop(self):
        
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.webcamActive  = True
                if self.webcamActive:
                    # self.red.on()
                    frame = self.cam.capture_array("main")                    
                    decodedObjects = self.decode(frame)
                    for decodedObject in decodedObjects:
                        x = decodedObject.rect.left
                        y = decodedObject.rect.top
                        print(x, y)
                        print('Type : ', decodedObject.type)
                        print('Data : ', decodedObject.data, '\n')
                        response = self.controller.validate(decodedObject.data.decode("utf-8"))
                        if response.status_code == 200:
                            self.controller.apriporta()
                            print("Apri Porta")
                        else:
                            print("Qrcode failure")
                            self.controller.apriporta()
                    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                    # Display the resulting frame
                    # if bbox is not None:
                    #    cv.putText(frame, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv.FONT_HERSHEY_SIMPLEX,
                    #               0.5, (0, 255, 0), 2)

                    # self.green.off()

                else:
                    # self.red.off()
                    print("Red on")

            self.cam.stop()
            self.cam = None
            self.stopEvent.set()

        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

    def onClose(self):
        if self.stopEvent is not None:
            print("[INFO] closing...")
            self.stopEvent.set()
