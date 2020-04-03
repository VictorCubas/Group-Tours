#!/usr/bin/env python

import pickle
import datetime
import time
import copy

from Telefono import Telefono
from Contacto import Contacto
from Persona import Persona
from Nacionalidad import Nacionalidad
from Usuario import Usuario
from Paquete import Paquete
from TerrestreEstandar import TerrestreEstandar
from TerrestrePersonalizado import TerrestrePersonalizado
from AereoEstandar import AereoEstandar
from AereoPersonalizado import AereoPersonalizado
from FacturaCredito import FacturaCredito
from FacturaContado import FacturaContado

def main6():
	'''
		PROBANDO SENHAR
	'''

	usuario1 = Usuario( "Victor", "Cubas", "4028760", "18/11/1991", 20, "Paraguay" )
	usuario1.agregar_contacto( Telefono( "0971991960", "personal") )
	usuario1.agregar_contacto( Telefono( "0985871759", "tigo" ) )

	usuario2 = Usuario( "Andrea", "Escurra", "4028760", "18/11/1991", 20, "Paraguay" )

	paquete1 = TerrestreEstandar(3000, 200, "11/30/19", nombre_paquete="Camboriu", incluye_descripcion="holel, desayuno, almuerzo")
	paquete2 = AereoPersonalizado(nombre_paquete="Punta Cana", incluye_descripcion="holel, desayuno, almuerzo")
	paquete2.set_precio(10000)
	paquete2.set_saldo(10000)
	paquete2.set_senha(500)
	paquete2.set_fecha_de_viaje("18/11/2020")

	usuario1.agregar_paquete(paquete1)
	paquete1.agregar_usuario(usuario1)

	usuario2.agregar_paquete(paquete2)
	paquete2.agregar_usuario(usuario2)

	usuarios = []
	usuarios.append(usuario1)
	usuarios.append(usuario2)

	factura = FacturaCredito("Hugo Balbuena", "00021", "2019-06-26", "10:00", "2019-06-27")

	factura.agregar_usuario(usuario1)
	factura.agregar_paquete(paquete1)
	#factura.agregar_monto(2000)

	factura.agregar_usuario(usuario2)
	factura.agregar_paquete(paquete2)
	#factura.agregar_monto(3000)

	factura.senhar()

	print("PAQUETES DESPUES DE SENHAR")

	for usuario in usuarios:
		print("Usuario: " + usuario.__str__())
		paquetes = usuario.get_paquetes()
		for paquete in paquetes:
			print("Paquete: " + paquete.nombre_paquete + " Tipo: " + paquete.TRASLADO)
			print("Cantidad de pagos: {} Saldo: {} Total: {}\n".format(paquete.cantidad_pagos_actual, paquete.saldo, paquete.total))


