#!/usr/bin/env python

#import datetime
#import time

class PreVenta:
	'''Abstraccion de la clase Pre Venta'''
	
	def __init__(self, precio, senha, monto_cuota, cantidad_cuotas, fecha_inicio, fecha_fin):
		self.fecha_inicio = fecha_inicio
		self.fecha_fin = fecha_fin
		self.precio = precio
		self.senha = senha
		self.monto_cuota = monto_cuota
		self.cantidad_cuotas = cantidad_cuotas
		self.cantidad_cuotas_actual = 0
		self.paquetes = []

	#def liquidar(self):
	#	self.cantidad_cuotas_actual += cantidad_cuotas
		
	def calcular_monto(self, cantidad_cuotas):
		return self.monto_cuota * cantidad_cuotas

	def set_cantidad_cuotas_actual(self, cantidad_cuotas):
		self.cantidad_cuotas_actual += cantidad_cuotas

	def agregar_paquete(self, paquete):
		self.paquetes = paquete

	#def set_cantidad_cuota_actual(self, cantidad_cuotas_a_pagar):
	#	self.cantidad_cuota_actual += cantidad_cuotas_a_pagar

	def get_cantidad_cuotas(self):
		return self.cantidad_cuotas

	def set_cantidad_cuotas(self, cantidad_cuotas):
		self.cantidad_cuotas = cantidad_cuotas

	def get_cantidad_cuota_actual(self):
		return self.cantidad_cuotas_actual

	def get_fecha_inicio(self):
		return self.fecha_inicio

	def get_fecha_fin(self):
		return self.fecha_fin

	def get_senha(self):
		return self.senha

	def get_precio(self):
		return self.precio

	def set_senha(self, sehna):
		self.sehna = sehna

	def set_precio(self, precio):
		self.precio = precio

	def get_monto_cuota(self):
		return self.monto_cuota

	def esta_vigente(self, fecha_actual):
		'''Metodo que calcula si sigue vigente la pre-venta'''
		return self.fecha_fin <= fecha_actual


#preventa = PreVenta("2019-03-12", datetime.date(2019,6,13), 200, 23, 3, 34)
#print( preventa.esta_vigente( datetime.date.today()) )
