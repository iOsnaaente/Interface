# The screens dictionary contains the objects of the models and controllers
# of the screens of the application.


from Model.login_screen import LoginScreenModel
from Controller.login_screen import LoginScreenController
from Model.home_screen import HomeScreenModel
from Controller.home_screen import HomeScreenController
from Model.config_screen import ConfigScreenModel
from Controller.config_screen import ConfigScreenController

screens = {
    "login screen": {
        "model": LoginScreenModel,
        "controller": LoginScreenController,
    },

    "home screen": {
        "model": HomeScreenModel,
        "controller": HomeScreenController,
    },

    "config screen": {
        "model": ConfigScreenModel,
        "controller": ConfigScreenController,
    },
}