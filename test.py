import digitalio
import busio
import time

from ATM90E32.powerMetering import ATM90E32

BAUDRATE = 200_000
CS_PIN   = 10 
SCK      = 11
MISO     = 12
MOSI     = 13

spi_bus = busio.SPI( clock = SCK, MISO = MISO, MOSI = MOSI )
cs      = digitalio.DigitalInOut( CS_PIN )

PME = ATM90E32( spi_bus, cs, BAUDRATE )
print( 'system status: 0x{:x} meter status: 0x{:x}'.format( PME.sys_status, PME.meter_status) ) 