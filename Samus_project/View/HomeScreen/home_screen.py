from View.base_screen import BaseScreenView
from View.base_screen import SwipeScreen

from kivygo.uix.frostedglass import FrostedGlass 
from kivy.clock import Clock 
import os 

from View.HomeScreen.components.raspberry_content import RaspberryContent 
from View.HomeScreen.components.gpio_out_content import GPIOOUTContent  
from View.HomeScreen.components.gpio_in_content import GPIOINContent 
from View.HomeScreen.components.power_meter import PowerMeterContent 
from View.HomeScreen.components.power_relay import PowerRelayContent 
from View.HomeScreen.components.relays_out import RelayContent 
from View.HomeScreen.components.led_rgb import LedRGBContent 



img_path =  lambda file_name: os.path.join( os.path.dirname(__file__).removesuffix( '\\View\\HomeScreen'), 'assets', 'images', file_name if type(file_name) == str else str(file_name) )
hover_offset = 0.25

board_top: str = img_path( 'board_top.png' )
raspy_top: str = img_path( 'raspy_top.png' )
raspy_bot: str = img_path( 'raspy_bot.png' )

class HomeScreenView( BaseScreenView, SwipeScreen ):

    board_top: str = img_path( 'board_top.png' )
    raspy_top: str = img_path( 'raspy_top.png' )
    raspy_bot: str = img_path( 'raspy_bot.png' )

    connector_gpio_out_color: list = [ 0.25,    1, 0.25, 0.10 ]
    connector_gpio_in_color: list  = [    1,    1, 0.25, 0.10 ]
    connector_power_in_color: list = [    1, 0.25, 0.25, 0.10 ]
    raspberry_board_color: list    = [ 0.25,    1, 0.25, 0.10 ]
    relays_power_in_color: list    = [    1, 0.25, 0.25, 0.10 ]
    power_sensor_color: list       = [ 0.25, 0.25,    1, 0.20 ]
    relays_out_color: list         = [ 0.25,    1, 0.25, 0.10 ]
    leds_rgb: list                 = [    1, 0.25, 0.25, 0.10 ]

    connector_gpio_out_color_hover_in: list = [ 0.25,    1, 0.25, hover_offset ]
    connector_gpio_in_color_hover_in: list  = [    1,    1, 0.25, hover_offset ]
    connector_power_in_color_hover_in: list = [    1, 0.25, 0.25, hover_offset ]
    raspberry_board_color_hover_in: list    = [ 0.25,    1, 0.25, hover_offset ]
    power_sensor_color_hover_in: list       = [ 0.25, 0.25,    1, hover_offset ]
    relays_power_in_color_hover_in: list    = [    1, 0.25, 0.25, hover_offset ]
    relays_out_color_hover_in: list         = [ 0.25,    1, 0.25, hover_offset ]
    leds_rgb_hover_in: list                 = [    1, 0.25, 0.25, hover_offset ]

    selection_option: str = "None" 

    def clicked( self, obj, state: bool ) -> None:
        if state:
            obj.md_bg_color = obj.md_bg_color[:-1] + [hover_offset]
            obj.border, obj.border_color = 2, [0, 0, 0, 1]
            self.selection_option = obj.name
            Clock.schedule_once( self.selection, 0.1 )
        else:
            obj.md_bg_color = obj.md_bg_color[:-1] + [0.10]
            obj.border, obj.border_color = 0, [0, 0, 0, 0]


    def selection( self, args = None ) -> None:
        obj = self.ids.main_content 
        for chl in obj.children:
            obj.remove_widget( chl )
        print( self.selection_option )
        if self.selection_option == 'RASPBERRY':
            widget = RaspberryContent()
        elif self.selection_option == 'RELAY OUT':
            widget = RelayContent( relay_list = [1, 2, 3] )
        elif self.selection_option == 'GPIO OUT':
            widget = GPIOOUTContent( [1, 2, 3, 4] )
        elif self.selection_option == 'LED RGB':
            widget = LedRGBContent( gpio_list = [ 1, 2, 3] ) 
        elif self.selection_option == 'GPIO IN':
            widget = GPIOINContent( gpio_list = [1, 2, 3] )
        elif self.selection_option == 'POWER SENSOR':
            widget = PowerMeterContent() 
        elif self.selection_option == 'POWER RELAY':
            widget = PowerRelayContent( gpio_list = [ 1, 2 ] ) 
        else: 
            return 
        self.ids.main_content.add_widget( widget )



    def on_kv_post( self, *arg, **kw ):
        return super().on_kv_post( *arg, **kw ) 

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
