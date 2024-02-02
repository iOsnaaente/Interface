from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.screenmanager import WipeTransition
from kivymd.tools.hotreload.app import MDApp
from kivy.utils import rgba, QueryDict 

from screeninfo import get_monitors
try: 
    monitor = get_monitors()[1]
except:
    monitor = get_monitors()[0]

from kivy.core.window import Window
Window.size = ( monitor.width, monitor.height )
Window.left = monitor.x
Window.top = monitor.y + 25

# Inicia em modo Tela Cheia 
Window.fullscreen = 'auto'


# Debug 
LOAD_SCREEN = 'login screen'
#


class Gigadetestes( MDApp ):
    from resources.access_manager import Database
    db = Database( True )
    
    import os
    KV_DIRS = [os.path.join(os.getcwd(), "View")]

    # Cores 
    colors = QueryDict() 
    colors.background    = rgba( "#E8F8E8F0" )
    colors.primary       = rgba( "#4AD66DF0" )
    colors.primary_HUE   = rgba( "#4AD66D50" )
    colors.accent        = rgba( "#10451DFF" )
    colors.hint          = rgba( "#888888FF" )
    colors.error         = rgba( "#FF5449FF" )
    colors.warning       = rgba( "#F87F29FF" )
    colors.success       = rgba( "#4AD66DFF" )
    colors.inactive      = rgba( "#535353FF" )
    
    def build_app(self) -> MDScreenManager:
        """
        In this method, you don't need to change anything other than the
        application theme.
        """
        import importlib 
        import View.screens

        self.manager_screens = MDScreenManager( transition = WipeTransition() )
        Window.bind(on_key_down=self.on_keyboard_down)
        importlib.reload(View.screens)
        screens = View.screens.screens

        for _, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]( database = self.db )
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "500"
        self.manager_screens.current = LOAD_SCREEN

        return self.manager_screens

    def on_keyboard_down(self, window, keyboard, keycode, text, modifiers) -> None:
        if "meta" in modifiers or "ctrl" in modifiers and text == "r":
            self.rebuild()


Gigadetestes().run()



# """
# The entry point to the application.

# The application uses the MVC template. Adhering to the principles of clean
# architecture means ensuring that your application is easy to test, maintain,
# and modernize.

# You can read more about this template at the links below:

# https://github.com/HeaTTheatR/LoginAppMVC
# https://en.wikipedia.org/wiki/Model–view–controller
# """

# from kivymd.app import MDApp
# from kivymd.uix.screenmanager import MDScreenManager

# from View.screens import screens


# class Gigadetestes(MDApp):
#     from resources.database.access_manager import Database
#     db = Database()
#
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.load_all_kv_files(self.directory)
#         # This is the screen manager that will contain all the screens of your
#         # application.
#         self.manager_screens = MDScreenManager()
        
#     def build(self) -> MDScreenManager:
#         self.generate_application_screens()
#         return self.manager_screens

#     def generate_application_screens(self) -> None:
#         """
#         Creating and adding screens to the screen manager.
#         You should not change this cycle unnecessarily. He is self-sufficient.

#         If you need to add any screen, open the `View.screens.py` module and
#         see how new screens are added according to the given application
#         architecture.
#         """

#         for i, name_screen in enumerate(screens.keys()):
#             model = screens[name_screen]["model"]()
#             controller = screens[name_screen]["controller"](model)
#             view = controller.get_view()
#             view.manager_screens = self.manager_screens
#             view.name = name_screen
#             self.manager_screens.add_widget(view)


# Gigadetestes().run()
