from kivy.animation import Animation 

import View.HomeScreen.home_screen

from kivy.clock import Clock 
import importlib

# We have to manually reload the view module in order to apply the
# changes made to the code on a subsequent hot reload.
# If you no longer need a hot reload, you can delete this instruction.
importlib.reload(View.HomeScreen.home_screen)


class HomeScreenController:
    """
    The `HomeScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model):
        self.model = model  # Model.home_screen.HomeScreenModel
        self.view = View.HomeScreen.home_screen.HomeScreenView(controller=self, model=self.model)

    def get_view(self) -> View.HomeScreen.home_screen:
        return self.view
        
    def hover_sign( self, obj, status, *args ):
        if status == 'IN':
            anim = Animation( 
                size = [ obj.size[0]*1.1, obj.size[1]*1.1 ],
                md_bg_color = obj.color_active, 
                duration = 0.15 
            )
            anim.start( obj )
        elif status == 'OUT':
            anim = Animation( 
                size = obj.origin_size, 
                md_bg_color = obj.color_active if obj.activated else obj.color_deactive,  
                duration = 0.15 
            )
            anim.start( obj )

    def set_focus_widget( self, dt = None ): 
        self.view.ids.text_field_input.text = ''
        self.get_view().ids.text_field_input.focus = True

    def validate_input( self ):
        if len(self.get_view().ids.text_field_input.text) == self.model.MAX_LEN_INPUT:
            print( 'INPUT VALIDATED' ) 
            self.view.ids.text_field_input.focus = True 
        else: 
            print( 'INVALID INPUT' )

        Clock.schedule_once(self.set_focus_widget, 1 )