from View.HomeScreen.components.common_peripherals import CommonPeripheral 
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard 
from kivy.clock import Clock 
from kivy.metrics import sp 
import os 

class GPIOOUTContent( CommonPeripheral ):
    routine = None 
    grid = None 

    def __init__(self, gpio_list: list = [], *args, **kwargs):
        self.gpio_list = gpio_list 
        self.gpio_state = [ False for _ in range( len(self.gpio_list ) ) ] 
        super().__init__(*args, **kwargs)

    def on_kv_post( self, *arg, **kw ):
        self.ids.title.text = "GPIO OUT"
        self.ids.description.text = "Saídas digitais de propósito geral, podem ser usadas como bem entender, para atender demandas gerais como acionamento de cargas digitais ou entradas de periféricos adicionais como medidores ou sensores auxiliares."
        self.ids.image.source = self.img_path(  os.path.join('comp', 'comp_gpio_out.png') )
        self.ids.peripheral_content.size_hint = [1, 0.75]
        label = MDGridLayout(
                size_hint = [0.9, 0.2 ],
                pos_hint = {'center_x': 0.5,'center_y': 0.5} ,
                padding = sp(10),
                spacing = sp(10),
                cols = 3 ,
        )
        for title in [ 'GPIO', 'State', 'Force']:
            card = MDCard( md_bg_color = [0.5, 1, 0.5, 0.9] )
            card.add_widget( 
                MDLabel(
                    text = title,
                    halign = "center",
                    font_size = sp(16),
                    theme_text_color = "Custom",
                    text_color = 'black' ,
                    bold = True,
                )
            )
            label.add_widget( card )
        self.ids.peripheral_content.add_widget( label ) 
        self.grid = MDGridLayout(
                size_hint = [0.9, 0.9],
                pos_hint = {'center_x': 0.5,'center_y': 0.5} ,
                padding = sp(10),
                spacing = sp(10),
                cols = 3
        )
        self.ids.peripheral_content.add_widget( self.grid ) 
        self.routine = Clock.schedule_interval( self.att_gpio, 0.1 )
        self.att_gpio_out() 
        return super().on_kv_post( *arg, **kw ) 

    def att_gpio_out( self ) -> None:
        self.grid.children = [] 
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
            self.grid.add_widget( wid_name )
            self.grid.add_widget( wid_state )
            self.grid.add_widget( wid_butt )
    

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
        
        