import View.LoginScreen.login_screen
import importlib

from kivy.animation import Animation
from kivy.clock import Clock

# We have to manually reload the view module in order to apply the
# changes made to the code on a subsequent hot reload.
# If you no longer need a hot reload, you can delete this instruction.
importlib.reload(View.LoginScreen.login_screen)

class LoginScreenController:
    """
    The `LoginScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """


    def __init__(self, model):
        self.model = model  # Model.login_screen.LoginScreenModel
        self.view = View.LoginScreen.login_screen.LoginScreenView( controller = self, model = self.model)
        self.app = self.view.app


    def get_view(self) -> View.LoginScreen.login_screen:
        return self.view
    

    def validate_input( self, dt = None ):
        textInput = self.get_view().ids.TextFieldInput
        if self.model.validate_input( textInput.text ):
            print( f'INPUT VÁLIDO: {textInput.text}' )
            self.go_to_home()
        else:
            print( f'INPUT INVÁLIDO: {textInput.text}' )
            # Clock.schedule_once( self.set_text_field_focus, 0.1 )


    # Setar o foco do Text Field 
    def set_text_field_focus( self, event = None ):
        textInput = self.get_view().ids.TextFieldInput
        textInput.focus = True
        textInput.text = ''

    # Cria um efeito de hover mudando o frostItem noise 
    def hover_info( self, state : str ):
        frostItem = self.get_view().ids.FrostedInfoCard
        if state == 'IN':
            anm = Animation( noise_opacity = 0.15, duration = 0.1 )
            anm.start( widget = frostItem  )
        elif state == 'OUT':
            anm = Animation( noise_opacity = 0.075, duration = 0.1 )
            anm.start( widget = frostItem  )
    

    # Mudar de página 
    def go_to_home( self ):
        self.app.manager_screens.current = 'home screen'