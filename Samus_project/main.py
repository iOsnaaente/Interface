from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import WipeTransition
from kivymd.tools.hotreload.app import MDApp
from kivy.utils import rgba, QueryDict 

from screeninfo import get_monitors
try: 
    monitor = get_monitors()[0]
except:
    monitor = get_monitors()[1]

from kivy.core.window import Window
Window.size = ( monitor.width, monitor.height )
Window.left = monitor.x
Window.top = monitor.y + 25

# Inicia em modo Tela Cheia 
Window.fullscreen = 'auto'

import importlib
import os 

PATH =  os.path.dirname( __file__ ) 


class Samus(MDApp):
    
    KV_FILES = [
        PATH + '/View/HomeScreen/home_screen.kv'
    ]

    CLASSES = { 'ManagerScreens': 'manager_screens' }
    AUTORELOADER_PATHS = [ os.getcwd(), { 'recursive': True } ]

    def build_app(self) -> MDScreenManager:
        import View.screens
        self.manager_screens = MDScreenManager()

        Window.bind( on_key_down = self.on_keyboard_down )
        
        importlib.reload( View.screens )
        screens = View.screens.screens

        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)
        
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.accent_palette = "DeepOrange"        
        self.theme_cls.primary_hue = '400'
        self.theme_cls.theme_style = "Dark"

        self.manager_screens.current = 'home screen'
        return self.manager_screens
    

    def on_keyboard_down(self, window, keyboard, keycode, text, modifiers) -> None:
        print( "KEY PRESSED:", keyboard, keycode, text, modifiers)
            

Samus().run()
