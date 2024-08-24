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
root.attributes('-fullscreen', True)
print(root.winfo_screenwidth())
print(root.winfo_screenheight())
app = main.Application(root,
                       "ws://service.local:8080/ssc/prenostazione-risorse/websocket",
                       "/info",
                        "http://service.local:8080/ssc",
                        root.winfo_screenwidth(), 
                        root.winfo_screenheight(), 
                        controller.CameraController)

root.title('SSC')
try:
  app.mainloop()
except Exception as e:
  print(e)
