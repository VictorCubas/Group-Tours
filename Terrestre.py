#!/usr/bin/env python

from Paquete import Paquete
#from abc import ABCMeta, abstractmethod

class Terrestre(Paquete):
	'''Clase que representa a un paquete cuyo traslado es via terrestre'''

	cantidad_total_terrestres = 0
	TRASLADO = "Terrestre"

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# Incrementamos la cantidad de instancias
		Terrestre.cantidad_total_terrestres += 1

	def get_lugares_disponibles(self):
		return self.cantidad_de_usuarios_total - self.cantidad_de_usuarios_actual

	def set_cantidad_de_usuarios_total(self, cantidad_de_usuarios_total):
		self.cantidad_de_usuarios_total = cantidad_de_usuarios_total

	def get_cantidad_de_usuarios_total(self):
		return self.cantidad_de_usuarios_total

#terrestre = Terrestre(nombre_paquete='Cambo',incluye_descripcion='Incluye desayuno')

