#!/usr/bin/env python

import abc

from Contacto import Contacto

class Persona:
	'''Abstracion de una Persona'''
	
	def __init__( self, nombre, apellido, ci, fecha_nacimiento, edad, nacionalidad ):
		self.nombre = nombre
		self.apellido = apellido
		self.ci = ci
		self.fecha_nacimiento = fecha_nacimiento
		self.edad = edad
		self.contactos = []
		self.nacionalidad = nacionalidad

	def agregar_contacto(self, contacto ):
		self.contactos.append( contacto )

	def eliminar_contacto(self, posicion_contacto ):
		self.contactos.pop( posicion_contacto )

	def set_nacionalidad(self):
		self.nacionalidad = nacionalidad

	def get_nacionalidad(self):
		return self.nacionalidad

	def set_nombre( self, nombre ):
		self.nombre = nombre
		
	def get_nombre( self ):
		return self.nombre

	def set_apellido( self, apellido ):
		self.apellido = apellido

	def get_apellido( self ):
		return self.apellido
		
	def set_ci( self, ci ):
		self.ci = ci

	def get_ci( self ):
		return self.ci

	def set_fecha_nacimiento( self, fecha_nacimiento ):
		self.fecha_nacimiento = fecha_nacimiento

	def get_fecha_nacimiento( self ):
		return self.fecha_nacimiento

	def set_edad( self, edad ):
		self.edad = edad

	def get_edad( self ):
		return self.edad

	def __str__(self):
		return "Nombre: {} Apellido: {} Nacionalidad: {}".format(self.nombre, self.apellido, self.nacionalidad.get_nombre_pais())

	def get_contactos(self):
		return self.contactos
