from kivymd.uix.button import MDRoundFlatIconButton
from kivymd.icon_definitions import md_icons
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard 
from kivy.clock import Clock 
from kivy.metrics import sp 

KV_FILE = ''' 
<GPIOOUTContent@MDCard>:
    md_bg_color: [0.5, 1, 0.5, 0.25 ]
    pos_hint: {'center_x': 0.5,'center_y': 0.5}
    size_hint: 1, 1
    orientation: 'vertical'  
    MDLabel:
        size_hint: 0.75, 0.05
    MDLabel:
        size_hint: 1, 0.05
        text: "GPIO OUT"
        halign: "center"
        font_size: sp(16)
        theme_text_color: "Custom"
        text_color: 'black'    
    MDLabel:
        size_hint: 0.75, 0.05
        pos_hint: {'center_x': 0.5,'center_y': 0.5}
        text: "Saídas digitais de propósito geral, podem ser usadas como bem entender, para atender demandas gerais como acionamento de cargas digitais ou entradas de periféricos adicionais como medidores ou sensores auxiliares."
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
                size_hint: 1, 0.6
                pos_hint: {'center_x': 0.5,'center_y': 0.5}
                source: root.gpio_out
                allow_stretch: True   
                keep_ratio: False
        MDBoxLayout:
            orientation: 'vertical'
            size_hint: 0.8, 0.9
            pos_hint: {'center_x': 0.5,'center_y': 0.5} 
            MDGridLayout:
                size_hint: 0.9, 0.1
                pos_hint: {'center_x': 0.5,'center_y': 0.5} 
                padding: sp(10)
                spacing: sp(10)
                cols: 3 
                MDCard:
                    md_bg_color: [0.5, 1, 0.5, 0.9]
                    MDLabel:
                        text: 'GPIO'
                        halign: "center"
                        font_size: sp(16)
                        theme_text_color: "Custom"
                        text_color: 'black' 
                        bold: True
                MDCard:
                    md_bg_color: [0.5, 1, 0.5, 0.9]
                    MDLabel:
                        text: 'Stado'
                        halign: "center"
                        font_size: sp(16)
                        theme_text_color: "Custom"
                        text_color: 'black' 
                        bold: True
                MDCard:
                    md_bg_color: [0.5, 1, 0.5, 0.9]
                    MDLabel:
                        text: 'Force'
                        halign: "center"
                        font_size: sp(16)
                        theme_text_color: "Custom"
                        text_color: 'black' 
                        bold: True

            MDGridLayout:
                id: gpio_out_content 
                size_hint: 0.9, 0.9
                pos_hint: {'center_x': 0.5,'center_y': 0.5} 
                padding: sp(10)
                spacing: sp(10)
                cols: 3 
'''

import os 
img_path =  lambda file_name: os.path.join( os.path.dirname(__file__).removesuffix( '\\View\\HomeScreen\\components'), 'assets', 'images', file_name if type(file_name) == str else str(file_name) )

from kivy.lang import Builder
Builder.load_string(KV_FILE)

class GPIOOUTContent( MDCard ):
    gpio_out: str = img_path( os.path.join('comp', 'comp_gpio_out.png') )

    def __init__(self, gpio_list: list = [], *args, **kwargs):
        self.gpio_list = gpio_list 
        self.gpio_state = [ False for _ in range( len(self.gpio_list ) ) ] 
        self.routine = Clock.schedule_interval( self.att_gpio, 0.1 )
        
        super().__init__(*args, **kwargs)

    def on_kv_post( self, *arg, **kw ):
        self.att_gpio_out() 
        return super().on_kv_post( *arg, **kw ) 

    def att_gpio_out( self ) -> None:
        self.ids.gpio_out_content.children = [] 
        for gpio, state in zip(self.gpio_list, self.gpio_state):
            wid_name = MDCard( md_bg_color = [0.5, 1, 0.5, 0.250] ) 
            wid_name.add_widget( 
                MDLabel(
                    text  = "GPIO" + str(gpio), 
                    halign = "center", 
                    font_size = sp(16), 
                    theme_text_color = "Custom", 
                    text_color = 'black',  
                    bold = True )
            )            
            wid_state = MDCard( md_bg_color = [0.5, 1, 0.5, 0.250] ) 
            wid_state.add_widget( 
                MDLabel(
                    text  = 'HIGH' if state else 'LOW', 
                    halign = "center", 
                    font_size = sp(16), 
                    theme_text_color = "Custom", 
                    text_color = 'black',  
                    bold = True )
            )
            wid_butt = MDCard( md_bg_color = [0.5, 1, 0.5, 0.25 ], on_press = self.set_gpio, name = str(gpio) )
            wid_butt.add_widget( 
                MDLabel(
                    text  = 'Turn Off' if state else 'Turn On', 
                    halign = "center", 
                    font_size = sp(16), 
                    theme_text_color = "Custom", 
                    text_color = 'black',  
                    bold = True             
                )
            ) 
            self.ids.gpio_out_content.add_widget( wid_name )
            self.ids.gpio_out_content.add_widget( wid_state )
            self.ids.gpio_out_content.add_widget( wid_butt )
    

    def get_gpio( self, num: int ) -> bool:
        for ind, gpio in enumerate(self.gpio_list):
            if str(gpio) == str(num):
                return self.gpio_state[ind]

    def set_gpio( self, obj = None ):
        print( f'Set gpio [{obj.name}] with value { not self.get_gpio( int(obj.name) ) }')
        for ind, gpio in enumerate(self.gpio_list):
            if str(gpio) == obj.name:
                self.gpio_state[ind] = not self.gpio_state[ind]
    
    def att_gpio( self, clock_event ) -> None:
        changed = False 
        for gpio, old_state in zip( self.gpio_list, self.gpio_state):
            state = self.get_gpio( gpio )
            if old_state != state:
                print( 'GPIO CHANGED' ) 
                changed = True 
                break 
        if changed:
            self.att_gpio_out()
        
        