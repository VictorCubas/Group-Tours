#!/usr/bin/env python

from abc import ABCMeta, abstractmethod
from Factura import Factura

class Empresa(metaclass=ABCMeta):
	'''Abstraccion que representa a una empresa'''

	def __init__(self, ruc, nombre, direccion):
		self.__ruc = ruc
		self.__nombre = nombre
		self.__direccion = direccion
		self.paquetes = []
		self.usuarios = []
		self.empleados = []
		self.contactos = []

	#def vender(self, usuario, empleado, paquete):
		

	#def vender(self, empleado, paquete)
	#	empleado.liquidar(paquete)

	#def vender(self, paquete):
	#	paquete.liquidar()

	def vender(self, factura, cantidad_cuotas):
		factura.liquidar(cantidad_cuotas)

	def senhar(self, factura):
		factura.senhar()

	def agregar_paquete(self, paquete):
		self.paquetes.append(paquete)

	def agregar_usuario(self, usuario):
		self.usuarios.append(usuario)

	def agregar_empleado(self, empleado):
		self.empleados.append(empleado)

	def agregar_contacto(self, contacto):
		self.contactos.append(contacto)

	def obtener_paquetes(self):
		return self.paquetes

	def obtener_usuarios(self):
		return self.usuarios

	def obtener_empleados(self):
		return self.empleados

	def obtener_contactos(self):
		return self.contactos

	def set_ruc(self, ruc):
		self.__ruc = ruc

	def get_ruc(self):
		return self.__ruc

	def set_nombre(self, nombre):
		self.__nombre = nombre

	def get_nombre(self):
		return self.__nombre

	def set_direccion(self, direccion):
		self.__direccion = direccion

	def get_direccion(self):
		return self.__direccion

	@abstractmethod
	def accion(self):
		pass
