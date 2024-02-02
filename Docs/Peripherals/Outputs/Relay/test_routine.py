from random import randint
from relay import *

import time 

RELAY_TOP = 16
RELAY_MIDDLE = 13
RELAY_BOTTOM = 12

LR = Relay( "RELAY_TOP", RELAY_TOP, False, debug = True )
LG = Relay( "RELAY_MIDDLE", RELAY_MIDDLE, False, debug = True )
LB = Relay( "RELAY_BOTTOM", RELAY_BOTTOM, False, debug = True )


RELAYS = [ LR, LG, LB ]
for rel in RELAYS:
    rel.__str__()

while True:
    for rel in RELAYS:
        rel.set_state( randint(0,2))
    time.sleep( 1 )

