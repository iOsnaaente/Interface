WRITE = 0 # WRITE SPI
READ  = 1 # READ SPI

SOFT_RESET = 0x789A
CFG_ALLOW = 0x55AA 


''' STATUS REGISTERS '''
# MeterEn[7:0] Metering is enabled when any bit in this register is set
# Address: 00H
# Type: Read/Write
# Default Value: 00H
MeterEn         = 0x00	# Metering Enable 


# Current and Voltage Channel Mapping Configuration
#   bit        Input       +--------+-------------------+
#  10:8      Channel C     | Code   |  ADC Input Source |                
#   6:4      Channel B     +--------+-------------------+    
#   2:0      Channel A     | 000    |  I0               |    
#                          | 001    |  I1               |    
#                          | 010    |  I2               |    
#                          | 011    |  Fixed-0          |        
#                          | 100    |  U0               |    
#                          | 101    |  U1               |    
#                          | 110    |  U2               |    
#                          | 111    |  Fixed-0          |        
#                          +--------+-------------------+
# Address: 01H (Current)
# Address: 02H (Voltage)
# Type: Read/Write
# Default Value (I): 0210H = 0b 0000 0010 0001 0000 
# Default Value (V): 0654H = 0b 0000 0110 0101 0100
ChannelMapI     = 0x01 	# Current Channel Mapping Configuration
ChannelMapU     = 0x02 	# Voltage Channel Mapping Configuration


# 15:8 PeakDet_period:   Period in which the peak detector detects the U/I peak. Unit is ms.
# 7:0 Sag_Period:        Period in which the phase voltage needs to stay below the SagTh before to assert the Sag status. Unit is ms.
#                        The Phase Loss detector also uses this parameter in detecting Phase Loss.
# Address: 05H
# Type: Read/Write
# Default Value: 143FH = 0b 0001 0100 0011 1111 
SagPeakDetCfg   = 0x05 	# Sag and Peak Detector Period Configuration


# Address: 06H
# Type: Read/Write
# Default Value: C000H
OVth            = 0x06	# Over Voltage Threshold


#    Bit            Name        Description
#   15:13       ZX2Src[2:0]     These bits select the signal source for the ZX2, ZX1 or ZX0 pins.
#   12:10       ZX1Src[2:0]         Code    Source
#    9: 7       ZX0Src[2:0]          011    Fixed-0
#                                    000    Ua
#                                    001    Ub
#                                    010    Uc
#                                    111    Fixed-0
#                                    100    Ia
#                                    101    Ib
#                                    110    Ic
#
#    6: 5       ZX2Con[1:0]     These bits configure zero-crossing type for the ZX2, ZX1 and ZX0 pins.
#    4: 3       ZX1Con[1:0]         Code    Zero-Crossing Configuration  
#    2: 1       ZX0Con[1:0]           00    Positive Zero-crossing  
#                                     01    Negative Zero-crossing
#                                     10    All Zero-crossing
#                                     11    No Zero-crossing Output
# 
#       0        ZXdis           This bit determines whether to disable the ZX signals:
#                                   0: enable
#                                   1: disable all the ZX signals to ‘0’ (default).
#
# Address: 07H
# Type: Read/Write
# Default Value: 0001H
ZXConfig        = 0x07	# Zero-Crossing Config

SagTh           = 0x08	# Voltage Sag Th
PhaseLossTh     = 0x09	# Voltage Phase Losing Th


# Neutral current (calculated) warning threshold.
# Threshold for calculated (Ia + Ib +Ic) N line rms current. Unsigned 16 bit, unit 1mA.
# If N line rms current is greater than the threshold, the INOv0ST bit (b7, EMMState0) bit is asserted if
# enabled. Refer to 3.7.5 Neutral Line Overcurrent Detection.
# 
# Address: 0AH
# Type: Read/Write
# Default Value: FFFFH
INWarnTh        = 0x0A	# Neutral Current (Calculated) Warning Threshold


