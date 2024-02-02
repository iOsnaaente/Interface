from Outputs.Led.led_control import LED
from Outputs.Led.led_rgb import RGB
from Outputs.Relay.relay import Relay
from Inputs.Button.button import Button
from power_sensor import PowerSensor
from Power_sensor.constants import *

from pinout import *

import time
DEBUG = True

if __name__ == "__main__":

    led_RGB = RGB( LED_RED, LED_GREEN, LED_BLUE, debug = DEBUG )
    pm = PowerSensor( debug = DEBUG )
    while True:
        try:
            led_RGB.pisca( [100, 100, 0], 5)
            print( pm.measure_addrs([Temp]), 1 )
            time.sleep(1)
        except KeyboardInterrupt:
            led_RGB.stop_thread()
            print( f"Keyboard interrupt.")
            break
