from Outputs.Led.led_control import LED
from Outputs.Led.led_rgb import RGB
from Outputs.Relay.relay import Relay
from Inputs.Button.button import Button
from power_sensor import PowerSensor

from pinout import *

import time

DEBUG = True

if __name__ == "__main__":
	led_RGB = RGB( LED_RED, LED_GREEN, LED_BLUE, debug = DEBUG )
	RELAYS = [
		Relay( 'TOP RELAY', RELAY_TOP, False, debug = DEBUG  ),
		Relay( 'MIDDLE RELAY', RELAY_MIDDLE, False, debug = DEBUG  ),
		Relay( 'BOTTOM RELAY', RELAY_BOTTOM, False, debug = DEBUG  ),
	]
	pm = PowerSensor( debug = DEBUG )

	led_RGB.pisca( [50, 50, 100], 1 )

	while True:
		try:
                        led_RGB.pisca( [100, 100, 0], 1)
                        print( pm.routine([0xD9, 0xDD, 0xDE]), 1 )
                        time.sleep(1)
                        led_RGB.color( [0,100,0])
                        time.sleep(5)
		except KeyboardInterrupt:
                        led_RGB.stop_thread()
                        print( f"Keyboard interrupt.")
                        break
