#!/usr/bin/env python

from Persona import Persona
from abc import ABCMeta, abstractmethod

class Empleado(metaclass=ABCMeta):
	'''
	Abstraccion de la clase empleado
	'''

	cantidad_total_empleados = 0

	def __init__(self, nombre, apellido, cedula, fecha_nacimiento, edad, nacionalidad):
		self.persona = Persona(nombre, apellido, cedula, fecha_nacimiento, edad, nacionalidad)
		self.paquetes = []
		self.facturas = []
		#Incrementamos la cantidad de instancias
		Empleado.cantidad_total_empleados += 1

	def liquidar(self, factura, cantidad_cuotas):
		factura.liquidar(cantidad_cuotas)

	def senhar(self, factura):
		factura.senhar()

	def agregar_factura(self, factura):
		self.facturas.append(factura)

	def agregar_paquete(self, paquete):
		self.paquetes.append(paquete)

	def get_paquetes(self):
		return self.paquetes

	@abstractmethod
	def calcular_sueldo(self):
		pass

	@staticmethod
	def get_total_empleados():
		return Empleado.cantidad_total_empleados
