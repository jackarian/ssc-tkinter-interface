import gpiod
import time
LED_PIN =25
chip = gpiod.Chip('gpiochip4')
led_line = chip.get_line(LED_PIN)
led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
try:
    led_line.set_value(1)
    time.sleep(5)
    led_line.set_value(0)
finally:
   led_line.release()
