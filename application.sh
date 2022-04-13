#!/usr/bin/env python3
import sys
import os

from tkinter import Tk

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from pathlib import Path
home = str(Path.home())
#import json
#import time

#from stomp_ws.client import Client
#import logging

from application import main

#def print_frame(frame):
#    print(json.loads(frame.body))


#LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
#logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

# open transport
#client = Client("ws://localhost:8080/ssc/prenostazione-risorse/websocket")

# connect to the endpoint
#client.connect()

# subscribe channel
#client.subscribe("/info", callback=print_frame)

#time.sleep(60)

#client.disconnect()
root = Tk()
app = main.Application(root,
                       "ws://service.local:8080/ssc/prenostazione-risorse/websocket",
                       "http://service.local:8080/ssc",
                       "/info",1366, 768)
root.title('SSC')
app.mainloop()