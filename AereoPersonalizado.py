#!/usr/bin/env python

from Aereo import Aereo

class AereoPersonalizado(Aereo):
	'''Clase que representa un paquete cuyo traslado es
		via aereo y que esta edefinido por el usuario'''

	cantidad_total_aereo_personalizado = 0
	TIPO = 'Personalizado'

	def __init__(self, precio, senha, **kwargs):
		super().__init__(precio, senha, **kwargs)
		#Incrementamos la cantidad de instancias
		AereoPersonalizado.cantidad_total_aereo_personalizado += 1

	def AereoPersonalizado(self):
		return AereoPersonalizado.TIPO

	def accion(self):
		pass
