import sys
import threading
import board
import busio
import adafruit_vl53l0x
import time
import numpy as np
import cv2 as cv
from PIL import ImageTk, Image
from rest.restclient import SscClient


class CameraController:
    def __init__(self, label=None, controller=None):
        self.thread = None
        self.stopEvent = None
        self.frame = None
        self.panel = label
        self.pipe = "libcamerasrc ! video/x-raw, width=640, height=480, framerate=30/1 ! videoconvert ! videoscale ! " \
                    "appsink "
        self.cap = None
        self.detector = None
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vl53l0x.VL53L0X(self.i2c)
        self.sensor.measurement_timing_budget = 200000
        self.controller: SscClient = controller
        self.startCapture()
    @staticmethod
    def rescale_frame(frame, percent=75):
        width = int(frame.shape[1] * percent / 100)
        height = int(frame.shape[0] * percent / 100)
        dim = (width, height)
        return cv.resize(frame, dim, interpolation=cv.INTER_AREA)

    def startCapture(self):
        self.cap = cv.VideoCapture(0)
        self.detector = cv.QRCodeDetector()
        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

    def videoLoop(self):
        # DISCLAIMER:
        # I'm not a GUI developer, nor do I even pretend to be. This
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                if self.sensor.range < 1000:
                    ret, frame = self.cap.read()
                    # if frame is read correctly ret is True
                    if not ret:
                        print("Can't receive frame (stream end?). Exiting ...")
                        break
                        # Our operations on the frame come here
                    data, bbox, _ = self.detector.detectAndDecode(frame)
                    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                    # Display the resulting frame
                    if bbox is not None:
                        cv.putText(frame, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv.FONT_HERSHEY_SIMPLEX,
                                   0.5, (0, 255, 0), 2)

                    if data:
                        code = data
                        self.stopEvent.set()
                        frame = self.rescale_frame(frame, 50)
                        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                        image = Image.fromarray(image)
                        image = ImageTk.PhotoImage(image)
                        self.panel.configure(image=image)
                        self.controller.sendPayload(data)

            self.cap.release()
            cv.destroyAllWindows()
            self.cap = None
            self.detector = None
            # self.stopEvent = None

        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

    def onClose(self):
        if self.stopEvent is not None:
            print("[INFO] closing...")
            self.stopEvent.set()
