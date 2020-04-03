#!/usr/bin/env python

from Paquete import Paquete
#from abc import ABCMeta, abstractmethod

class Aereo(Paquete):
	'''Abstracion de la clase Paquete Aereo'''

	cantidad_total_aereos = 0
	TRASLADO = "Aereo"

	def __init__(self, precio, senha, **kwargs):
		super().__init__(**kwargs)
		self.precio = precio
		self.saldo = precio
		self.senha = senha
		#incrementamos la cantidad de instancias
		Aereo.cantidad_total_aereos += 1

	def get_lugares_disponibles(self):
		return -1

	def get_cantidad_de_usuarios_total(self):
		return -1
	#agregar def get cantidad maxima de pasajero (return -1)
