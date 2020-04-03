#!/usr/bin/env python

import abc
import datetime

from abc import ABCMeta, abstractmethod
from Documento import Documento

class Factura(Documento):
	'''Abstraccion de la clase Factura'''

	#RUC = 
	'''
	ANHADIR LOS DATOS DE LA BOLETA
	'''

	def __init__(self, nombre_razon_social, numero_factura, fecha_de_pago, hora_de_pago):
		super().__init__()
		self.numero_factura = numero_factura
		self.fecha_de_pago = fecha_de_pago
		self.hora_de_pago = hora_de_pago
		self.nombre_razon_social = nombre_razon_social
		self.usuarios = []
		self.paquetes = []
		self.montos = []
		self.cuotas = []
		self.empleado = None
		self.total = 0
		self.cantidad_paquetes = 0
		self.cantidad_usuarios = 0
		#self.saldo = 0

	def agregar_usuario(self, usuario):
		self.usuarios.append(usuario)
		self.cantidad_usuarios += 1

	def agregar_paquete(self, paquete):
		self.paquetes.append(paquete)
		self.cantidad_paquetes += 1

	def agregar_monto(self, monto):
		self.montos.append(monto)

	def agregar_empleado(self, empleado):
		self.empleado = empleado

	def agregar_cuota(self, cuota):
		self.cuotas.append(cuota)

	def get_empleado(self):
		return self.empleado

	@abstractmethod
	def liquidar(self):
		pass

	def senhar(self):
		i = 0

		for usuario in self.usuarios:
			usuario.senhar(self.paquetes[i])
			self.total += self.paquetes[i].get_senha()
			i += 1
