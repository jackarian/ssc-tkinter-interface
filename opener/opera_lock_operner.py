from  opener.opener_interface import OpenerFacade
from RPi import GPIO
import time

class OperaLockOpenerFacade(OpenerFacade):
    
    def __init__(self):        
        self.pin = 26
        self.time_to_wait = 5
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin,GPIO.OUT)
        GPIO.output(self.pin,GPIO.LOW)

    def lock(self, observable=None):
        pass

    def unlock(self, observable=None):
        GPIO.output(self.pin,GPIO.HIGH);
        time.sleep(self.time_to_wait);
        GPIO.output(self.pin,GPIO.LOW	);

if __name__ == '__main__':
   opner  = OperaLockOpenerFacade()
   opner.unlock()
