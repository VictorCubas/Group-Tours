#!/usr/bin/env python

from Factura import Factura

class FacturaCredito(Factura):
	'''Representacion de la case factura contado'''

	TIPO = "Credito"

	def __init__(self, nombre_razon_social, numero_factura, fecha_de_pago, hora_de_pago, fecha_vencimiento):
		super().__init__(nombre_razon_social, numero_factura, fecha_de_pago, hora_de_pago)
		self.fecha_vencimiento = fecha_vencimiento

	def liquidar(self):
		i = 0

		for usuario in self.usuarios:
			usuario.liquidar(self.paquetes[i], self.montos[i], self.cuotas[i])
			self.total += self.montos[i]
			i += 1

	def accion(self):
		pass

'''
factura = FacturaCredito(2, 123, "20-06-2019", '18:06', "20-06-2019")
print(factura.cantidad_paquetes)
print(factura.numero_factura)
print(factura.fecha_de_pago)
print(factura.hora_de_pago)
print(factura.fecha_vencimiento)'''
