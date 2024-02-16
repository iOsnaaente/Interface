from View.HomeScreen.components.common_peripherals import CommonPeripheral
from kivymd.uix.card import MDCard 
import os 

class PowerMeterContent( CommonPeripheral ):
    routine = None 
    grid = None 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_kv_post( self, *arg, **kw ):
        self.ids.title.text = "Medidor de energia"
        self.ids.description.text = "O medidor de energia baseado no ATM90E32 possui uma série de registradores que registram os estados do CI medidor, entregando informações como energia ativa, energia aparente, temperatura, angulo de fase e muitos outros. Abaixo possui uma lista dos registradores disponíveis e que podem ser lidos de acordo com a necessidade de uso."
        self.ids.image.source = self.img_path(  os.path.join('comp', 'comp_power_sensor.png') )
        self.ids.peripheral_content.size_hint = [1, 0.75]
        self.ids.peripheral_content.add_widget(
            MDCard(
                
            )
        )