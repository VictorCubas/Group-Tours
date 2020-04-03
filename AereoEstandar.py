#!/usr/bin/env python

from Aereo import Aereo

class AereoEstandar(Aereo):
	'''Clase que representa un paquete cuyo traslado es
		via aereo y que esta predefinido por la agencia'''

	cantidad_total_aereo_estandar = 0
	TIPO = 'Estandar'

	#def __init__(self, precio, senha, fecha_de_viaje, **kwargs):
	def __init__(self, precio, senha, **kwargs):
		super().__init__(precio, senha, **kwargs)
		#self.precio = precio
		#self.saldo = precio
		#self.senha = senha
		#self.fecha_de_viaje = fecha_de_viaje

		#Incrementamos la cantidad de instancias
		AereoEstandar.cantidad_total_aereo_estandar += 1

	def accion(self):
		pass