# Over Current threshold -> 0xFFFF maps to ADC output full-scale peak.
# 
# Address: 0BH
# Type: Read/Write
# Default Value: C000H
OIth            = 0x0B	# Over Current Threshold

FreqLoTh        = 0x0C	# Low Threshold for Frequency Detection
FreqHiTh        = 0x0D	# High Threshold for Frequency Detection


#   Bit        Name                         Description
#   15:9         -          Reserved.
#   8       PMPwrDownVch    In Partial Measurement Mode the V0/V1/V2 analog channel can be powered off to save power
#                               0: Power on
#                               1: Power off
#   3     ACTRL_CLK_GATE    Power off the clock of analog control block to save power.
#                               0: Power on
#                               1: Power off
#   2       DSP_CLK_GATE    Power off the clock of DSP register to save power.
#                               0: Power on
#                               1: Power off
#   1       MTMS_CLK_GATE   Power off the metering and measuring block to save power.
#                               0: Power on
#                               1: Power off
#   0        PMClkLow       In Partial Measurement Mode the main clock can be reduced to 8.192MHz to save power.
#                               0: 16.384MHz
#                               1: 8.192MHz
#
# Address: 0EH
# Type: Read/Write
# Default Value: 010FH = 0b 0000 0001 0000 1111
PMPwrCtrl       = 0x0E	# Partial Measurement Mode Power Control

# Default Value: 0000H
IRQ0MergeCfg    = 0x0F 	# IRQ0 Merge Configuration


''' EMM STATUS REGISTERS '''
# SoftReset[15:0] = Software reset register. The M90E32AS resets if 789AH is written
#                   to this register. The reset domain is the
#                   same as the RESET pin or Power On Reset. Reading this register always return 0.
# 
# Address: 70H
# Type: Write
# Default Value: 0000H
SoftReset       = 0x70	# Software Reset

EMMState0       = 0x71	# EMM State 0
EMMState1       = 0x72	# EMM State 1

EMMIntState0    = 0x73  # EMM Interrupt Status 0
EMMIntState1    = 0x74  # EMM Interrupt Status 1

EMMIntEn0       = 0x75	# EMM Interrupt Enable 0
EMMIntEn1       = 0x76	# EMM Interrupt Enable 1

LastSPIData     = 0x78	# Last Read/Write SPI Value
CRCErrStatus    = 0x79	# CRC Error Status
CRCDigest       = 0x7A	# CRC Digest

CfgRegAccEn     = 0x7F	# Configure Register Access Enable


''' LOW POWER MODE REGISTERS - NOT USED '''
DetectCtrl      = 0x10
DetectTh1       = 0x11
DetectTh2       = 0x12
DetectTh3       = 0x13
PMOffsetA       = 0x14
PMOffsetB       = 0x15
PMOffsetC       = 0x16
PMPGA           = 0x17
PMIrmsA         = 0x18
PMIrmsB         = 0x19
PMIrmsC         = 0x1A
PMConfig        = 0x10B
PMAvgSamples    = 0x1C
PMIrmsLSB       = 0x1D


''' CONFIGURATION REGISTERS '''
PLconstH    = 0x31 		# High Word of PL_Constant
PLconstL    = 0x32 		# Low Word of PL_Constant


