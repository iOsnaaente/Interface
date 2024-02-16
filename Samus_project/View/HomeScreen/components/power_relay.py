from View.HomeScreen.components.common_peripherals import CommonPeripheral
from kivymd.uix.card import MDCard 
import os 

class PowerRelayContent( CommonPeripheral ):
    routine = None 
    grid = None 

    def __init__(self, gpio_list: list = [], *args, **kwargs):
        self.gpio_list = gpio_list 
        self.gpio_state = [ False for _ in range( len(self.gpio_list ) ) ] 
        super().__init__(*args, **kwargs)

    def on_kv_post( self, *arg, **kw ):
        self.ids.title.text = "Power Relay"
        self.ids.description.text = " "
        self.ids.image.source = self.img_path(  os.path.join('comp', 'comp_power_relay.png') )
        self.ids.image.angle = 90
        self.ids.peripheral_content.size_hint = [1, 0.75]
        self.ids.peripheral_content.add_widget(
            MDCard(
                
            )
        )