from resources.access_manager import Database
from Model.base_model import BaseScreenModel
class HomeScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.home_screen.HomeScreen.HomeScreenView` class.
    """
    steps = {
        0 : "Bipar o Serial Number (SN) do dispositivo;",
        1 : "Verificar se o SN esta correto;",
        2 : "Conectar o dispositivo. Com o dispositivo conectado, fechar a tampa;",
        3 : "Aguardar a energização e verificação dos valores medidos;",
        4 : "Validar o estado do teste;",
        5 : "Descarregar o dispositivo e abrir a tampa."
    }
    
    MAX_LEN_INPUT = 12

    def __init__( self, database : Database ) -> None:
        super().__init__()
        self.db = database