def main5():
	'''
		PROBANDO LIQUIDAR
	'''
	usuario1 = Usuario( "Victor", "Cubas", "4028760", "18/11/1991", 20, "Paraguay" )
	usuario1.agregar_contacto( Telefono( "0971991960", "personal") )
	usuario1.agregar_contacto( Telefono( "0985871759", "tigo" ) )

	usuario2 = Usuario( "Andrea", "Escurra", "4028760", "18/11/1991", 20, "Paraguay" )

	paquete1 = TerrestreEstandar(2000000, 350000, datetime.date(2019,11,30), nombre_paquete="Camboriu")
	paquete1.set_incluye_descripcion('holel, desayuno, almuerzo')
	paquete1.set_cantidad_de_usuarios_total(0)
	paquete1.set_esta_vigente(True)
	paquete2 = AereoPersonalizado(10000, 500, nombre_paquete="Punta Cana")
	paquete2.set_incluye_descripcion('holel, desayuno, almuerzo')
	paquete2.set_saldo(10000)
	paquete2.set_fecha_de_viaje(datetime.date(2020,11,18))
	paquete2.set_esta_vigente(True)
	paquete3 = TerrestreEstandar(1350000, 350000, datetime.date(2019,8,19), nombre_paquete="Buenos Aires")
	paquete3.set_incluye_descripcion('holel, desayuno, almuerzo')
	paquete3.set_cantidad_de_usuarios_total(10)
	paquete3.set_esta_vigente(True)
	paquete4 = AereoPersonalizado(1087, 100, nombre_paquete="Fortaleza & Jericoacoara")
	paquete4.set_incluye_descripcion('holel, desayuno, almuerzo')
	paquete4.set_saldo(1087)
	paquete4.set_esta_vigente(True)
	#paquete4.set_fecha_de_viaje(datetime.date(2020,11,18))

	paquetes = []
	paquetes_copy = []

	#paquetes.append(paquete1)
	#paquetes.append(paquete2)
	guardar_paquete(paquete1)
	guardar_paquete(paquete2)
	guardar_paquete(paquete3)
	guardar_paquete(paquete4)
	paquetes = listar_paquetes()

	paquetes_copy = copy.deepcopy(paquetes)

	usuario1.agregar_paquete(paquete1)
	paquete1.agregar_usuario(usuario1)

	usuario2.agregar_paquete(paquete2)
	paquete2.agregar_usuario(usuario2)

	usuarios = []
	usuarios.append(usuario1)
	usuarios.append(usuario2)

	factura = FacturaCredito("Hugo Balbuena", "00021", "2019-06-26", "10:00", "2019-10-26")

	factura.agregar_usuario(usuario1)
	factura.agregar_paquete(paquete1)
	factura.agregar_monto(2000)
	factura.agregar_cuota(1)

	factura.agregar_usuario(usuario2)
	factura.agregar_paquete(paquete2)
	factura.agregar_monto(3000)
	factura.agregar_cuota(1)

	print('PAQUETES ANTES DE LIQUIDAR')
	for paquete in paquetes:
		print("Cantidad de pagos: {} Saldo: {} Total: {}\n".format(paquete.cantidad_pagos_actual, paquete.saldo, paquete.total))

	factura.liquidar()


	print("PAQUETES DESPUES DE LIQUIDAR")
	print("Tipo factura: " + factura.TIPO)
	for usuario in usuarios:
		print("Usuario: " + usuario.__str__())
		paquetes = usuario.get_paquetes()
		for paquete in paquetes:
			print("Paquete: " + paquete.nombre_paquete + " Tipo: " + paquete.TRASLADO)
			print("Cantidad de pagos: {} Saldo: {} Total: {}\n".format(paquete.cantidad_pagos_actual, paquete.saldo, paquete.total))

	print("PAQUETES COPIADOS")
	for paquete in paquetes_copy:
		print("Cantidad de pagos: {} Saldo: {} Total: {}".format(paquete.cantidad_pagos_actual, paquete.saldo, paquete.total))

def main4():
	paquete_terrestre = TerrestreEstandar(3000, 200, "11/30/19", nombre_paquete="Camboriu", incluye_descripcion="holel, desayuno, almuerzo")
	paquete_personalizado = AereoPersonalizado(nombre_paquete="Punta Cana", incluye_descripcion="holel, desayuno, almuerzo")
	paquete_personalizado.set_precio(5000)
	paquete_personalizado.set_senha(500)
	paquete_personalizado.set_fecha_de_viaje("18/11/2020")

	usuario = Usuario( "Victor", "Cubas", "4028760", "18/11/1991", 20, "Paraguay" )
	usuario.agregar_contacto( Telefono( "0971991960", "personal") )
	usuario.agregar_contacto( Telefono( "0985871759", "tigo" ) )
	usuario.agregar_paquete(paquete_terrestre)

	#usuarios = []
	#usuarios.append(usuario)

	paquete_terrestre.agregar_usuario(usuario)
	paquete_personalizado.agregar_usuario(usuario)

	usuario = Usuario( "Andrea", "Escurra", "4028760", "18/11/1991", 20, "Paraguay" )
	#usuarios.append(usuario)
	usuario.agregar_paquete(paquete_personalizado)
	paquete_terrestre.agregar_usuario(usuario)
	
	paquete_personalizado.agregar_usuario(usuario)

	guardar_paquete(paquete_terrestre)
	guardar_paquete(paquete_personalizado)
	paquetes = listar_paquetes( )

	for paquete_aux in paquetes:
		print("\nPAQUETE: " + paquete_aux.nombre_paquete + "\tTIPO: " + paquete_aux.TRASLADO)

		usuarios = paquete_aux.get_usuarios()

		for usu in usuarios:
			print( usu.__str__())

	print("\nUSUARIOS")
	for usu in usuarios:
		print(usu.__str__() )

	factura = FacturaContado("Hugo Balbuena", "00021", "2019-06-26", "10:00")
	i = 0
	for usu in usuarios:
		factura.agregar_usuario(usu)
		factura.agregar_paquete(paquetes[i])
		factura.agregar_monto(20000)
		i += 1

	print("\nNombre o rason social:" + factura.nombre_razon_social)
	print("Cantidad de paquetes: {}".format(factura.cantidad_paquetes))
	i = 0
	for i in range(factura.cantidad_paquetes):
		print(factura.usuarios[i].__str__())
		print(factura.paquetes[i].get_nombre())
		print(factura.montos[i])
		print()

	print("PAQUETES POR USUARIO")
	for usu in usuarios:
		print(usu.__str__())
		paquetes = usu.get_paquetes()
		for paq in paquetes:
			print(paq.get_nombre())

	factura.liquidar()

	print("PAQUETES DESPUES DE FACTURAR")
	for usu in usuarios:
		print(usu.__str__())
		paquetes = usu.get_paquetes()
		for paq in paquetes:
			print("Cantidad de pagos: {} Saldo: {} Total: {}".format(paq.cantidad_pagos_actual, paq.saldo, paq.total))



