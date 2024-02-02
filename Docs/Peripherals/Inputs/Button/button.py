from pinout import * 

try:
    import RPi.GPIO as GPIO 
except RuntimeError:
    print( f'{__name__} error: RPi.GPIO import error - probably you not use the "sudo" statement to run the .py file')

RISING = GPIO.RISING 
FALLING = GPIO.FALLING
BOTH = GPIO.BOTH

class Button:
    gpio_name: str 
    gpio_num: int 

    state: bool 

    gpio_pull_up_en: bool 
    gpio_pull_down_en: bool 

    int_enabled: bool

    debug: bool

    def __init__( self, gpio_name: str, gpio_num: int, pull_up_en: bool = False, pull_down_en: bool = False, allow_warnings: bool = False, debug: bool = False ):
        self.gpio_name = gpio_name 
        self.gpio_num = gpio_num
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings( allow_warnings )
        
        if pull_up_en:
            self.gpio_pull_up_en = pull_up_en
            self.gpio_pull_down_en = not pull_up_en
            GPIO.setup( self.gpio_num, GPIO.IN, pull_up_down = GPIO.PUD_UP )
        elif pull_down_en:
            self.gpio_pull_down_en = pull_down_en
            self.gpio_pull_up_en = not pull_down_en
            GPIO.setup( self.gpio_num, GPIO.IN, pull_up_down = GPIO.PUD_DOWN )

        self.debug = debug
        self.state = False

        if self.debug:
            self.__str__()

    def __str__( self ):
        print( f"{self.gpio_name} / GPIO[{self.gpio_num}] = {self.get_state()}" )
     
    def get_state( self ) -> bool:
        self.gpio_state = GPIO.input( self.gpio_num )
        return self.gpio_state

    def set_interrupt( self, mode: str = "FALLING" ) -> bool:
        if mode == 'FALLING':
            mode = FALLING
        elif mode == 'RISING':
            mode = RISING
        elif mode == 'BOTH':
            mode = BOTH 
        else: 
            self.int_enabled = False
            return False     
        try:
            GPIO.add_event_detect( self.gpio_num, mode )
            self.int_enabled = True
            return True 
        except:
            self.int_enabled = False 
            return False 

    def remove_interrupt( self ) -> True:
        if self.int_enabled:
            GPIO.remove_event_detect( self.gpio_num )
            self.int_enabled = False 
            return True 
        else: 
            return False 

    def got_interrupt( self ) -> bool:
        if self.int_enabled:
            if GPIO.event_detected( self.gpio_num ):
                return True 
            else:
                return False 
        else: 
            return False