#   Bit         Name            Description
#   15-13       -               Reserved.
#   12          Freq60Hz        Current Grid operating line frequency.
#                                   0: 50Hz (default)
#                                   1: 60Hz
#   11          HPFoff          Disable HPF in the signal processing path.
#   10          didtEn          Enable Integrator for didt current sensor.
#                                   0: disable (default)
#                                   1: enable
#   9           -               Reserved.
#   8           3P3W            This bit defines the voltage/current phase sequence detection mode:
#                                   0: 3P4W (default)
#                                   1: 3P3W (Ua is Uab, Uc is Ucb, Ub is not used)
#   7           CF2varh         CF2 pin source:
#                                   0: apparent energy
#                                   1: reactive energy (default)
#   6-5         -               Reserved.
#   4           ABSEnQ          These bits configure the calculation method of total (all-phase-sum) reactive/active energy and power:
#   3           ABSEnP              0: Arithmetic sum: (default)
#                                       ET=EA*EnPA+ EB*EnPB+ EC*EnPC
#                                       PT= PA*EnPA+ PB*EnPB+ PC*EnPC
#                                   1: Absolute sum:
#                                       ET=|EA|*EnPA+ |EB|*EnPB+ |EC|*EnPC
#                                       PT=|PA|*EnPA+ |PB|*EnPB+ |PC|*EnPC
#   2           EnPA            These bits configure whether Phase A/B/C are counted into the all-phase sum energy/power (P/Q/S).
#   1           EnPB                1: Corresponding Phase A/B/C to be counted into the all-phase sum energy/power (P/Q/S) (default)
#   0           EnPC                0: Corresponding Phase A/B/C not counted into the all-phase sum energy/power (P/Q/S)
# 
# Address: 33H
# Type: Read/Write
# Default Value: 0087H = 0b 0000 0000 1000 0111
MMode0      = 0x33 		# Metering Mode Config


# 15-6      -           Reserved.
# 5-0       PGA_GAIN    PGA gain for all ADC channels.
#                       Mapping:
#                           [5:4]: I3
#                           [3:2]: I2
#                           [1:0]: I1
#                       Encoding:
#                           00: 1X (default)
#                           01: 2X
#                           10: 4X
#                           11: N/A
#
# Address: 34H
# Type: Read/Write
# Default Value: 0000H
MMode1      = 0x34 		# PGA Gain Configuration for Current Channels

PStartTh    = 0x35 		# Startup Power Th (P)
QStartTh    = 0x36 		# Startup Power Th (Q)
SStartTh    = 0x37		# Startup Power Th (S)
PPhaseTh    = 0x38 		# Startup Power Accum Th (P)
QPhaseTh    = 0x39		# Startup Power Accum Th (Q)
SPhaseTh    = 0x3A		# Startup Power Accum Th (S)



''' CALIBRATION REGISTERS '''
PoffsetA    = 0x41 		# A Line Power Offset (P)
QoffsetA    = 0x42 		# A Line Power Offset (Q)
PoffsetB    = 0x43 		# B Line Power Offset (P)
QoffsetB    = 0x44 		# B Line Power Offset (Q)
PoffsetC    = 0x45 		# C Line Power Offset (P)
QoffsetC    = 0x46 		# C Line Power Offset (Q)
PQGainA     = 0x47 		# A Line Calibration Gain
PhiA        = 0x48  	# A Line Calibration Angle
PQGainB     = 0x49 		# B Line Calibration Gain
PhiB        = 0x4A  	# B Line Calibration Angle
PQGainC     = 0x4B 		# C Line Calibration Gain
PhiC        = 0x4C  	# C Line Calibration Angle

''' FUNDAMENTAL/HARMONIC ENERGY CALIBRATION REGISTERS '''
POffsetAF   = 0x51		# A Fund Power Offset (P)
POffsetBF   = 0x52		# B Fund Power Offset (P)
POffsetCF   = 0x53		# C Fund Power Offset (P)
PGainAF     = 0x54		# A Fund Power Gain (P)
PGainBF     = 0x55		# B Fund Power Gain (P)
PGainCF     = 0x56		# C Fund Power Gain (P)

''' MEASUREMENT CALIBRATION REGISTERS '''
UgainA      = 0x61 		# A Voltage RMS Gain
IgainA      = 0x62 		# A Current RMS Gain
UoffsetA    = 0x63 		# A Voltage Offset
IoffsetA    = 0x64 		# A Current Offset
UgainB      = 0x65 		# B Voltage RMS Gain
IgainB      = 0x66 		# B Current RMS Gain
UoffsetB    = 0x67 		# B Voltage Offset
IoffsetB    = 0x68 		# B Current Offset
UgainC      = 0x69 		# C Voltage RMS Gain
IgainC      = 0x6A 		# C Current RMS Gain
UoffsetC    = 0x6B 		# C Voltage Offset
IoffsetC    = 0x6C 		# C Current Offset
IoffsetN    = 0x6E 		# N Current Offset

