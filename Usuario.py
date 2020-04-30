#!/usr/bin/env python

from Persona import Persona
from Nacionalidad import Nacionalidad

class Usuario():
	'''Abstraccion de la clase Usuario'''
	cantidad_total_usuarios = 0

	def __init__(self, nombre, apellido, cedula, fecha_nacimiento, edad, nacionalidad):
		self.persona = Persona(nombre, apellido, cedula, fecha_nacimiento, edad, Nacionalidad(nacionalidad))
		self.senha = 0 #VER
		self.saldo = 0 #VER
		self.total_pagado = 0
		self.paquetes = []
		self.facturas = []
		self.observacion = None
		#Incrementamos la cantidad de instancias
		Usuario.cantidad_total_usuarios += 1

	def get_nombre(self):
		return self.persona.get_nombre()

	def get_apellido(self):
		return self.persona.get_apellido()

	def get_cedula(self):
		return self.persona.get_ci()

	def agregar_paquete(self, paquete):
		self.paquetes.append(paquete)

	def agregar_contacto(self, contacto ):
		self.persona.agregar_contacto( contacto )

	def set_telefono_primario(self, telefono):
		self.persona.set_telefono_primario(telefono)

	def set_telefono_secundario(self, telefono):
		self.persona.set_telefono_secundario(telefono)

	def set_correo(self, correo):
		self.persona.set_correo(correo)

	def get_telefono_primario(self):
		return self.persona.get_telefono_primario()

	def get_telefono_secundario(self):
		return self.persona.get_telefono_secundario()

	def get_correo(self):
		return self.persona.get_correo()

	def agregar_factura(self, factura):
		self.facturas.append(factura)

	def get_facturas(self):
		return self.facturas

	def calificar_usuario(self, observacion):
		self.observacion = observacion

	def eliminar_contacto(self, posicion_contacto ):
		self.persona.eliminar_contacto( posicion_contacto )

	def get_contactos(self):
		return self.persona.get_contactos()

	def get_paquetes(self):
		return self.paquetes

	def senhar(self, paquete):
		paquete.senhar()

	def liquidar(self, paquete, monto, cantidad_cuotas):
		paquete.liquidar(monto, cantidad_cuotas)

	def __str__(self):
		return self.persona.__str__()

	@staticmethod
	def get_total_usuarios():
		return Usuario.cantidad_total_usuarios
