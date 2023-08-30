from resources.access_manager import Database
from Model.base_model import BaseScreenModel

class ConfigScreenModel(BaseScreenModel):
    """
    Implements the logic of the
    :class:`~View.config_screen.ConfigScreen.ConfigScreenView` class.
    """

    def __init__( self, database : Database ) -> None:
        super().__init__()
        self.db = database