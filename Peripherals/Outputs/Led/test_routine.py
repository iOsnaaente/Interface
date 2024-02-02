from led_control import *
from random import randint
import time 

LED_RED = 17
LED_GREEN = 18
LED_BLUE = 27


LR = LED( "RED LED", LED_RED, 'OUT', True, debug = True )
LG = LED( "GREEN LED", LED_GREEN, 'OUT', True, debug = True )
LB = LED( "BLUE LED", LED_BLUE, 'OUT', True, debug = True )


LEDS = [ LR, LG, LB ]
for led in LEDS:
    led.set_pwm( 1000 )
    led.__str__()


while True:
    for led in LEDS:
        led.set_duty( randint(0,100))
    time.sleep( 1 )

