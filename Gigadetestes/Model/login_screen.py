from Model.base_model import BaseScreenModel
from resources.access_manager import Database
import re 

class LoginScreenModel( BaseScreenModel ):
    """
    Implements the logic of the
    :class:`~View.login_screen.LoginScreen.LoginScreenView` class.
    """

    MAX_LEN_INPUT = 10

    # ESSE É PADRAO DE INPUT DO TEXTO 
    # Exemplo:
    #   A12345678B
    # 1 Letra + 8 Numeros + 1 Letra 
    PATTERN = r'^[a-zA-Z]{1}\d{8}[a-zA-Z]{1}'

    def __init__( self, database : Database ) -> None:
        super().__init__()
        self.db = database

    def validate_input( self, input_text : str ) -> bool:
        if re.match( self.PATTERN, input_text ) is not None:
            # Salva o acesso no banco de dados
            return self.db.new_access( input_text, self.db.ACCESS_IN )
        else: 
            # Fora de padrão, invalida instantaneamente 
            return None 