#!/usr/bin/python

"""
    Description: Adaptação da biblioteca ATM90E32 para Python
    Author: Bruno G. F. Sampaio 
    email: bruno.bielsam.1205@hotmail.com
    date: 27/11/2023
    version: 1.2.1
    Rev: 0.2
"""

from Power_sensor.constants import *

import RPi.GPIO as GPIO 
import spidev

import struct
import time
import math

class ATM90E32:
    line_freq: int
    pga_gain: int
    u_gain: int
    i_gain_F: int
    i_gain_N: int

    SPI_CHANNEL = 0
    SPI_DISP = 0
    SPI_SPEED = 100_000

    CS: int = 8

    debug: bool

    def __init__( self, debug: bool = False ) -> None:
        ''' SpiDev usa Dispositivo e Canal para criar o SPI 
            Essas configurações devem ser feitas no .config do Rasp
            As definições de pinos estão no .config também
        '''
        self.spi = spidev.SpiDev()
        self.spi.open( self.SPI_DISP, self.SPI_CHANNEL )
        self.spi.max_speed_hz = self.SPI_SPEED
        self.spi.mode = 0x03

        ''' Chip Select Setup ''' 
        GPIO.setmode( GPIO.BCM )
        GPIO.setwarnings( False )
        GPIO.setup( self.CS, GPIO.OUT )

        self.debug = debug


    def begin( self, line_freq : int, pga_gain : int, u_gain : int, i_gain_N : int, i_gain_F: int, u_min : int = 190 ):
        self.lineFreq = line_freq    # frequency of power
        self.pga_gain = pga_gain     # PGA Gain for current channels
        ''' Ganho de tensão: Definido pelo divisor resistivo. '''
        self.u_gain = u_gain         
        ''' Ganho de corrente: Definido pelo TC (datasheet) '''
        self.i_gain_F = i_gain_F
        self.i_gain_N = i_gain_N
        ''' Default value to operate with UA and aparent power measure ''' 
        MMode_value = 0b_0001_0000_0001_1100
        if line_freq < 60:
            MMode_value &= ( 0xffff-(1<<12) ) 
            freq_high_thresh = 51 * 100
            freq_low_thresh = 49 * 100
        else: 
            freq_high_thresh = 61 * 100
            freq_low_thresh = 59 * 100
            
        # Tensão mínima de threshold 
        u_sag_thresh = int(( 90 * 100 * math.sqrt(2)) / (2 * self.u_gain / 32768))
        
        # Enable ZX0 channel with UA zero cross with all passings by zero 
        zero_cross_ZX0 = 0b_111_111_000_11_11_10_0 

        # Definição dos canais habilitados de medição de tensão e corrente 
        voltage_channels = 0b_00000_011_0_010_0_001 # Canal I1 = IA e I2 = IB 
        current_channels = 0b_00000_011_0_011_0_001 # Canal V1 = VA 

        # Initialize registers
        self.write( SoftReset, 0x789A)              # 70H Perform soft reset
        time.sleep( 100 / 1_000_000 )                # 100us de sleep 

        self.write( CfgRegAccEn, 0x55AA)            # 7FH enable register config access
        self.write( MeterEn, 0x0001)                # 00H Enable Metering

        self.write( ChannelMapI, current_channels ) # 01H Definição dos canais de corrente 
        self.write( ChannelMapU, voltage_channels ) # 02H Definição dos canais de tensão 

        self.write(SagPeakDetCfg, 0x143F)           # 05H Sag and Voltage peak detect period set to 20ms
        self.write(SagTh, u_sag_thresh)             # 08H Voltage sag threshold
        self.write(FreqHiTh, freq_high_thresh)      # 0DH High frequency threshold
        self.write(FreqLoTh, freq_low_thresh)       # 0CH Lo frequency threshold

        # self.write(EMMIntEn0, 0xB76F)
        # self.write(EMMIntEn1, 0xDDFD)
        # self.write(EMMIntState0, 0x0001)
        # self.write(EMMIntState1, 0x0001)

        self.write(ZXConfig, zero_cross_ZX0)        # ZX0 pin config - all polarity
        
        # Set metering config values (CONFIG)
        self.write(PLconstH, 0x0861)                # 31 PL Constant MSB (default) - Meter Constant = 3200 - PL Constant = 140625000
        self.write(PLconstL, 0xC468)                # 32 PL Constant LSB (default) - this is 4C68 in the application note, which is incorrect
        
        self.write(MMode0  , MMode_value)           # 33 Mode Config (frequency set in main program)
        self.write(MMode1  , pga_gain)              # 34 PGA Gain Configuration for Current Channels - 0x002A (x4) # 0x0015 (x2) # 0x0000 (1x)
        
        self.write(PStartTh, 0x1D4C)                # 35 All phase Active Startup Power Threshold - 50% of startup current = 0.02A/0.00032 = 7500
        self.write(QStartTh, 0x1D4C)                # 36 All phase Reactive Startup Power Threshold
        self.write(SStartTh, 0x1D4C)                # 37 All phase Apparent Startup Power Threshold
        self.write(PPhaseTh, 0x02EE)                # 38 Each phase Active Phase Threshold = 10% of startup current = 0.002A/0.00032 = 750
        self.write(QPhaseTh, 0x02EE)                # 39 Each phase Reactive Phase Threshold
        self.write(SPhaseTh, 0x02EE)                # 3A Each phase Apparent Phase Threshold

        # Set metering calibration values (CALIBRATION)
        self.write(PQGainA , 0x0000)                # 47 Line calibration gain
        self.write(PhiA    , 0x0000)                # 48 Line calibration angle
        self.write(PQGainB , 0x0000)                # 49 Line calibration gain
        self.write(PhiB    , 0x0000)                # 4A Line calibration angle
        self.write(PoffsetA, 0x0000)                # 41 A line active power offset FFDC
        self.write(QoffsetA, 0x0000)                # 42 A line reactive power offset
        self.write(PoffsetB, 0x0000)                # 43 B line active power offset
        self.write(QoffsetB, 0x0000)                # 44 B line reactive power offset

        # Set metering calibration values (HARMONIC)
        self.write(POffsetAF, 0x0000)               # 51 A Fund. active power offset
        self.write(POffsetBF, 0x0000)               # 52 B Fund. active power offset
        self.write(PGainAF, 0x0000)                 # 54 A Fund. active power gain
        self.write(PGainBF, 0x0000)                 # 55 B Fund. active power gain

        # Set measurement calibration values (ADJUST)
        self.write(UgainA, self.u_gain)             # 61 A Voltage rms gain
        self.write(UoffsetA, 0x0000)                # 63 A Voltage offset - 61A8
        self.write(IgainA, self.i_gain_F)           # 62 A line current gain
        self.write(IoffsetA, 0x0000)                # 64 A line current offset - FE60
        self.write(IgainB, self.i_gain_N)           # 66 A line current gain
        self.write(IoffsetB, 0x0000)                # 68 A line current offset - FE60
        
        self.write(CfgRegAccEn, 0x0000)             # 7F end configuration
        # self.write( MeterEn, 0x0000)                # 00H Disable Metering
        

    def chip_select( self, state: bool ):
      if state:    
        GPIO.output( self.CS, GPIO.HIGH  )
      else:
        GPIO.output( self.CS, GPIO.LOW )


    def write( self, addr : int, value : int ) -> bool:
      try:
        # Adiciona a flag WRITE no endereço
        addr |= WRITE << 15
        # Converte os inteiros para bytearray de 16 bits (dois bytes)
        addr = bytearray(addr.to_bytes(2, byteorder = 'big'))
        value = bytearray(value.to_bytes(2, byteorder = 'big'))

        # Concatenando o endereço e o valor
        data_to_send = addr + value

        self.chip_select( False )        
        time.sleep( 10 / 1_000_000 )      # 1us de sleep 
        self.spi.xfer( data_to_send )
        self.chip_select( True )
        return True  

      except Exception as err:
        print( err, "/tAddr:", addr, "/tValue:", value )
        return False 


    def read16bits( self, addr : int ) -> int:
        # Adiciona a flag READ no endereço
        addr |= READ << 15
        value = 0x00 

        # Converte o endereço para bytearray de 16 bits (dois bytes)
        addr = bytearray(addr.to_bytes(2, byteorder='big'))
        value = bytearray( value.to_bytes(2, byteorder='big'))
        
        data_to_send = addr + value 
        data_received = b''

        self.chip_select( False )        
        time.sleep( 10 / 1_000_000 )                # 1us de sleep 
        data_received = self.spi.xfer( data_to_send )
        self.chip_select( True )

        # Convertendo os bytes lidos de volta para um valor inteiro
        value = int.from_bytes(data_received, byteorder='big')
        return value


    def read32bits(self, regh_addr, regl_addr):
        val_h = self.read16bits(regh_addr)
        val_l = self.read16bits(regl_addr)
        # Concatenar os 2 registradores para formar um número de 32 bits
        return (val_h << 16) | val_l  
    

    ''' Retorna a tensão da linha A em volts '''
    def get_line_voltage_a(self) -> float:
        voltage = self.read16bits(UrmsA)
        return float(voltage) / 100

    ''' Retorna a corrente da linha A em amps '''
    def get_line_current_a(self) -> float:
        current = self.read16bits(IrmsA)
        return float(current) / 1000

    ''' Retorna a potência ativa da linha A em watts '''
    def get_active_power_a(self) -> float:
        val = self.read32bits(PmeanA, PmeanALSB)
        return float(val) * 0.00032

    ''' Retorna a potência ativa fundamental total em watts '''
    def get_total_active_fundamental_power(self) -> float:
        val = self.read32bits(PmeanTF, PmeanTFLSB)
        return float(val) * 0.00032

    ''' Retorna a potência ativa harmônica total em watts '''
    def get_total_active_harmonic_power(self) -> float:
        val = self.read32bits(PmeanTH, PmeanTHLSB)
        return float(val) * 0.00032

    ''' Retorna a potência reativa da linha A em vars '''
    def get_reactive_power_a(self) -> float:
        val = self.read32bits(QmeanA, QmeanALSB)
        return float(val) * 0.00032

    ''' Retorna a potência aparente da linha A em VA '''
    def get_apparent_power_a(self) -> float:
        val = self.read32bits(SmeanA, SmeanALSB)
        return float(val) * 0.00032

    ''' Retorna a frequência da linha em hertz '''
    def get_frequency(self) -> float:
        freq = self.read16bits(Freq)
        return float(freq) / 100

    ''' Retorna o fator de potência da linha A '''
    def get_power_factor_a(self) -> float:
        pf = self.read16bits(PFmeanA)
        return float(pf) / 1000
  
    ''' Habilita a medição de energia '''
    def enable_power_metering( self ) -> bool:
        try:
          self.write( MeterEn, 0x1234 )
          return True 
        except:
            return False   
    
    ''' Desabilita a medição de energia '''
    def disable_power_metering( self ) -> bool:
        try:
          self.write( MeterEn, 0x0000 )
          return True 
        except:
            return False 

    ''' System Status Registers '''
    def get_sys_status_0( self ):
        return self.read16bits( EMMIntState0 )

    def get_sys_status_1( self ):
        return self.read16bits( EMMIntState1 )

    def get_meter_status_0( self ) :
        return self.read16bits( EMMState0 )

    def get_meter_status_1( self ) :
        return self.read16bits( EMMState1 )
        



