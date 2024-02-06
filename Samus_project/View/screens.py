# The screen's dictionary contains the objects of the models and controllers
# of the screens of the application.

from Model.home import HomeModel
from Controller.home_screen import HomeController

screens = {
    'home screen': {
        'model': HomeModel,
        'controller': HomeController,
    }
}