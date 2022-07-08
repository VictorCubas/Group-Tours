#!/usr/bin/env python

import abc
import datetime

from abc import ABCMeta, abstractmethod

class Paquete(metaclass=ABCMeta):
	'''Abstraccion de la clase Factura'''

	cantidad_total_paquetes = 0

	def __init__(self, nombre_paquete):
		self.nombre_paquete = nombre_paquete #*******
		self.incluye_descripcion = None
		self.fecha_de_viaje = None	#*******
		self.precio = 0
		self.senha = 0
		self.saldo = 0 #VER
		self.total = 0 #VER
		self.usuarios = []
		self.facturas = []
		self.pre_venta = None
		self.esta_vigente = None
		self.codigo = None
		self.cantidad_pagos_actual = 0
		self.cantidad_de_usuarios_total = 0
		self.cantidad_de_usuarios_actual = 0
		self.imagen = None
		#Incrementamos la cantidad de instancias
		Paquete.cantidad_total_paquetes += 1

	def agregar_usuario(self, usuario):
		self.cantidad_de_usuarios_actual += 1
		self.usuarios.append(usuario)

	def get_usuarios(self):
		return self.usuarios
		
	def get_imagen(self):
		return self.imagen

	def agregar_facturas(self, factura):
		self.facturas.append(factura)

	def get_facturas(self):
		return self.facturas

	def senhar(self):
		senha_aux = self.senha

		if self.si_pre_venta():
			senha_aux = self.pre_venta.get_senha()

		self.saldo -= senha_aux
		self.total += senha_aux
		self.cantidad_pagos_actual += 1

	#def senhar(self):
	#	'''Metodo'''
	#	if si_pre_venta():
	#		self.pre_venta.senhar()
	#	else:
	#		self.saldo = self.senha
	#		self.total += self.senha


	#def liquidar(self, monto):
	#	monto_aux = self.monto
	#
	#	if si_pre_venta():
	#		#self.pre_venta.liquidar(cantidad_cuotas)
	#		monto_aux = self.pre_venta.get_monto_cuota()
	#		self.pre_venta.
	#
	#	self.saldo -= monto_aux

	def liquidar(self, monto, cantidad_cuotas):
		'''Metodo que realiza el pago (liquidacion) correspondiente a un paquete'''
		'''FALTA AGREGAR EXCEPCION A LA CANTIDAD DE CUOTAS'''

		monto_aux = monto

		if self.si_pre_venta():
			monto_aux = self.pre_venta.calcular_monto(cantidad_cuotas)
			self.pre_venta.set_cantidad_cuotas_actual(cantidad_cuotas)
		else:
			self.cantidad_pagos_actual += 1

		self.saldo -= monto_aux
		self.total += monto_aux

	def get_cantidad_pagos_actual(self):
		if self.si_pre_venta():
			return pre_venta.get_cantidad_cuota_actual()

		return self.cantidad_pagos_actual

	def agregar_pre_venta(self, pre_venta):
		self.pre_venta = pre_venta

	def get_pre_venta(self):
		return self.pre_venta

	def set_codigo(self, codigo):
		self.codigo = codigo

	def get_codigo(self):
		return self.codigo

	def set_esta_vigente(self, esta_vigente):
		self.esta_vigente = esta_vigente

	def get_esta_vigente(self):
		return self.esta_vigente

	def get_nombre(self):
		return self.nombre_paquete

	def si_pre_venta(self):
		return not(self.pre_venta == None)
		
	def set_imagen(self, imagen):
		self.imagen = imagen

	def set_precio(self, precio):
		self.precio = precio

	def get_precio(self):
		return self.precio

	def set_precio_pre_venta(self, precio_pre_venta):
		if self.si_pre_venta():
			self.pre_venta.set_precio(precio_pre_venta)

		return None

	def get_precio_pre_venta(self):
		if self.si_pre_venta():
			return self.pre_venta.get_precio()

		return None

	def set_saldo(self, saldo):
		self.saldo = saldo

	def get_saldo(self):
		return self.saldo

	def set_senha_pre_venta(self, senha_pre_venta):
		if self.si_pre_venta():
			self.pre_venta.set_senha(senha_pre_venta)

		return None

	def get_senha_pre_venta(self):
		if self.si_pre_venta():
			return self.pre_venta.get_senha()

		return None

	def set_senha(self, senha):
		self.senha = senha

	def get_senha(self):
		return self.senha

	def set_senha_pre_venta(self, senha_pre_venta):
		if self.si_pre_venta():
			self.pre_venta.set_senha(precio_pre_venta)

		return None

	def get_precio_pre_venta(self):
		if self.si_pre_venta():
			return self.pre_venta.get_precio()

		return None

	def set_fecha_de_viaje(self, fecha_de_viaje):
		self.fecha_de_viaje = fecha_de_viaje

	def get_fecha_de_viaje(self):
		return self.fecha_de_viaje

	def get_anho_de_viaje(self):
		return self.fecha_de_viaje.year

	def get_cantidad_pagos_actual(self):
		if self.si_pre_venta():
			return self.pre_venta.get_cantidad_cuotas_actual()
		else:
			return self.cantidad_pagos_actual

	def set_cantidad_de_usuarios_total(self, cantidad_de_usuarios_total):
		self.cantidad_de_usuarios_total = cantidad_de_usuarios_total

	@abstractmethod
	def get_cantidad_de_usuarios_total(self):
		pass

	def get_cantidad_de_usuarios_actual(self):
		return self.cantidad_de_usuarios_actual

	def get_incluye_descripcion(self):
		return self.incluye_descripcion

	def set_incluye_descripcion(self, incluye_descripcion):
		self.incluye_descripcion = incluye_descripcion

	@abstractmethod
	def get_lugares_disponibles(self):
		pass

	@abstractmethod
	def accion(self):
		pass

	@staticmethod
	def get_total_paquetes():
		return Paquete.cantidad_total_paquetes