def main3( ):
	'''paquete = Paquete("Camboriu", "11/30/19", 3000, 200, "holel, desayuno, almuerzo")

	usuario = Usuario( "Victor", "Cubas", "4028760", "18/11/1991", 20, "Paraguay" )
	usuario.agregar_contacto( Telefono( "0971991960", "personal") )
	usuario.agregar_contacto( Telefono( "0985871759", "tigo" ) )

	paquete.agregar_usuario(usuario)

	usuario = Usuario( "Andrea", "cubas", "4028760", "18/11/1991", 20, "Paraguay" )
	paquete.agregar_usuario(usuario)

	guardar_paquete(paquete)
	paquetes = listar_paquetes( )

	for paquete_aux in paquetes:
		print("\nPAQUETE: " + paquete_aux.nombre_paquete)

		usuarios = paquete_aux.get_usuarios()

		for usu in usuarios:
			print( usu.__str__())
	'''


	t1 = datetime.date(2019,6,11)
	print(t1)

	t2 = datetime.date.today()
	print(t2)

	if t1 < t2:
		print("t1 menor a t2")
	elif t1 > t2:
		print("t1 mayor a t2")
	else:
		print("son iguales las fechas")


	t3 = datetime.time(1, 2, 3)
	print('ANHO: ' + str(t1.year))
	print(t3)
	#print("t1-t2: " + (t2 - t1) )
	#print(date_object.strftime("%c"))


	t4 = time.strftime("%H:%M:%S")
	print( t4 )

	#print(len(paquetes))


def guardar_paquete(paquete):

		result = []
		try:
			#print("aqui1")
			archivo = open('paquete.pickle', 'rb')
			#print("aqui1")
			result = pickle.load(archivo)
			archivo.close()
			archivoNuevo = open('paquete.pickle', 'wb')
			result.append(paquete)
			pickle.dump(result, archivoNuevo)
			archivoNuevo.close()
		except IOError:
			#print("aqui2")
			archivoNuevo = open('paquete.pickle', 'wb')
			result.append(paquete)
			pickle.dump(result, archivoNuevo)
			archivoNuevo.close()
		return

def listar_paquetes():
		result = []
		try:
			archivo = open('paquete.pickle', 'rb')
			result = pickle.load(archivo)
			archivo.close()
			return result
		except IOError:
			return result
		return
	

def main2( ):
	usuario = Usuario( "Victor", "Cubas", "4028760", "18/11/1991", 20, "Paraguay" )
	print( usuario.__str__( ))

	usuario.agregar_contacto( Telefono( "0971991960", "personal") )
	usuario.agregar_contacto( Telefono( "0985871759", "tigo" ) )

	contactos = usuario.get_contactos( )

	for contacto in contactos:
		print( contacto.__str__())

	usuario.eliminar_contacto( 1 )
	contactos = usuario.get_contactos( )

	for contacto in contactos:
		print( contacto.__str__())

def main1( ):
	#contacto = Contacto( "tigo" )
	#print( contacto.__str__( ) )
	tel1 = Telefono( "0971991960", "personal")
	print( tel1.__str__() )
	#print( tel.get_descripcion( ))

	tel2 = Telefono( "0985871759", "tigo")

	lista = [ ]
	lista.append( tel1 )
	lista.append( tel2 )

	print( "\nimprimiendo la lista...\n" )
	for lista_aux in lista:
		print(lista_aux.__str__())

if ( __name__ == "__main__"):
    #main1()
	#main2()
	#main3()
	#main4()
	main5()
	#main6()