''' ENERGY REGISTERS '''
APenergyT   = 0x80 		# Total Forward Active	
APenergyA   = 0x81 		# A Forward Active
APenergyB   = 0x82 		# B Forward Active
APenergyC   = 0x83 		# C Forward Active
ANenergyT   = 0x84 		# Total Reverse Active	
ANenergyA   = 0x85 		# A Reverse Active
ANenergyB   = 0x86 		# B Reverse Active
ANenergyC   = 0x87 		# C Reverse Active
RPenergyT   = 0x88 		# Total Forward Reactive
RPenergyA   = 0x89 		# A Forward Reactive
RPenergyB   = 0x8A 		# B Forward Reactive
RPenergyC   = 0x8B 		# C Forward Reactive
RNenergyT   = 0x8C 		# Total Reverse Reactive
RNenergyA   = 0x8D 		# A Reverse Reactive
RNenergyB   = 0x8E 		# B Reverse Reactive
RNenergyC   = 0x8F 		# C Reverse Reactive

SAenergyT   = 0x90 		# Total Apparent Energy
SenergyA    = 0x91 		# A Apparent Energy		
SenergyB    = 0x92 		# B Apparent Energy
SenergyC    = 0x93 		# C Apparent Energy


''' FUNDAMENTAL / HARMONIC ENERGY REGISTERS '''
APenergyTF  = 0xA0 	# Total Forward Fund. Energy
APenergyAF  = 0xA1 	# A Forward Fund. Energy
APenergyBF  = 0xA2 	# B Forward Fund. Energy
APenergyCF  = 0xA3 	# C Forward Fund. Energy
ANenergyTF  = 0xA4  # Total Reverse Fund Energy
ANenergyAF  = 0xA5 	# A Reverse Fund. Energy
ANenergyBF  = 0xA6 	# B Reverse Fund. Energy 
ANenergyCF  = 0xA7 	# C Reverse Fund. Energy
APenergyTH  = 0xA8 	# Total Forward Harm. Energy
APenergyAH  = 0xA9 	# A Forward Harm. Energy
APenergyBH  = 0xAA 	# B Forward Harm. Energy
APenergyCH  = 0xAB 	# C Forward Harm. Energy
ANenergyTH  = 0xAC 	# Total Reverse Harm. Energy
ANenergyAH  = 0xAD  # A Reverse Harm. Energy
ANenergyBH  = 0xAE  # B Reverse Harm. Energy
ANenergyCH  = 0xAF  # C Reverse Harm. Energy

''' POWER & P.F. REGISTERS '''
PmeanT      = 0xB0 		# Total Mean Power (P)
PmeanA      = 0xB1 		# A Mean Power (P)
PmeanB      = 0xB2 		# B Mean Power (P)
PmeanC      = 0xB3 		# C Mean Power (P)
QmeanT      = 0xB4 		# Total Mean Power (Q)
QmeanA      = 0xB5 		# A Mean Power (Q)
QmeanB      = 0xB6 		# B Mean Power (Q)
QmeanC      = 0xB7 		# C Mean Power (Q)
SmeanT      = 0xB8 		# Total Mean Power (S)
SmeanA      = 0xB9 		# A Mean Power (S)
SmeanB      = 0xBA 		# B Mean Power (S)
SmeanC      = 0xBB 		# C Mean Power (S)
PFmeanT     = 0xBC 		# Mean Power Factor
PFmeanA     = 0xBD 		# A Power Factor
PFmeanB     = 0xBE 		# B Power Factor
PFmeanC     = 0xBF 		# C Power Factor

