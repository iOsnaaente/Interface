import sqlite3 

import re 
PATTERN = r'^[a-zA-Z]{1}\d{8}[a-zA-Z]{1}'

inputs = 'A12345678A'
# print( re.match( PATTERN, inputs ) is not None )


class StateMachine: 
    ''' Definição das máquinas de estado com o Rasp
    '''

    def __init__( self, db_path : str, debug : bool = False ) -> None: 
        self.db_path = db_path 
        return 1 

    def next( self ): 
        pass 

    def back( self ): 
        pass 

    def get_state_info( self ): 
        pass 

    def reset( self ):
        pass 

    def save_state( self ): 
        pass 

    def get_last_state( self ):
        pass 