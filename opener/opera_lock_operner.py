from  opener.opener_interface import OpenerFacade
from  gpiozero import LED
import time

class OperaLockOpenerFacade(OpenerFacade):
    
    def __init__(self):        
        self.pin = 26
        self.time_to_wait = 5
        self.led = LED(self.pin)
        self.led.off()
        
    def lock(self, observable=None):
        pass

    def unlock(self, observable=None):
        self.led.on()
        time.sleep(self.time_to_wait)
        self.led.off()

if __name__ == '__main__':
   import sys
   import os
   SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
   sys.path.append(os.path.dirname(SCRIPT_DIR))
   from pathlib import Path
   home = str(Path.home())
   opner  = OperaLockOpenerFacade()
   opner.unlock()
