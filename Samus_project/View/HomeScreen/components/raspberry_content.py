from kivymd.uix.card import MDCard 
from kivy.lang import Builder

KV_FILE = '''
<RaspberryContent@MDCard>:
    md_bg_color: [0.5, 1, 0.5, 0.5 ]
    pos_hint: {'center_x': 0.5,'center_y': 0.5}
    size_hint: 1, 1
    orientation: 'vertical'
    MDLabel:
        size_hint: 1, 0.1
        text: "Raspberry pinout"
        halign: "center"
        font_size: sp(10)
        theme_text_color: "Custom"
        text_color: 'black'
    MDBoxLayout:
        orientation: 'horizontal'
        MDBoxLayout:
            size_hint: 0.30, 1
            FitImage:
                radius: 0 
                size_hint: 1, 0.6
                pos_hint: {'center_x': 0.5,'center_y': 0.5}
                source: root.raspy_top
                allow_stretch: True   
                keep_ratio: True
        MDBoxLayout:
            id: raspy_table 
            orientation: 'vertical'
            size_hint: 0.70, 0.9
            pos_hint: {'center_x': 0.5,'center_y': 0.5}
'''

import os 
img_path =  lambda file_name: os.path.join( os.path.dirname(__file__).removesuffix( '\\View\\HomeScreen\\components'), 'assets', 'images', file_name if type(file_name) == str else str(file_name) )

Builder.load_string(KV_FILE)

class RaspberryContent( MDCard ):    
    raspy_top: str = img_path( 'raspy_top.png' )    

