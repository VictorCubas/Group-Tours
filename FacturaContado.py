#!/usr/bin/env python

from Factura import Factura

class FacturaContado(Factura):
	'''Representacion de la case factura contado'''

	TIPO = "Contado"
	CANTIDAD_CUOTA = 1

	def __init__(self, nombre_razon_social, numero_factura, fecha_de_pago, hora_de_pago):
		super().__init__(nombre_razon_social, numero_factura, fecha_de_pago, hora_de_pago)

	def liquidar(self):
		i = 0

		for usuario in self.usuarios:
			usuario.liquidar(self.paquetes[i], self.montos[i], FacturaContado.CANTIDAD_CUOTA)
			self.total += self.montos[i]
			i += 1

	def accion(self):
		pass

'''
factura_contado = FacturaContado(2, 123, "20-06-2019", '18:06')
print(factura_contado.cantidad_paquetes)
print(factura_contado.numero_factura)
print(factura_contado.fecha_de_pago)
print(factura_contado.hora_de_pago)'''
