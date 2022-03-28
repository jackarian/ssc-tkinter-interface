#!/usr/bin/env python3
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

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

app = main.Application(None,"ws://localhost:8080/ssc/prenostazione-risorse/websocket","/info")
app.master.title('SSC')
app.master.minsize(820, 480)
app.master.maxsize(820, 480)
app.mainloop()