#!/usr/bin/env python

from Terrestre import Terrestre

class TerrestrePersonalizado(Terrestre):
	'''Clase que representa a un paquete cuyo traslado es via terrestre
	que la agencia tiene disponible al publico'''

	cantidad_total_terrestre_personalizado = 0
	TIPO = 'Personalizado'

	def __init__(self, precio, senha, **kwargs):
		super().__init__(**kwargs)
		self.precio = precio
		self.senha = senha
		#Incrementamos la cantidad de instancias
		TerrestrePersonalizado.cantidad_total_terrestre_personalizado += 1

	def accion(self):
		pass
