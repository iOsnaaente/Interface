try:
    import RPi.GPIO as GPIO 
except RuntimeError:
    print( f'{__name__} error: RPi.GPIO import error - probably you not use the "sudo" statement to run the .py file')


class LED:
    gpio_name: str 
    gpio_num: int 

    gpio_state: bool 

    gpio_pwm: GPIO.PWM
    pwm_frequency: int 
    pwm_duty: int 
    pwm_enabled: bool 

    debug: bool

    def __init__( self, gpio_name: str, gpio_num: int, initial_state: bool = False, allow_warnings: bool = False, debug: bool = False ):
        self.gpio_name = gpio_name 
        self.gpio_num = gpio_num
        self.gpio_state = initial_state
        self.debug = debug 

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings( allow_warnings )

        GPIO.setup( self.gpio_num, GPIO.OUT )
        GPIO.output( self.gpio_num, self.gpio_state ) 
        
        if self.debug:
            print( f"{self.gpio_name}/GPIO[{self.gpio_num}] initiated" )

    def __str__( self ):
        print( f"{self.gpio_name} / GPIO[{self.gpio_num}] = {self.gpio_state}" )

    def set_state( self, state: bool ) -> bool:
        self.gpio_state = state 
        try:
            GPIO.output( self.gpio_num, self.gpio_state )
            return True
        except:
            return False
         
    def get_state( self ) -> bool:
        self.gpio_state = GPIO.input( self.gpio_num )
        return self.gpio_state

    def set_pwm( self, frequency: int = 1000, initial_duty: int = -1 ) -> bool:
        self.pwm_frequency = frequency
        if self.pwm_frequency == 0:
            self.pwm_enabled = False
            return self.pwm_enabled
        else:
            self.pwm_enabled = True
        
        GPIO.setup( self.gpio_num, GPIO.OUT )
        self.gpio_pwm = GPIO.PWM( self.gpio_num, self.pwm_frequency )
        if initial_duty == -1:
            self.set_duty( 50 )
        else: 
            self.set_duty( initial_duty )
        self.gpio_pwm.start( self.pwm_enabled )
        return self.pwm_enabled

    def set_duty( self, duty: int ) -> None:
        if duty > 100:
            duty = 100 
        elif duty < 0:
            duty = 0 
        self.pwm_duty = duty 
        self.gpio_pwm.ChangeDutyCycle( self.pwm_duty )

        
