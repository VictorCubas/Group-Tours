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
		self.pre_ventas = []
		self.imagenes = []
		self.esta_vigente = None
		self.codigo = None
		self.cantidad_pagos_actual = 0
		self.cantidad_de_usuarios_total = 0
		self.cantidad_de_usuarios_actual = 0
		self.cantidad_de_pre_ventas = 0
		self.cantidad_de_imagenes = 0
		#Incrementamos la cantidad de instancias
		Paquete.cantidad_total_paquetes += 1

	def agregar_imagen(self, imagen):
		self.imagenes.append(imagen)

	def set_imagenes(self, imagenes):
		self.imagenes = imagenes
		self.cantidad_de_imagenes = len(imagenes)

	def get_cantidad_de_imagenes(self):
		return self.cantidad_de_imagenes

	def get_imagenes(self):
		return self.imagenes

	def agregar_usuario(self, usuario):
		self.cantidad_de_usuarios_actual += 1
		self.usuarios.append(usuario)

	def get_usuarios(self):
		return self.usuarios

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
		self.pre_ventas.append(pre_venta)

	def set_pre_ventas(self, pre_ventas):
		self.pre_ventas = pre_ventas
		self.cantidad_de_pre_ventas = len(pre_ventas)

	def get_pre_ventas(self):
		return self.pre_ventas

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
		return not(self.cantidad_de_pre_ventas == 0)

	def set_precio(self, precio):
		self.precio = precio

	def get_precio(self):
		return self.precio

	def get_precio_pre_venta(self):
		#devolvemos la preventa mas actual que se adecue a la fecha
		pre_venta_actual = None

		if self.si_pre_venta():
			fecha_hoy = datetime.date.today()
			for pre_venta in self.pre_ventas:
				fecha_inicio = pre_venta.get_fecha_inicio()
				fecha_fin = pre_venta.get_fecha_fin()
				if fecha_hoy >= fecha_inicio and fecha_hoy <= fecha_fin:
					return pre_venta.get_precio()

			#significa que tiene pre venta pero no se encuentra en la fecha de pre venta por tanto se retorna el precio de venta
			return self.precio

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
		pre_venta_actual = None
		if self.si_pre_venta():
			fecha_hoy = datetime.date.today()
			for pre_venta in self.pre_ventas:
				fecha_inicio = pre_venta.get_fecha_inicio()
				fecha_fin = pre_venta.get_fecha_fin()
				if fecha_hoy >= fecha_inicio and fecha_hoy <= fecha_fin:
					return pre_venta.get_senha()

			#significa que tiene pre venta pero no se encuentra en la fecha de pre venta por tanto se retorna el senha de venta
			return self.senha

		return None

	def set_senha(self, senha):
		self.senha = senha

	def get_senha(self):
		return self.senha

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