PmeanTLSB   = 0xC0 		# Lower Word (Tot. Act. Power)
PmeanALSB   = 0xC1 		# Lower Word (A Act. Power)
PmeanBLSB   = 0xC2 		# Lower Word (B Act. Power)
PmeanCLSB   = 0xC3 		# Lower Word (C Act. Power)
QmeanTLSB   = 0xC4 		# Lower Word (Tot. React. Power)
QmeanALSB   = 0xC5 		# Lower Word (A React. Power)
QmeanBLSB   = 0xC6 		# Lower Word (B React. Power)
QmeanCLSB   = 0xC7 		# Lower Word (C React. Power)
SAmeanTLSB  = 0xC8 	    # Lower Word (Tot. App. Power)
SmeanALSB   = 0xC9 		# Lower Word (A App. Power)
SmeanBLSB   = 0xCA 		# Lower Word (B App. Power)
SmeanCLSB   = 0xCB 		# Lower Word (C App. Power)


''' FUND/HARM POWER & V/I RMS REGISTERS '''
PmeanTF     = 0xD0 		# Total Active Fund. Power
PmeanAF     = 0xD1 		# A Active Fund. Power
PmeanBF     = 0xD2 		# B Active Fund. Power
PmeanCF     = 0xD3 		# C Active Fund. Power
PmeanTH     = 0xD4 		# Total Active Harm. Power
PmeanAH     = 0xD5 		# A Active Harm. Power
PmeanBH     = 0xD6 		# B Active Harm. Power
PmeanCH     = 0xD7 		# C Active Harm. Power
UrmsA       = 0xD9 		# A RMS Voltage
UrmsB       = 0xDA 		# B RMS Voltage
UrmsC       = 0xDB 		# C RMS Voltage
IrmsN       = 0xDC 		# Calculated N RMS Current
IrmsA       = 0xDD 		# A RMS Current
IrmsB       = 0xDE 		# B RMS Current
IrmsC       = 0xDF 		# C RMS Current

PmeanTFLSB  = 0xE0		# Lower Word (Tot. Act. Fund. Power)
PmeanAFLSB  = 0xE1		# Lower Word (A Act. Fund. Power) 
PmeanBFLSB  = 0xE2		# Lower Word (B Act. Fund. Power)
PmeanCFLSB  = 0xE3		# Lower Word (C Act. Fund. Power)
PmeanTHLSB  = 0xE4		# Lower Word (Tot. Act. Harm. Power)
PmeanAHLSB  = 0xE5		# Lower Word (A Act. Harm. Power)
PmeanBHLSB  = 0xE6		# Lower Word (B Act. Harm. Power)
PmeanCHLSB  = 0xE7		# Lower Word (C Act. Harm. Power)
#           = 0xE8	    # Reserved Register 
UrmsALSB    = 0xE9		# Lower Word (A RMS Voltage)
UrmsBLSB    = 0xEA		# Lower Word (B RMS Voltage)
UrmsCLSB    = 0xEB		# Lower Word (C RMS Voltage)
#           = 0xEC	    # Reserved Register	
IrmsALSB    = 0xED		# Lower Word (A RMS Current)
IrmsBLSB    = 0xEE		# Lower Word (B RMS Current)
IrmsCLSB    = 0xEF		# Lower Word (C RMS Current)

''' PEAK, FREQUENCY, ANGLE & TEMP REGISTERS'''
UPeakA  = 0xF1 		# A Voltage Peak - THD+N on ATM90E36
UPeakB  = 0xF2 		# B Voltage Peak
UPeakC  = 0xF3 		# C Voltage Peak
#       = 0xF4	    # Reserved Register	
IPeakA  = 0xF5 		# A Current Peak
IPeakB  = 0xF6 		# B Current Peak
IPeakC  = 0xF7 		# C Current Peak
Freq    = 0xF8 		# Frequency
PAngleA = 0xF9 		# A Mean Phase Angle
PAngleB = 0xFA 		# B Mean Phase Angle
PAngleC = 0xFB 		# C Mean Phase Angle
Temp    = 0xFC		# Measured Temperature
UangleA = 0xFD		# A Voltage Phase Angle
UangleB = 0xFE		# B Voltage Phase Angle
UangleC = 0xFF		# C Voltage Phase Angle
