"""
    Description: Adaptação da biblioteca ATM90E32 para Python
    Author: Bruno G. F. Sampaio 
    email: bruno.bielsam.1205@hotmail.com
    date: 15/06/2023 
    version: 1.0.0
    Rev: 0.1
"""

# from adafruit_bus_device.spi_device import SPIDevice 
SPIDevice  = 1 

from constants import *

import digitalio
import struct
import math 
import time 
import busio

spi_bus = busio.SPI( clock = SCK, MISO = MISO, MOSI = MOSI )
cs      = digitalio.DigitalInOut( CS_PIN )

class ATM90E32:

    _round_number = lambda f_num : math.floor(f_num) if f_num - math.floor(f_num) < 0.5 else math.ceil(f_num)
    usleep = lambda x : time.sleep( x/(1e7) )

    _spi_bus    : int = 0
    _cs         : int = 0  
    _baudrate   : int = 0  
    _line_freq  : int = 0          
    _pgagain    : int = 0          
    _ugain      : int = 0      
    _igainA     : int = 0      
    _igainB     : int = 0      
    _igainC     : int = 0      
    
    ''' Initialization Functions '''	
    def __init__( 
            self, 
            bus         : busio.SPI , 
            cs          : digitalio.DigitalInOut, 
            baudrate    : int, 
            line_freq   : int   = 4485, 
            pgagain     : float = 1.0, 
            ugain       : float = 1.0, 
            igainA      : float = 1.0, 
            igainB      : float = 1.0, 
            igainC      : float = 1.0 
    ):
        self._baudrate  = baudrate
        self._line_freq = line_freq
        self._pgagain   = pgagain
        self._ugain     = ugain
        self._igainA    = igainA
        self._igainB    = igainB
        self._igainC    = igainC
        self._cs        = cs

        self.device = SPIDevice( bus, cs, baudrate = baudrate, polarity = 1, phase = 1 )
        self.config_device() 


    def config_device( self ):
        # CurrentGainCT2 = 25498  #25498 - SCT-013-000 100A/50mA
        if ( self._line_freq == 4485 or self._line_freq == 5231 ):
            # Brazil power frequency
            FreqHiThresh = 61 * 100
            FreqLoThresh = 59 * 100
            sagV = 90
        else:
            FreqHiThresh = 51 * 100
            FreqLoThresh = 49 * 100
            sagV = 190

        # calculation for voltage sag threshold - assumes we do not want to go under 90v for split phase and 190v otherwise
        # sqrt(2) = 1.41421356
        fvSagTh = ( sagV * 100 * 1.41421356) / (2 * self._ugain / 32768)

        # convert to int for sending to the ATM90E32
        vSagTh = self._round_number( fvSagTh )

        self._spi_write( SoftReset      , 0x789A            )   # Perform soft reset
        self._spi_write( CfgRegAccEn    , 0x55AA            )   # enable register config access
        self._spi_write( MeterEn        , 0x0001            )   # Enable Metering
        self._spi_write( SagTh          , vSagTh            )   # Voltage sag threshold
        self._spi_write( FreqHiTh       , FreqHiThresh      )   # High frequency threshold - 61.00Hz
        self._spi_write( FreqLoTh       , FreqLoThresh      )   # Lo frequency threshold - 59.00Hz
        self._spi_write( EMMIntEn0      , 0xB76F            )   # Enable interrupts
        self._spi_write( EMMIntEn1      , 0xDDFD            )   # Enable interrupts
        self._spi_write( EMMIntState0   , 0x0001            )   # Clear interrupt flags
        self._spi_write( EMMIntState1   , 0x0001            )   # Clear interrupt flags
        self._spi_write( ZXConfig       , 0x0A55            )   # ZX2, ZX1, ZX0 pin config
        # Set metering config values (CONFIG)
        self._spi_write( PLconstH       , 0x0861            )   # PL Constant MSB (default) - Meter Constant = 3200 - PL Constant = 140625000   
        self._spi_write( PLconstL       , 0xC468            )   # PL Constant LSB (default) - this is 4C68 in the application note, which is incorrect
        self._spi_write( MMode0         , self._line_freq   )   # Mode Config (frequency set in main program)
        self._spi_write( MMode1         , self._pgagain     )   # PGA Gain Configuration for Current Channels - 0x002A (x4) # 0x0015 (x2) # 0x0000 (1x)
        self._spi_write( PStartTh       , 0x0AFC            )   # Active Startup Power Threshold - 50% of startup current = 0.9/0.00032 = 2812.5
        self._spi_write( QStartTh       , 0x0AEC            )   # Reactive Startup Power Threshold
        self._spi_write( SStartTh       , 0x0000            )   # Apparent Startup Power Threshold
        self._spi_write( PPhaseTh       , 0x00BC            )   # Active Phase Threshold = 10% of startup current = 0.06/0.00032 = 187.5
        self._spi_write( QPhaseTh       , 0x0000            )   # Reactive Phase Threshold
        self._spi_write( SPhaseTh       , 0x0000            )   # Apparent  Phase Threshold
        # Set metering calibration values (CALIBRATION)
        self._spi_write( PQGainA        , 0x0000            )   # Line calibration A gain
        self._spi_write( PhiA           , 0x0000            )   # Line calibration A angle
        self._spi_write( PQGainB        , 0x0000            )   # Line calibration B gain
        self._spi_write( PhiB           , 0x0000            )   # Line calibration B angle
        self._spi_write( PQGainC        , 0x0000            )   # Line calibration C gain
        self._spi_write( PhiC           , 0x0000            )   # Line calibration C angle
        self._spi_write( PoffsetA       , 0x0000            )   # A line active power offset
        self._spi_write( QoffsetA       , 0x0000            )   # A line reactive power offset
        self._spi_write( PoffsetB       , 0x0000            )   # B line active power offset
        self._spi_write( QoffsetB       , 0x0000            )   # B line reactive power offset
        self._spi_write( PoffsetC       , 0x0000            )   # C line active power offset
        self._spi_write( QoffsetC       , 0x0000            )   # C line reactive power offset
        # Set metering calibration values (HARMONIC)
        self._spi_write( POffsetAF      , 0x0000            )   # A Fund. active power offset
        self._spi_write( POffsetBF      , 0x0000            )   # B Fund. active power offset
        self._spi_write( POffsetCF      , 0x0000            )   # C Fund. active power offset
        self._spi_write( PGainAF        , 0x0000            )   # A Fund. active power gain
        self._spi_write( PGainBF        , 0x0000            )   # B Fund. active power gain
        self._spi_write( PGainCF        , 0x0000            )   # C Fund. active power gain
        # Set measurement calibration values (ADJUST)
        self._spi_write( UgainA         , self._ugain       )   # A Voltage rms gain
        self._spi_write( IgainA         , self._igainA      )   # A line current gain
        self._spi_write( UoffsetA       , 0x0000            )   # A Voltage offset
        self._spi_write( IoffsetA       , 0x0000            )   # A line current offset
        self._spi_write( UgainB         , self._ugain       )   # B Voltage rms gain
        self._spi_write( IgainB         , self._igainB      )   # B line current gain
        self._spi_write( UoffsetB       , 0x0000            )   # B Voltage offset
        self._spi_write( IoffsetB       , 0x0000            )   # B line current offset
        self._spi_write( UgainC         , self._ugain       )   # C Voltage rms gain
        self._spi_write( IgainC         , self._igainC      )   # C line current gain
        self._spi_write( UoffsetC       , 0x0000            )   # C Voltage offset
        self._spi_write( IoffsetC       , 0x0000            )   # C line current offset
        self._spi_write( CfgRegAccEn    , 0x0000            )   # End configuration


    def _spi_write( self, address, val ) -> None:
        four_byte_buf = bytearray(4)
        address      |= WRITE << 15
        # Pack the address into a the bytearray.  
        # It is an unsigned short(H) that needs to be in MSB(>)
        struct.pack_into( '>H', four_byte_buf, 0, address )
        struct.pack_into( '>H', four_byte_buf, 2, val     )
        self.usleep(4)
        with self._device as spi:
            spi.write(four_byte_buf)
        return 


    def _spi_read( self, address ) -> bytearray:
        two_byte_buf  = bytearray(2)
        results_buf   = bytearray(2)
        address      |= READ << 15
        # Pack the address into a the bytearray.  
        # It is an unsigned short(H) that needs to be in MSB(>)
        struct.pack_into('>H', two_byte_buf, 0, address)
        self.usleep(4)
        with self._device as spi:
            # Send address w/ read request to the ATM90E32
            spi.write(two_byte_buf)
            # Get the unsigned short register values sent from the ATM90E32
            spi.readinto(results_buf)
            result = struct.unpack('>H', results_buf)
            # Unpack returns a tuple.  We're interested in result's first byte
            return result[0]


    def _spi_read32Register( self, regh_addr, regl_addr ):
        val_h   = self._spi_read( regh_addr )
        val_l   = self._spi_read( regl_addr )
        val     = (val_h << 16) + val_l     # Concatena 
        val     = val ^ 0xffffffff          # Flipa os bits...
        return (val)


    @property
    def lastSpiData( self ):
        reading = self._spi_read( LastSPIData )
        return reading

    @property
    def sys_status0( self ):
        reading = self._spi_read( EMMIntState0 )
        return reading

    @property
    def sys_status1( self ):
        reading = self._spi_read( EMMIntState1 )
        return reading

    @property
    def meter_status0( self ):
        reading = self._spi_read( EMMState0 )
        return reading

    @property
    def meter_status1( self ):
        reading = self._spi_read( EMMState1 )
        return reading

    @property
    def line_voltageA( self ):
        reading = self._spi_read( UrmsA )
        return reading / 100.0

    @property
    def line_voltageB( self ):
        reading = self._spi_read( UrmsB )
        return reading / 100.0

    @property
    def line_voltageC( self ):
        reading = self._spi_read( UrmsC )
        return reading / 100.0

    @property
    def line_currentA( self ):
        reading = self._spi_read( IrmsA )
        return reading / 1000.0

    @property
    def line_currentC( self ):
        reading = self._spi_read( IrmsC )
        return reading / 1000.0

    @property
    def frequency( self ):
        reading = self._spi_read( Freq )
        return reading / 100.0

    @property
    def active_power( self ):
        reading = self._spi_read32Register( PmeanT, PmeanTLSB )
        return reading * 0.00032


    ''' '''
    def CalculateVIOffset( self, regh_addr, regl_addr, offset_reg ):
        pass 
    
    def CalculatePowerOffset( self, regh_addr, regl_addr, offset_reg ):
        pass 
    
    def CalibrateVI( self, reg, actualVal ):
        pass 


    ''' Main Electrical Parameters (VOTLAGE)'''
    def GetLineVoltageA( self ):
        pass
    def GetLineVoltageB( self ):
        pass
    def GetLineVoltageC( self ):
        pass

    ''' Main Electrical Parameters (CURRENT) '''
    def GetLineCurrentA( self ):
        pass
    def GetLineCurrentB( self ):
        pass
    def GetLineCurrentC( self ):
        pass
    def GetLineCurrentN( self ):
        pass
    
    ''' Main Electrical Parameters (POWER)'''
    def GetActivePowerA( self ):
        pass
    def GetActivePowerB( self ):
        pass
    def GetActivePowerC( self ):
        pass
    def GetTotalActivePower( self ):
        pass 
    def GetTotalActiveFundPower( self ):
        pass 
    def GetTotalActiveHarPower( self ):
        pass 
    def GetReactivePowerA( self ):
        pass 
    def GetReactivePowerB( self ):
        pass 
    def GetReactivePowerC( self ):
        pass 
    def GetTotalReactivePower( self ):
        pass 
    def GetApparentPowerA( self ):
        pass 
    def GetApparentPowerB( self ):
        pass 
    def GetApparentPowerC( self ):
        pass 
    def GetTotalApparentPower( self ):
        pass 

    ''' Main Electrical Parameters (FREQUENCY) '''
    def GetFrequency( self ):
        pass

    ''' Main Electrical Parameters (POWER FACTOR)'''
    def GetPowerFactorA( self ):
        pass 
    def GetPowerFactorB( self ):
        pass 
    def GetPowerFactorC( self ):
        pass 
    def GetTotalPowerFactor( self ):
        pass 

    ''' Main Electrical Parameters (PHASE) '''
    def GetPhaseA( self ):
        pass
    def GetPhaseB( self ):
        pass
    def GetPhaseC( self ):
        pass

    ''' Temperature '''
    def GetTemperature( self ):
        pass 

    ''' Energy Consumption '''
    def GetImportEnergy( self ):
        pass
    def GetImportReactiveEnergy( self ):
        pass
    def GetImportApparentEnergy( self ):
        pass
    def GetExportEnergy( self ):
        pass
    def GetExportReactiveEnergy( self ):
        pass 

    ''' System Status '''
    def GetSysStatus0( self ):
        pass 
    def GetSysStatus1( self ):
        pass 
    def GetMeterStatus0( self ):
        pass 
    def GetMeterStatus1( self ):
        pass 