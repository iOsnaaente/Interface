from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.icon_definitions import md_icons
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard 
from kivy.clock import Clock 
from kivy.metrics import sp 

KV_FILE = ''' 
<RelayOUTContent@MDCard>:
    md_bg_color: [0.5, 1, 0.5, 0.25 ]
    pos_hint: {'center_x': 0.5,'center_y': 0.5}
    size_hint: 1, 1
    orientation: 'vertical'
    spacing: sp(10)  
    MDLabel:
        size_hint: 0.75, 0.05
    MDLabel:
        size_hint: 1, 0.05
        text: "GPIO IN"
        halign: "center"
        font_size: sp(16)
        theme_text_color: "Custom"
        text_color: 'black'    
    MDLabel:
        size_hint: 0.75, 0.05
        pos_hint: {'center_x': 0.5,'center_y': 0.5}
        text: "As entradas digitais são utilizadas para a detecção de chaves fim de curso ou sensores de input para sinalizar etapas de operação. O Giga de testes utiliza duas chaves fim de curso para dar inicio ao processo de medição das cargas. Uma terceira entrada digital de propósito geral ainda pode ser utilizada."
        halign: "center"
        font_size: sp(12)
        theme_text_color: "Custom"
        text_color: 'black'
    MDBoxLayout:
        orientation: 'horizontal'
        padding: sp(20), 0, 0, 0
        MDBoxLayout:
            size_hint: 0.2, 1
            Image:
                radius: 10 
                size_hint: 1, 0.3
                pos_hint: {'center_x': 0.5,'center_y': 0.5}
                source: root.comp_relay_out
                allow_stretch: True   
                keep_ratio: False
        MDBoxLayout:
            orientation: 'vertical'
            size_hint: 0.8, 0.9
            pos_hint: {'center_x': 0.5,'center_y': 0.5} 
            MDBoxLayout:
            MDCard:
                size_hint: 0.9, None
                pos_hint: {'center_x': 0.5,'center_y': 0.5} 
                padding: sp(10)
                spacing: sp(10)
                height: sp(50)
                md_bg_color: [0.5, 1, 0.5, 0.9]
                MDLabel:
                    text: 'GPIO State'
                    size_hint: 1, 1
                    halign: "center"
                    font_size: sp(16)
                    theme_text_color: "Custom"
                    text_color: 'black' 
                    bold: True
            MDGridLayout:
                id: gpio_in_content 
                size_hint: 0.9, None
                pos_hint: {'center_x': 0.5,'center_y': 0.5} 
                padding: 0, sp(10), 0, 0 
                spacing: sp(10)
                cols: 3 
            MDBoxLayout:
'''

import os 
img_path =  lambda file_name: os.path.join( os.path.dirname(__file__).removesuffix( '\\View\\HomeScreen\\components'), 'assets', 'images', file_name if type(file_name) == str else str(file_name) )

from kivy.lang import Builder
Builder.load_string(KV_FILE)

class RelayOUTContent( MDCard ):
    gpio_in: str = img_path( os.path.join('comp', 'comp_gpio_in.png') )

    def __init__(self, gpio_list: list = [], *args, **kwargs):
        self.gpio_list = gpio_list 
        self.gpio_state = [ False for _ in range( len(self.gpio_list ) ) ] 
        self.routine = Clock.schedule_interval( self._att_gpio, 0.1 )
        super().__init__(*args, **kwargs)

    def on_kv_post( self, *arg, **kw ):
        self.att_gpio() 
        return super().on_kv_post( *arg, **kw ) 

    def att_gpio( self ) -> None:
        self.ids.gpio_in_content.children = [] 
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
            self.ids.gpio_in_content.add_widget( wid_name )
    

    def get_gpio( self, num: int ) -> bool:
        for ind, gpio in enumerate(self.gpio_list):
            if str(gpio) == str(num):
                return self.gpio_state[ind]
    
    def _att_gpio( self, clock_event ) -> None:
        changed = False 
        for gpio, old_state in zip( self.gpio_list, self.gpio_state):
            state = self.get_gpio( gpio )
            if old_state != state:
                print( 'GPIO CHANGED' ) 
                changed = True 
                break 
        if changed:
            self.att_gpio_out()
        
        