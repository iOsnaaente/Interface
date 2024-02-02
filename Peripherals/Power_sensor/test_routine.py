from pm import *


pga_gain = 0
u_gain = 3920
i_gain_N = 39473
i_gain_F = 39473

pm = ATM90E32( debug = True )
pm.begin( 60, pga_gain, u_gain, i_gain_N, i_gain_F )

pm.enable_power_metering()

import time

while True:
	print( pm.get_sys_status_0() )
	print( pm.get_sys_status_1() )
	print( pm.get_line_voltage_a() )
	time.sleep(1)
