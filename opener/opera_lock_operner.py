from  opener.opener_interface import OpenerFacade
from RPi import GPIO
import time

class OperaLockOpenerFacade(OpenerFacade):
    
    def __init__(self):        
        self.pin = 6
        self.time_to_wait = 5
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin,GPIO.OUT)
        GPIO.output(self.pin,1)

    def lock(self, observable=None):
        pass

    def unlock(self, observable=None):
        GPIO.output(self.pin,1);
        time.sleep(self.time_to_wait);
        GPIO.output(self.pin,0);

if __name__ == '__main__':
   opner  = OperaLockOpenerFacade()
   opner.unlock()
