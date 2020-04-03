#!/usr/bin/env python

import abc

from abc import ABCMeta, abstractmethod

class Contacto( metaclass=ABCMeta ):
    '''Clase abstracta Contacto'''

    def __init__(self, descripcion):
        self.descripcion = descripcion

    def set_descripcion(self):
        self.descripcion = descripcion
       
    def get_descripcion( self ):
        return self.descripcion

    def __str__( self ):
        return "Contacto: "

    @abstractmethod
    def accion(self):
        pass
