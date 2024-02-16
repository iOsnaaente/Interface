from View.HomeScreen.components.common_peripherals import CommonPeripheral 
from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.icon_definitions import md_icons
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard 
from kivy.clock import Clock 
from kivy.metrics import sp 
import os 


class GPIOINContent( CommonPeripheral ):

    routine = None 
    grid = None

    def __init__(self, gpio_list: list = [], *args, **kwargs):
        self.gpio_list = gpio_list 
        self.gpio_state = [ False for _ in range( len(self.gpio_list ) ) ] 
        super().__init__(*args, **kwargs)
        
    def on_kv_post( self, *arg, **kw ):
        self.ids.title.text = "GPIO IN"
        self.ids.description.text = "As entradas digitais são utilizadas para a detecção de chaves fim de curso ou sensores de input para sinalizar etapas de operação. O Giga de testes utiliza duas chaves fim de curso para dar inicio ao processo de medição das cargas. Uma terceira entrada digital de propósito geral ainda pode ser utilizada."
        self.ids.image.source = self.img_path( os.path.join('comp', 'comp_gpio_in.png') )
        self.ids.peripheral_content.size_hint = [1, 0.30]
        cont  = MDCard(
            size_hint = [1.0, 0.35],
            pos_hint = {'center_x': 0.5,'center_y': 0.5} ,
            orientation = 'vertical',
            padding = sp(20),
            spacing = sp(10),
            md_bg_color = [0.5, 1, 0.5, 0.9],
        )
        cont.add_widget( 
            MDLabel(
                text = 'GPIO State',
                size_hint = [1, 1],
                halign = "center",
                font_size = sp(16),
                theme_text_color = "Custom",
                text_color = 'black' ,
                bold = True,
            )
        )
        self.grid = MDGridLayout(
            size_hint = [1.0, 0.65],
            pos_hint = {'center_x': 0.5,'center_y': 0.5} ,
            padding = [0, sp(10), 0, 0 ],
            spacing = sp(10),
            cols = 3
        )
        self.ids.peripheral_content.add_widget( cont ) 
        self.ids.peripheral_content.add_widget( self.grid ) 
        self.att_gpio() 

        self.routine = Clock.schedule_interval( self._att_gpio, 0.1 )
        return super().on_kv_post( *arg, **kw ) 

    def _att_gpio( self, clock_event = None ) -> None:
        changed = False 
        for gpio, old_state in zip( self.gpio_list, self.gpio_state):
            state = self.get_gpio( gpio )
            if old_state != state:
                print( 'GPIO CHANGED' ) 
                changed = True 
                break 
        if changed:
            self.att_gpio_out()

    def att_gpio( self ) -> None:
        self.grid.children = [] 
        for gpio, state in zip(self.gpio_list, self.gpio_state):
            wid_name = MDCard( 
                md_bg_color = [0.5, 1, 0.5, 0.50 ] if state else [1, 0.5, 0.5, 0.5 ],
                height = self.width,
                radius = self.height/2
            ) 
            wid_name.add_widget( 
                MDLabel(
                    text  = "GPIO" + str(gpio) + '\n' + str(state), 
                    halign = "center", 
                    font_size = sp(16), 
                    theme_text_color = "Custom", 
                    text_color = 'black',  
                    bold = True )
            )            
            self.grid.add_widget( wid_name )
    

    def get_gpio( self, num: int ) -> bool:
        for ind, gpio in enumerate(self.gpio_list):
            if str(gpio) == str(num):
                return self.gpio_state[ind]
    
        
        