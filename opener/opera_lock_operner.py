from  opener.opener_interface import OpenerFacade
from  gpiozero import LED
from singleton_decorator import singleton
import time


class OperaLockOpenerFacade(OpenerFacade):
    
    def __init__(self):        
        self.pin = 26
        self.time_to_wait = 2 
        self.led = LED(self.pin)
        self.led.off()
        
    def lock(self, observable=None):
        try:
            self.led.off()
        except Exception as e:
            pass

    def unlock(self, observable=None):
        try:
           self.led.on()
           time.sleep(self.time_to_wait)
           self.led.off()
        except Exception as e:
            pass

    def unlockForever(self, observable=None):
        try:
            self.led.on()
        except Exception as e:
            pass
        

if __name__ == '__main__':
   import sys
   import os
   SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
   sys.path.append(os.path.dirname(SCRIPT_DIR))
   from pathlib import Path
   home = str(Path.home())
   opner  = OperaLockOpenerFacade()
   opner.unlock()

