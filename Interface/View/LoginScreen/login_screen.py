from kivygo.uix.frostedglass import FrostedGlass
from View.base_screen import BaseScreenView
from kivy.clock import Clock 

class LoginScreenView(BaseScreenView):
    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """

    def __init__(self, **kw):
        super().__init__(**kw)

    # KV Post 
    def on_kv_post( self, *args, **kwargs ):
        Clock.schedule_once( self.controller.set_text_field_focus, 1 )
        return super().on_kv_post( *args, **kwargs )
    


    