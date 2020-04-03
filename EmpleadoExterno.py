#!/usr/bin/env python

from Empleado import Empleado

class EmpleadoExterno(Empleado):
	'''
	Clase que representa al empleado que se encuentra fuera de la empresa
	y que cobra por comision dado un porcentaje de sus ventas
	'''
	
	cantidad_total_empleados_externos = 0

	def __init__(self, nombre, apellido, cedula, fecha_nacimiento, edad, nacionalidad, porcentaje_comision):
		super().__init__(nombre, apellido, cedula, fecha_nacimiento, edad, nacionalidad)
		self.__porcentaje_comision = porcentaje_comision
		self.ventas = 0
		#Incrementamos la cantidad de instancias
		EmpleadoExterno.cantidad_total_empleados_externos += 1

	def calcular_sueldo(self):
		'''Implementacion del metodo abstracto para el
		calculo de sueldo para los empleados externo (por comision).'''
		self.sueldo = self.ventas * (self.__porcentaje / 100)

	@staticmethod
	def get_total_empleados_externos():
		return EmpleadoExternos.cantidad_total_empleados_externos

'''
empleado = EmpleadoExterno("Ariel", "Gaona", 12345, "12-23-23", 25, "Paraguaya", 10)
print(empleado.persona.get_nombre() + " " + empleado.persona.get_fecha_nacimiento())'''
