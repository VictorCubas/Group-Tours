#!/usr/bin/env python

from Empleado import Empleado

class EmpleadoInterno(Empleado):
	'''
	Clase que representa al empleado que se encuentra dentro de la empresa
	y que es asalariado
	'''
	cantidad_total_empleados_internos = 0

	def __init__(self, nombre, apellido, cedula, fecha_nacimiento, edad, nacionalidad, sueldo_base):
		super().__init__(nombre, apellido, cedula, fecha_nacimiento, edad, nacionalidad)
		self.__sueldo_base = sueldo_base
		#Incrementamos la cantidad de instancias
		EmpleadoInterno.cantidad_total_empleados_internos += 1

	def calcular_sueldo(self):
		self.sueldo = self.__sueldo_base

	@staticmethod
	def get_total_empleados_internos():
		return EmpleadoInterno.cantidad_total_empleados_internos

