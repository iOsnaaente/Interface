from Model.base_model import BaseScreenModel

import os 

PATH = os.path.dirname( __file__ ).removesuffix( '\\Model' )

class HomeModel(BaseScreenModel):
    
    photo_image = PATH + '/assets/images/bruno-sampaio.jpg'
    name =  'Bruno'
    nickname = 'Sampaio'
    username = name + ' ' + nickname 
    renda_total = 'R$ ' + str(11900)

    """
    Implements the logic of the
    :class:`~View.home_screen.HomeScreen.HomeScreenView` class.
    """