from  View.HomeScreen.components.common_peripherals import CommonPeripheral 
from kivy.clock import Clock 
import os 

from kivymd.uix.card import MDCard

img_path =  lambda file_name: os.path.join( os.path.dirname(__file__).removesuffix( '\\View\\HomeScreen\\components'), 'assets', 'images', file_name if type(file_name) == str else str(file_name) )

class RelayContent( CommonPeripheral ):
    relay_image: str = img_path( os.path.join('comp', 'comp_relay_out.png') )

    def __init__(self, relay_list: list = [], *args, **kwargs):
        self.relay_list = relay_list 
        self.relay_state = [ False for _ in range( len(self.relay_list ) ) ] 
        # self.routine = Clock.schedule_interval( self._att_relay, 0.1 )
        super().__init__(*args, **kwargs)

    def on_kv_post( self, *arg, **kw ):
        self.ids.image.source = self.relay_image 
        self.ids.title.text = 'RELAY OUT'
        self.ids.peripheral_content.add_widget( 
            MDCard(
                
            )
        )
        print( 'Relay OUT ')
        return super().on_kv_post( *arg, **kw ) 
