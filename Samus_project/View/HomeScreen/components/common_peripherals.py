KV_FILE = ''' 
<CommonPeripheral@MDCard>:
    id: source 
    md_bg_color: [0.5, 1, 0.5, 0.25 ]
    pos_hint: {'center_x': 0.5,'center_y': 0.5}
    size_hint: 1, 1
    orientation: 'vertical'
    spacing: sp(10)  
    padding: sp(20)

    MDLabel:
        id: title
        pos_hint: {'center_x': 0.5,'center_y': 0.5}
        size_hint: 1, 0.075
        halign: "center"
        text: "title"
        font_size: sp(16)
        theme_text_color: "Custom"
        text_color: 'black' 

    MDLabel:
        id: description 
        size_hint: 1, 0.125
        pos_hint: {'center_x': 0.5,'center_y': 0.5}
        text: "Description"
        halign: "center"
        font_size: sp(12)
        theme_text_color: "Custom"
        text_color: 'black'

    MDBoxLayout:
        orientation: 'horizontal'
        # padding: sp(20), 0, 0, 0
        spacing: sp(10)

        MDBoxLayout:
            id: image_box 
            size_hint: 0.25, 1
            Image:  
                id: image 
                radius: 10 
                size_hint: 1, 1
                pos_hint: {'center_x': 0.5,'center_y': 0.5}
                mipmap: True 
                keep_ratio: True
                allow_stretch: False   
                source: 

        MDBoxLayout:
            id: peripheral_content 
            orientation: 'vertical'
            size_hint: 0.75, 1
            pos_hint: {'center_x': 0.5,'center_y': 0.5}
'''

from kivymd.uix.card import MDCard 
from kivy.lang import Builder
import os 

Builder.load_string(KV_FILE)

class CommonPeripheral( MDCard ):
    img_path =  lambda obj, file_name:  os.path.join( os.path.dirname(__file__).removesuffix( '\\View\\HomeScreen\\components'), 'assets', 'images', file_name if type(file_name) == str else str(file_name) )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def on_kv_post( self, *arg, **kw ):
        print( 'Common peripherals')
        return super().on_kv_post( *arg, **kw ) 

        