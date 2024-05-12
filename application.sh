#!/usr/bin/env python3
import sys
import os

from tkinter import Tk


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from pathlib import Path
home = str(Path.home())

from application import main
from camera import controller
root = Tk()
app = main.Application(root,
                       "ws://service.local:8080/ssc/prenostazione-risorse/websocket",
                       "/info",
                        "http://service.local:8080/ssc",1366, 768, controller.CameraController)

root.title('SSC')
app.mainloop()

