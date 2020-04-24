#!/usr/bin/env python

from Contacto import Contacto

class Telefono( Contacto ):
    '''Clase telefono que hereda de Contacto'''

    def __init__( self, email, descripcion ):
        super().__init__( descripcion )
        self.email = email

    def accion(self):
        '''sobre-escribimos el metodos abstracto'''
        pass

    def set_email(self, email):
        self.email = email

    def get_email(self):
        return self.email
     
    def __str__( self ):
        return super( ).__str__( ) + "{}".format( self.email )