"""
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

        
        
double ATM90E32::CalculateVIOffset(unsigned short regh_addr, unsigned short regl_addr ''', unsigned short offset_reg''') :
//for getting the lower registers of Voltage and Current and calculating the offset
//should only be run when CT sensors are connected to the meter,
//but not connected around wires
  uint32_t val, val_h, val_l
  uint16_t offset
  val_h = CommEnergyIC(READ, regh_addr, 0xFFFF)
  val_l = CommEnergyIC(READ, regl_addr, 0xFFFF)
  val = CommEnergyIC(READ, regh_addr, 0xFFFF)
  val = val_h << 16 //move high register up 16 bits
  val |= val_l //concatenate the 2 registers to make 1 32 bit number
  val = val >> 7 //right shift 7 bits - lowest 7 get ignored - V & I registers need this
  val = (~val) + 1 //2s compliment
  offset = val //keep lower 16 bits
  //CommEnergyIC(WRITE, offset_reg, (signed short)val)
  return uint16_t(offset)



double ATM90E32::CalculatePowerOffset(unsigned short regh_addr, unsigned short regl_addr ''', unsigned short offset_reg''') :
//for getting the lower registers of energy and calculating the offset
//should only be run when CT sensors are connected to the meter,
//but not connected around wires
  uint32_t val, val_h, val_l
  uint16_t offset
  val_h = CommEnergyIC(READ, regh_addr, 0xFFFF)
  val_l = CommEnergyIC(READ, regl_addr, 0xFFFF)
  val = CommEnergyIC(READ, regh_addr, 0xFFFF)
  val = val_h << 16 //move high register up 16 bits
  val |= val_l //concatenate the 2 registers to make 1 32 bit number
  val = (~val) + 1 //2s compliment
  offset = val //keep lower 16 bits
  //CommEnergyIC(WRITE, offset_reg, (signed short)val)
  return uint16_t(offset)



double ATM90E32::CalibrateVI(unsigned short reg, unsigned short actualVal) :
//input the Voltage or Current register, and the actual value that it should be
//actualVal can be from a calibration meter or known value from a power supply
  uint16_t gain, val, m, gainReg
	//sample the reading 
	val = CommEnergyIC(READ, reg, 0xFFFF)
	val += CommEnergyIC(READ, reg, 0xFFFF)
	val += CommEnergyIC(READ, reg, 0xFFFF)
	val += CommEnergyIC(READ, reg, 0xFFFF)
	//get value currently in gain register
	switch (reg) :
		case UrmsA: :
			gainReg = UgainA 
		case UrmsB: :
			gainReg = UgainB 
		case UrmsC: :
			gainReg = UgainC 
		case IrmsA: :
			gainReg = IgainA 
		case IrmsB: :
			gainReg = IgainB 
		case IrmsC: :
			gainReg = IgainC 
		
	gain = CommEnergyIC(READ, gainReg, 0xFFFF) 
	m = actualVal
	m = ((m * gain) / val)
	gain = m
	//write new value to gain register
	CommEnergyIC(WRITE, gainReg, gain)
	return(gain)

    
        
// VOLTAGE
double ATM90E32::GetLineVoltageA() :
  unsigned short voltage = CommEnergyIC(READ, UrmsA, 0xFFFF)
  return (double)voltage / 100

double ATM90E32::GetLineVoltageB() :
  unsigned short voltage = CommEnergyIC(READ, UrmsB, 0xFFFF)
  return (double)voltage / 100

double ATM90E32::GetLineVoltageC() :
  unsigned short voltage = CommEnergyIC(READ, UrmsC, 0xFFFF)
  return (double)voltage / 100



// CURRENT
double ATM90E32::GetLineCurrentA() :
  unsigned short current = CommEnergyIC(READ, IrmsA, 0xFFFF)
  return (double)current / 1000

double ATM90E32::GetLineCurrentB() :
  unsigned short current = CommEnergyIC(READ, IrmsB, 0xFFFF)
  return (double)current / 1000

double ATM90E32::GetLineCurrentC() :
  unsigned short current = CommEnergyIC(READ, IrmsC, 0xFFFF)
  return (double)current / 1000

double ATM90E32::GetLineCurrentN() :
  unsigned short current = CommEnergyIC(READ, IrmsN, 0xFFFF)
  return (double)current / 1000



// ACTIVE POWER
double ATM90E32::GetActivePowerA() :
  int val = Read32Register(PmeanA, PmeanALSB)
  return (double)val * 0.00032

double ATM90E32::GetActivePowerB() :
  int val = Read32Register(PmeanB, PmeanBLSB)
  return (double)val * 0.00032

double ATM90E32::GetActivePowerC() :
  int val = Read32Register(PmeanC, PmeanCLSB)
  return (double)val * 0.00032

double ATM90E32::GetTotalActivePower() :
   int val = Read32Register(PmeanT, PmeanTLSB)
   return (double)val * 0.00032



// Active Fundamental Power
double ATM90E32::GetTotalActiveFundPower() :
  int val = Read32Register(PmeanTF, PmeanTFLSB)
  return (double)val * 0.00032



// Active Harmonic Power
double ATM90E32::GetTotalActiveHarPower() :
  int val = Read32Register(PmeanTH, PmeanTHLSB)
  return (double)val * 0.00032



// REACTIVE POWER
double ATM90E32::GetReactivePowerA() :
  int val = Read32Register(QmeanA, QmeanALSB)
  return (double)val * 0.00032

double ATM90E32::GetReactivePowerB() :
  int val = Read32Register(QmeanB, QmeanBLSB)
  return (double)val * 0.00032

double ATM90E32::GetReactivePowerC() :
  int val = Read32Register(QmeanC, QmeanCLSB)
  return (double)val * 0.00032

double ATM90E32::GetTotalReactivePower() :
  int val = Read32Register(QmeanT, QmeanTLSB)
  return (double)val * 0.00032



// APPARENT POWER
double ATM90E32::GetApparentPowerA() :
  int val = Read32Register(SmeanA, SmeanALSB)
  return (double)val * 0.00032

double ATM90E32::GetApparentPowerB() :
  int val = Read32Register(SmeanB, SmeanBLSB)
  return (double)val * 0.00032

double ATM90E32::GetApparentPowerC() :
  int val = Read32Register(SmeanC, SmeanCLSB)
  return (double)val * 0.00032

double ATM90E32::GetTotalApparentPower() :
  int val = Read32Register(SmeanT, SAmeanTLSB)
  return (double)val * 0.00032



// FREQUENCY
double ATM90E32::GetFrequency() :
  unsigned short freq = CommEnergyIC(READ, Freq, 0xFFFF)
  return (double)freq / 100



// POWER FACTOR
double ATM90E32::GetPowerFactorA() :
  signed short pf = (signed short) CommEnergyIC(READ, PFmeanA, 0xFFFF)
  return (double)pf / 1000

double ATM90E32::GetPowerFactorB() :
  signed short pf = (signed short) CommEnergyIC(READ, PFmeanB, 0xFFFF)
  return (double)pf / 1000

double ATM90E32::GetPowerFactorC() :
  signed short pf = (signed short) CommEnergyIC(READ, PFmeanC, 0xFFFF)
  return (double)pf / 1000

double ATM90E32::GetTotalPowerFactor() :
  signed short pf = (signed short) CommEnergyIC(READ, PFmeanT, 0xFFFF)
  return (double)pf / 1000



// MEAN PHASE ANGLE
double ATM90E32::GetPhaseA() :
  unsigned short angleA = (unsigned short) CommEnergyIC(READ, PAngleA, 0xFFFF)
  return (double)angleA / 10

double ATM90E32::GetPhaseB() :
  unsigned short angleB = (unsigned short) CommEnergyIC(READ, PAngleB, 0xFFFF)
  return (double)angleB / 10

double ATM90E32::GetPhaseC() :
  unsigned short angleC = (unsigned short) CommEnergyIC(READ, PAngleC, 0xFFFF)
  return (double)angleC / 10



// TEMPERATURE
double ATM90E32::GetTemperature() :
  short int atemp = (short int) CommEnergyIC(READ, Temp, 0xFFFF)
  return (double)atemp



''' Gets the Register Value if Desired '''
// REGISTER
double ATM90E32::GetValueRegister(unsigned short registerRead) :
  return (double) CommEnergyIC(READ, registerRead, 0xFFFF) //returns value register



// REGULAR ENERGY MEASUREMENT


// FORWARD ACTIVE ENERGY
// these registers accumulate energy and are cleared after being read
double ATM90E32::GetImportEnergy() :
  unsigned short ienergyT = CommEnergyIC(READ, APenergyT, 0xFFFF)
  return (double)ienergyT / 100 / 3200 //returns kWh

  // unsigned short ienergyA = CommEnergyIC(READ, APenergyA, 0xFFFF)
  // unsigned short ienergyB = CommEnergyIC(READ, APenergyB, 0xFFFF)
  // unsigned short ienergyC = CommEnergyIC(READ, APenergyC, 0xFFFF)

// FORWARD REACTIVE ENERGY
double ATM90E32::GetImportReactiveEnergy() :
  unsigned short renergyT = CommEnergyIC(READ, RPenergyT, 0xFFFF)
  return (double)renergyT / 100 / 3200 //returns kWh

  // unsigned short renergyA = CommEnergyIC(READ, RPenergyA, 0xFFFF)
  // unsigned short renergyB = CommEnergyIC(READ, RPenergyB, 0xFFFF)
  // unsigned short renergyC = CommEnergyIC(READ, RPenergyC, 0xFFFF)


// APPARENT ENERGY
double ATM90E32::GetImportApparentEnergy() :
  unsigned short senergyT = CommEnergyIC(READ, SAenergyT, 0xFFFF)
  return (double)senergyT / 100 / 3200 //returns kWh

  // unsigned short senergyA = CommEnergyIC(READ, SenergyA, 0xFFFF)
  // unsigned short senergyB = CommEnergyIC(READ, SenergyB, 0xFFFF)
  // unsigned short senergyC = CommEnergyIC(READ, SenergyC, 0xFFFF)

  
// REVERSE ACTIVE ENERGY
double ATM90E32::GetExportEnergy() :
  unsigned short eenergyT = CommEnergyIC(READ, ANenergyT, 0xFFFF)
  return (double)eenergyT / 100 / 3200 //returns kWh

  // unsigned short eenergyA = CommEnergyIC(READ, ANenergyA, 0xFFFF)
  // unsigned short eenergyB = CommEnergyIC(READ, ANenergyB, 0xFFFF)
  // unsigned short eenergyC = CommEnergyIC(READ, ANenergyC, 0xFFFF)

  
// REVERSE REACTIVE ENERGY
double ATM90E32::GetExportReactiveEnergy() :
  unsigned short reenergyT = CommEnergyIC(READ, RNenergyT, 0xFFFF)
  return (double)reenergyT / 100 / 3200 //returns kWh

  // unsigned short reenergyA = CommEnergyIC(READ, RNenergyA, 0xFFFF)
  // unsigned short reenergyB = CommEnergyIC(READ, RNenergyB, 0xFFFF)
  // unsigned short reenergyC = CommEnergyIC(READ, RNenergyC, 0xFFFF)

        """
