#!/usr/bin/env python

from Terrestre import Terrestre
from Usuario import Usuario

class TerrestreEstandar(Terrestre):
	'''Clase que representa a un paquete cuyo traslado es via terrestre
	que la agencia tiene disponible al publico'''

	cantidad_total_terrestre_estandar = 0
	TIPO = 'Estandar'

	def __init__(self, precio, senha, fecha_de_viaje, **kwargs):
		super().__init__(**kwargs)
		self.precio = precio
		self.saldo = precio
		self.senha = senha
		self.fecha_de_viaje = fecha_de_viaje
		#Incrementamos la cantidad de instancias
		TerrestreEstandar.cantidad_total_terrestre_estandar += 1

	def accion(self):
		pass

'''
nombre = 'cambo'
terrestre = TerrestreEstandar( 123, 22, "2019-06-12", nombre_paquete=nombre, incluye_descripcion='Inclueye desayuno')
usuario = Usuario( "Andrea", "Escurra", "4028760", "18/11/1991", 20, "Paraguay" )
terrestre.agregar_usuario(usuario)
usuarios = terrestre.get_usuarios()

for u in usuarios:
	print(u.__str__())

print(terrestre.precio)
print(terrestre.nombre_paquete)
print(terrestre.fecha_de_viaje)
terrestre.set_precio(20000)
print("precio: " + str(terrestre.precio))
print('pasajeros: ' + str(terrestre.get_cantidad_de_usuarios_actual()))

nombre = 'cambo'
terrestre = TerrestreEstandar( 456, 12, "2019-06-12" , nombre_paquete=nombre, incluye_descripcion='Inclueye desayuno')

print("\n")
print(terrestre.precio)
print(terrestre.nombre_paquete)
print(terrestre.fecha_de_viaje)'''
