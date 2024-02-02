"""
    Description: Adaptação da biblioteca ATM90E32 para Python
    Author: Bruno G. F. Sampaio 
    email: bruno.bielsam.1205@hotmail.com
    date: 17/12/2023
    version: 1.2.1
    Rev: 0.2
"""

from Inputs.Button.button import Button 
from Outputs.Relay.relay import Relay 
from Power_sensor.pm import ATM90E32

import time 

# Estados de operação do PM 
FAIL_STATE = -1 
INICIALIZANDO = 0 
CALIBRANDO = 1 
MEDINDO = 2 
MEDIDO = 3
OCIOSO = 4

# GPIOs usadas 
ZERO_CROSS_GPIO = 25 
RELAY_GPIO_N = 5
RELAY_GPIO_F = 6

# Obtidas através de calibração 
U_GAIN = 3920
I_GAIN = 39473
FREQ   = 60


class PowerSensor:
    # Inicializando 
    # Calibrando 
    # Medindo 
    # Idle 
    state: int 

    # Medidor de energia 
    pm: ATM90E32 

    # Reles para desativar energia 
    relay_F: Relay 
    relay_N: Relay 

    # Pino de Zero cross 
    zero_cross: Button

    # Permitir Debug ao longo da execução 
    debug: bool  

    def __init__( self, debug: bool = False ) -> None:
        self.debug = debug

        # Configura o Medidor de energia nos pinos padrões 
        self.pm = ATM90E32( debug = self.debug )
        # Configura os pinos dos relés 
        self.relay_F = Relay( 'Relé de Fase', RELAY_GPIO_F, initial_state = False, debug = self.debug )
        self.relay_N = Relay( 'Relé de Neutro', RELAY_GPIO_N, initial_state = False )
        # Configura o pino de Zero cross com PullDown 
        self.zero_cross = Button( "Detector de Zero cross", ZERO_CROSS_GPIO, pull_up_en = False, pull_down_en = True, debug = self.debug )

        self.state = INICIALIZANDO
    
        # Inicializando o medidor de energia 
        self.pm.begin( FREQ, 0, U_GAIN, I_GAIN, I_GAIN, 200 )
        if self.status():
            self.state = OCIOSO 
        else: 
            self.state = FAIL_STATE 

    def wait_zero_cross( self, timeout_ms: int = 1000 ):
        try: 
            self.zero_cross.remove_interrupt()
        except:
            pass 
        finally:
            self.zero_cross.set_interrupt( "RISING" )
        # timeout return 
        t0 = time.time()
        # Redundância 
        cnt = 0
        while True: 
            if self.zero_cross.got_interrupt():
                self.zero_cross.remove_interrupt()
                return True 
            else:
                if (time.time() - t0) > timeout_ms/1000:
                    if self.debug:
                        print( f"{__name__} error in wait_zero_cross: timeout" )
                    return False 
            cnt += 1
            if cnt > 1_000_000:
                print( f'{__name__} error in wait_zero_cross(): exit by redundancy')
                return False


    ''' Estado do medidor de energia '''
    def enable_power_metering( self ):
        self.pm.enable_power_metering()

    def disable_power_metering( self ):
        self.pm.disable_power_metering() 


    ''' Estados do relé Neutro '''
    def turn_on_relay_N( self, timeout_zero_cross: int = 1000 ) -> bool:
        if self.wait_zero_cross( timeout_zero_cross ):
            self.relay_N.on()
            return True
        else: 
            return False 
    def turn_off_relay_N( self, timeout_zero_cross: int = 1000 ) -> bool:
        if self.wait_zero_cross( timeout_zero_cross ):
            self.relay_N.off()
            return True
        else: 
            return False 

    ''' Estados do relé Fase - Sem Zero Cross pois ele interrompe o Zero cross '''
    def turn_on_relay_F( self ):
        self.relay_F.on()
    def turn_off_relay_F( self ):
        self.relay_F.off()
    

    ''' Verifica o estado do medidor de energia '''
    def status( self ) -> bool:
        # Leitura dos registradores de status do CI
        sys0 = self.pm.get_sys_status_0()  # EMMState0
        sys1 = self.pm.get_sys_status_1()  # EMMState1
        en0 = self.pm.get_meter_status_0() # EMMIntState0
        en1 = self.pm.get_meter_status_1() # EMMIntState1
        if self.debug:
            print( f"Sys Status: 0x{sys0}{sys1}\tMeter Status: 0x{en0}{en1}" )

        # Verifica se o CI esta conectado ou possui algum erro de medição  
        if sys0 == 0xFFFF or sys0 == 0x0000:
            if self.debug:
                print( "Error: Not receiving data from energy meter - check your connections" )
            return False 
        else: 
            return True     
    
    ''' Realiza a rotina de leitura de uma lista de registradores '''
    def measure_addrs( self, addrs_to_get: list, num_mean: int = 10 ) -> dict:
        measures = {
            addr: {'values': [], 'mean': 0} for addr in addrs_to_get
        }
        if self.status:
            # Pega o valor de leitura de cada registrador 
            for _ in range( num_mean ):
                for addr in addrs_to_get:
                    value = self.pm.read16bits(addr)
                    measures[addr]['values'].append(value)
            # Calcula a média dos valores lidos para cada endereço
            for addr, data in measures.items():
                data['mean'] = sum(data['values']) / len(data['values'])
        return measures
    
    def routine( self, addrs_to_get: list, num_mean: int = 10 ) -> dict:
        try:
            read = {
                addr: {'values': [], 'mean': 0} for addr in addrs_to_get
            }
            if self.status():
                self.state = MEDINDO 
                # Liga os relés de medição 
                self.turn_on_relay_F()
                if not self.turn_on_relay_N():
                    return False 
                # Habilita a medição 
                self.enable_power_metering()
                time.sleep( 100 / 1_000 ) # 100 ms  
                # Realiza as medições 
                read = self.measure_addrs( addrs_to_get, num_mean )
                # Desabilita as medições 
                self.disable_power_metering()
                # Desliga os relés            
                self.turn_off_relay_N()
                self.turn_off_relay_F()
                self.state = MEDIDO
            else: 
                self.state = FAIL_STATE 
        except:  
            self.disable_power_metering()
            self.turn_off_relay_F()     
            self.turn_off_relay_N()     
        finally:
            return read 
