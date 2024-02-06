from kivy.properties import ObjectProperty
from kivymd.theming import ThemableBehavior
from gestures4kivy import CommonGestures
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp

from Utility.observer import Observer


# Swipe effect  
class SwipeScreen( MDScreen, CommonGestures ):
    def cgb_horizontal_page(self, touch, rigth ):
        MDApp.get_running_app().swipe_screen( touch, rigth )


# Screen manager 
class BaseScreenView( ThemableBehavior, MDScreen, Observer ):
    manager_screens = ObjectProperty()
    controller = ObjectProperty()
    model = ObjectProperty()
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()
        self.model.add_observer(self)