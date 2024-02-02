from pinout import * 

try:
    import RPi.GPIO as GPIO 
except RuntimeError:
    print( f'{__name__} error: RPi.GPIO import error - probably you not use the "sudo" statement to run the .py file')


class Relay:
	gpio_name: str 
	gpio_num: int 

	state: bool 

	debug: bool

	def __init__( self, gpio_name: str, gpio_num: int, initial_state: bool = False, allow_warnings: bool = False, debug: bool = False ):
		self.gpio_name = gpio_name 
		self.gpio_num = gpio_num
		self.state = initial_state
		self.debug = debug 

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings( allow_warnings )
		GPIO.setup( self.gpio_num, GPIO.OUT )
		GPIO.output( self.gpio_num, self.state ) 
        
		if self.debug:
			self.__str__()

	def __str__( self ):
		print( f"{self.gpio_name} / GPIO[{self.gpio_num}] = {self.state}" )

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

	def on( self ) -> bool:
		return self.set_state( True )

	def off( self ) -> bool:
		return self.set_state( False )