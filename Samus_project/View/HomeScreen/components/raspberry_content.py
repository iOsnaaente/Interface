from View.HomeScreen.components.common_peripherals import CommonPeripheral
from kivymd.uix.card import MDCard 
import os 

class RaspberryContent( CommonPeripheral ):
    routine = None 
    grid = None 

    def __init__(self, gpio_list: list = [], *args, **kwargs):
        self.gpio_list = gpio_list 
        self.gpio_state = [ False for _ in range( len(self.gpio_list ) ) ] 
        super().__init__(*args, **kwargs)

    def on_kv_post( self, *arg, **kw ):
        self.ids.title.text = "Raspberry Pi"
        self.ids.description.text = "Por ser o microprocessador do sistema, o Raspeberry Pi possui funções importantes a serem considaradas, ..... CONTINUAR "
        self.ids.image.source = self.img_path(  os.path.join('comp', 'comp_raspy_top.png') )
        self.ids.peripheral_content.size_hint = [1, 0.75]
        self.ids.peripheral_content.add_widget(
            MDCard(
                
            )
        )