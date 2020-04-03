#!/usr/bin/env python

from Contacto import Contacto

class Telefono( Contacto ):
    '''Clase telefono que hereda de Contacto'''

    def __init__( self, numero, descripcion ):
        super().__init__( descripcion )
        self.numero = numero

    def accion(self):
        '''sobre-escribimos el metodos abstracto'''
        pass

    def set_numero(self, numero):
        self.numero = numero

    def get_numero(self):
        return self.numero
     
    def __str__( self ):
        return super( ).__str__( ) + "{}".format( self.numero )
