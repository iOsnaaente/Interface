from View.base_screen import BaseScreenView
from kivymd.app import MDApp 
from kivy.clock import Clock 

from akivymd.uix.progresswidget import AKCircularProgress 



class HomeScreenView(BaseScreenView):

    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
    
    def on_enter( self, *args ):
        Clock.schedule_once(self.controller.set_focus_widget, 0.1 )
        return super().on_enter( *args )
    
    def on_kv_post(self, base_widget):
        BaseScreenView.on_kv_post(self, base_widget)
    
    