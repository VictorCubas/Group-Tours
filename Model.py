#model.py

import pickle
from Usuario import Usuario
import datetime
from time import sleep
from exceptions.NombreException import NombreException
from exceptions.ApellidoException import ApellidoException
from exceptions.TelefonoIncorrectoException import TelefonoIncorrectoException
from exceptions.CorreoIncorrectoException import CorreoIncorrectoException
from exceptions.CedulaIncorrectaException import CedulaIncorrectaException
from TerrestreEstandar import TerrestreEstandar
from TerrestrePersonalizado import TerrestrePersonalizado
from AereoEstandar import AereoEstandar
from AereoPersonalizado import AereoPersonalizado
from PreVenta import PreVenta
from TemporizadorVigencia import TemporizadorVigencia
from TemporizadorDeleteFile import TemporizadorDeleteFile


class Model:
	HORA = '05:00:00'
	HORA_COMPROBACION = '00:00:00'

	def __init__(self):
		self.paquetes_result = []
		self.encontrando = True
		self.pos_result_busqueda = []
		self.pos_result_busqueda_cliente = []

		self.clientes_result = []

		self.t_existe_archivo = None
		self.t = None

	def ejecutar_temporizador(self):
		print('ejecutando hilos...')
		#Instanciamos nuestra clase Temporizador
		self.t_existe_archivo = TemporizadorDeleteFile(Model.HORA_COMPROBACION, 1)
		#Iniciamos el hilo
		self.t_existe_archivo.start()

		#Instanciamos nuestra clase Temporizador
		self.t = TemporizadorVigencia(Model.HORA, 1)
		#Iniciamos el hilo
		self.t.start()

	def stop_hilos(self):
		self.t_existe_archivo.stop()
		self.t.stop()

	def buscar_cliente_por_apellido(self, apellido_cliente, cantidad_de_filtros, encontrando):
		'''
		Busca una lista de paquetes en base al nombre dado como parametro y es almacenado
		como atributo de la clase
		'''
		print('buscando por apellido...')

		encontrando = False
		apellido_cliente = apellido_cliente.lower()
		clientes_result_aux = []

		pos_result_busqueda_aux = []
		esta_vacio_el_vector = False

		#el patron debe teber por lo menos 3 caracteres
		if len(apellido_cliente) > 2:
			if len(self.clientes_result) == 0 or cantidad_de_filtros == 1:
				clientes = Model.abrir_archivo_clientes()
				self.pos_result_busqueda_cliente = []
			else:
				clientes = self.clientes_result

			if len(self.pos_result_busqueda_cliente) == 0:
				esta_vacio_el_vector = True

			i = -1
			for cliente in clientes:
				i += 1
				if Model.boyer_moore_busqueda_patron(apellido_cliente, cliente.get_apellido().lower()):
					clientes_result_aux.append(cliente)

					if esta_vacio_el_vector:
						pos_result_busqueda_aux.append(i)
					else:
						pos_result_busqueda_aux.append(self.pos_result_busqueda_cliente[i])

					encontrando = True

		self.clientes_result = clientes_result_aux
		self.pos_result_busqueda_cliente = pos_result_busqueda_aux

		return [self.clientes_result, encontrando, self.pos_result_busqueda_cliente]

	def buscar_cliente_por_cedula(self, cedula_cliente, cantidad_de_filtros, encontrando):
		'''
		Busca una lista de paquetes en base al nombre dado como parametro y es almacenado
		como atributo de la clase
		'''
		print('buscando por cedula...')

		encontrando = False
		clientes_result_aux = []

		pos_result_busqueda_aux = []
		esta_vacio_el_vector = False

		#el patron debe teber por lo menos 3 caracteres
		if len(cedula_cliente) > 2:
			if len(self.clientes_result) == 0 or cantidad_de_filtros == 1:
				clientes = Model.abrir_archivo_clientes()
				self.pos_result_busqueda_cliente = []
			else:
				clientes = self.clientes_result

			if len(self.pos_result_busqueda_cliente) == 0:
				esta_vacio_el_vector = True

			i = -1
			for cliente in clientes:
				i += 1
				if Model.boyer_moore_busqueda_patron(str(cedula_cliente), str(cliente.get_cedula())):
				#if cedula_cliente == cliente.get_cedula():
					clientes_result_aux.append(cliente)

					if esta_vacio_el_vector:
						pos_result_busqueda_aux.append(i)
					else:
						pos_result_busqueda_aux.append(self.pos_result_busqueda_cliente[i])

					encontrando = True

		self.clientes_result = clientes_result_aux
		self.pos_result_busqueda_cliente = pos_result_busqueda_aux

		return [self.clientes_result, encontrando, self.pos_result_busqueda_cliente]

	def buscar_cliente_por_nombre(self, nombre_cliente, cantidad_de_filtros, encontrando):
		'''
		Busca una lista de paquetes en base al nombre dado como parametro y es almacenado
		como atributo de la clase
		'''
		print('buscando por nombre...')

		encontrando = False
		nombre_cliente = nombre_cliente.lower()
		clientes_result_aux = []

		pos_result_busqueda_aux = []
		esta_vacio_el_vector = False

		#el patron debe teber por lo menos 3 caracteres
		if len(nombre_cliente) > 2:
			if len(self.clientes_result) == 0 or cantidad_de_filtros == 1:
				clientes = Model.abrir_archivo_clientes()
				self.pos_result_busqueda_cliente = []
			else:
				clientes = self.clientes_result

			if len(self.pos_result_busqueda_cliente) == 0:
				esta_vacio_el_vector = True

			i = -1
			for cliente in clientes:
				i += 1
				if Model.boyer_moore_busqueda_patron(nombre_cliente, cliente.get_nombre().lower()):
					clientes_result_aux.append(cliente)

					if esta_vacio_el_vector:
						pos_result_busqueda_aux.append(i)
					else:
						pos_result_busqueda_aux.append(self.pos_result_busqueda_cliente[i])

					encontrando = True

		self.clientes_result = clientes_result_aux
		self.pos_result_busqueda_cliente = pos_result_busqueda_aux

		return [self.clientes_result, encontrando, self.pos_result_busqueda_cliente]

	def buscar_paquete_por_nombre(self, nombre_paquete, cantidad_de_filtros, encontrando):
		'''
		Busca una lista de paquetes en base al nombre dado como parametro y es almacenado
		como atributo de la clase
		'''
		print('buscando por nombre...')

		encontrando = False
		nombre_paquete = nombre_paquete.lower()
		paquetes_result_aux = []

		pos_result_busqueda_aux = []
		esta_vacio_el_vector = False

		#el patron debe teber por lo menos 3 caracteres
		if len(nombre_paquete) > 2:
			if len(self.paquetes_result) == 0 or cantidad_de_filtros == 1:
				paquetes = Model.abrir_archivo_paquetes()
				self.pos_result_busqueda = []
			else:
				paquetes = self.paquetes_result

			if len(self.pos_result_busqueda) == 0:
				esta_vacio_el_vector = True

			i = -1
			for paquete in paquetes:
				i += 1
				if Model.boyer_moore_busqueda_patron(nombre_paquete, paquete.get_nombre().lower()):
					paquetes_result_aux.append(paquete)

					if esta_vacio_el_vector:
						pos_result_busqueda_aux.append(i)
					else:
						pos_result_busqueda_aux.append(self.pos_result_busqueda[i])

					encontrando = True
					#print('encontrando: ' + str(encontrando))

		self.paquetes_result = paquetes_result_aux
		self.pos_result_busqueda = pos_result_busqueda_aux

		return [self.paquetes_result, encontrando, self.pos_result_busqueda]

	def buscar_paquete_por_vigencia(self, esta_vigente, cantidad_de_filtros, filtro_anho_seleccionado, filtro_tipo_seleccionado,
																				filtro_sub_tipo_seleccionado, encontrando):
		'''
		Busca una lista de paquetes en base a si esta vigente o no el paquete, el cual es dado
		como parametro y es almacenado como atributo de la clase
		'''
		print('buscando por vigencia...')
		esta_vigente_aux = None

		if esta_vigente == 'si':
			esta_vigente_aux = True
		elif esta_vigente == 'no':
			esta_vigente_aux = False

		encontrando = False
		paquetes_result_aux = []
		pos_result_busqueda_aux = []
		esta_vacio_el_vector = False

		if esta_vigente != 'ninguno':
			if len(self.paquetes_result) == 0 or cantidad_de_filtros == 1:
				paquetes = Model.abrir_archivo_paquetes()
				self.pos_result_busqueda = []
			else:
				if cantidad_de_filtros == 2:
					if filtro_anho_seleccionado or filtro_tipo_seleccionado or filtro_sub_tipo_seleccionado:
						paquetes = Model.abrir_archivo_paquetes()
						self.pos_result_busqueda = []
					else:
						paquetes = self.paquetes_result
				else:
					paquetes = self.paquetes_result

			if len(self.pos_result_busqueda) == 0:
				esta_vacio_el_vector = True

			i = -1
			for paquete in paquetes:
				i += 1
				if paquete.get_esta_vigente() == esta_vigente_aux:
					paquetes_result_aux.append(paquete)

					if esta_vacio_el_vector:
						pos_result_busqueda_aux.append(i)
					else:
						pos_result_busqueda_aux.append(self.pos_result_busqueda[i])

					encontrando = True

			self.paquetes_result = paquetes_result_aux
			self.pos_result_busqueda = pos_result_busqueda_aux
		else:
			if cantidad_de_filtros != 0:
				encontrando = True

		if cantidad_de_filtros == 0:
			self.paquetes_result = []
			self.pos_result_busqueda = []

		return [self.paquetes_result, encontrando, self.pos_result_busqueda]

	def buscar_paquete_por_anho(self, anho, cantidad_de_filtros):
		'''
		Busca una lista de paquetes en base al anho en la que se realiza el viaje, el cual es dado
		como parametro y es almacenado como atributo de la clase
		'''

		print('buscando por anho... ' + str(anho))
		encontrando = False
		paquetes_result_aux = []
		pos_result_busqueda_aux = []
		esta_vacio_el_vector = False

		if anho != '':
			if len(self.paquetes_result) == 0 or cantidad_de_filtros == 1:
				paquetes = Model.abrir_archivo_paquetes()
				self.pos_result_busqueda = []
			else:
				paquetes = self.paquetes_result

			if len(self.pos_result_busqueda) == 0:
				esta_vacio_el_vector = True

			i = -1
			for paquete in paquetes:
				i += 1
				if paquete.get_fecha_de_viaje() != None and paquete.get_anho_de_viaje() == int(anho):
					paquetes_result_aux.append(paquete)

					if esta_vacio_el_vector:
						pos_result_busqueda_aux.append(i)
					else:
						pos_result_busqueda_aux.append(self.pos_result_busqueda[i])

					encontrando = True

			self.paquetes_result = paquetes_result_aux
			self.pos_result_busqueda = pos_result_busqueda_aux
		else:
			if cantidad_de_filtros != 0:
				encontrando = True

		if cantidad_de_filtros == 0:
			self.paquetes_result = []
			self.pos_result_busqueda = []

		return [self.paquetes_result, encontrando, self.pos_result_busqueda]

	def buscar_paquete_por_tipo(self, tipo, cantidad_de_filtros):
		'''
		Busca una lista de paquetes en base al anho en la que se realiza el viaje, el cual es dado
		como parametro y es almacenado como atributo de la clase
		'''

		print('buscando por tipo... ')
		encontrando = False
		paquetes_result_aux = []
		pos_result_busqueda_aux = []
		esta_vacio_el_vector = False

		if tipo != '':
			if len(self.paquetes_result) == 0 or cantidad_de_filtros == 1:
				paquetes = Model.abrir_archivo_paquetes()
				self.pos_result_busqueda = []
			else:
				paquetes = self.paquetes_result

			if len(self.pos_result_busqueda) == 0:
				esta_vacio_el_vector = True

			i = -1
			for paquete in paquetes:
				i += 1
				if paquete.TRASLADO == tipo:
					paquetes_result_aux.append(paquete)
					if esta_vacio_el_vector:
						pos_result_busqueda_aux.append(i)
					else:
						pos_result_busqueda_aux.append(self.pos_result_busqueda[i])

					encontrando = True

			self.paquetes_result = paquetes_result_aux
			self.pos_result_busqueda = pos_result_busqueda_aux
		else:
			if cantidad_de_filtros != 0:
				encontrando = True

		if cantidad_de_filtros == 0:
			self.paquetes_result = []
			self.pos_result_busqueda = []

		return [self.paquetes_result, encontrando, self.pos_result_busqueda]

	def buscar_paquete_por_sub_tipo(self, sub_tipo, cantidad_de_filtros):
		'''
		Busca una lista de paquetes en base al anho en la que se realiza el viaje, el cual es dado
		como parametro y es almacenado como atributo de la clase
		'''

		print('buscando por subtipo... ')
		encontrando = False
		paquetes_result_aux = []
		pos_result_busqueda_aux = []
		esta_vacio_el_vector = False

		if len(self.paquetes_result) == 0 or cantidad_de_filtros == 1:
			paquetes = Model.abrir_archivo_paquetes()
			self.pos_result_busqueda = []
		else:
			paquetes = self.paquetes_result

		if len(self.pos_result_busqueda) == 0:
				esta_vacio_el_vector = True

		i = -1
		for paquete in paquetes:
			i += 1
			if paquete.TIPO == sub_tipo:
				paquetes_result_aux.append(paquete)
				if esta_vacio_el_vector:
					pos_result_busqueda_aux.append(i)
				else:
					pos_result_busqueda_aux.append(self.pos_result_busqueda[i])

				encontrando = True

		self.paquetes_result = paquetes_result_aux
		self.pos_result_busqueda = pos_result_busqueda_aux

		if cantidad_de_filtros == 0:
			self.paquetes_result = []
			self.pos_result_busqueda = []

		return [self.paquetes_result, encontrando, self.pos_result_busqueda]


	@staticmethod
	def boyer_moore_busqueda_patron(pattern, text):
		m = len(pattern)
		n = len(text)
		if m > n: return False
		skip = []
		for k in range(256): skip.append(m)
		for k in range(m - 1): skip[ord(pattern[k])] = m - k - 1
		skip = tuple(skip)
		k = m - 1
		while k < n:
		    j = m - 1; i = k
		    while j >= 0 and text[i] == pattern[j]:
		        j -= 1; i -= 1
		    if j == -1: return True
		    k += skip[ord(text[k])]
		return False

	@staticmethod
	def abrir_archivo_clientes():
		paquetes = []

		try:
			archivo = open('data_base_files/clientes.pickle', 'rb')
			clientes = pickle.load(archivo)
			archivo.close()
			return clientes
		except IOError:
			return clientes
		return

	@staticmethod
	def abrir_archivo_paquetes():
		paquetes = []

		try:
			archivo = open('data_base_files/paquete.pickle', 'rb')
			paquetes = pickle.load(archivo)
			archivo.close()
			return paquetes
		except IOError:
			return paquetes
		return

	def	es_la_pre_venta_actual(self, pre_venta):
		fecha_hoy = datetime.date.today()
		fecha_inicio = pre_venta.get_fecha_inicio()
		fecha_fin = pre_venta.get_fecha_fin()
	
		if fecha_hoy >= fecha_inicio and fecha_hoy <= fecha_fin:
			return True

		return False

	def generar_lista_nacionalidades(self):
		lista_nacionalidades = []
		lista_nacionalidades.append('')

		archivo = open('data_base_files/nacionalidades.txt', 'r')
		for nacionalidad in archivo.readlines():
			lista_nacionalidades.append(nacionalidad)
	
		archivo.close() 
		return lista_nacionalidades

	def generar_lista_edades(self):
		lista_edades = []
		lista_edades.append('')

		for i in range(111):
			lista_edades.append(i)

		return lista_edades

	def generar_lista_anhos(self):
		date = datetime.date.today()

		lista_anhos = []
		lista_anhos.append('')
		
		for i in range(date.year + 3, 2015,-1):
			lista_anhos.append(i)

		return lista_anhos

	def validar_datos_cliente(self, nombre, apellido, cedula, fecha_nacimiento, edad, nacionalidad, telefono1, telefono2, email):
		print('validando los datos del cliente...')

		try:
			if nombre == '' or nombre == None:
				raise NombreException('Nombre incorrecto')

			if apellido == '' or apellido == None:
				raise ApellidoException('Apellido incorrecto')

			if cedula is None:
				raise CedulaIncorrectaException('Debe introducir una cedula')

			if fecha_nacimiento is None:
				raise Exception('Debe introducir una fecha')

			if edad is '':
				raise Exception('Debe introducir una edad')

			if nacionalidad is '':
				raise Exception('Debe introducir la nacionalidad')

			if telefono1 is not '':
				try:
					if len(telefono1) is not 10:
						raise TelefonoIncorrectoException('Telefono 1 incorrecto')

					telefono1 = int(telefono1)
				except TelefonoIncorrectoException:
						raise
				except Exception:
					raise TelefonoIncorrectoException('Telefono 1 incorrecto')

			if telefono2 is not '':
				try:
					if len(telefono2) is not 10:
						raise TelefonoIncorrectoException('Telefono 2 incorrecto')

					telefono2 = int(telefono2)
				except TelefonoIncorrectoException:
						raise
				except Exception:
					raise TelefonoIncorrectoException('Telefono 2 incorrecto')

			#************************************
			#	Agregar validacion de correo	*
			#************************************

		except NombreException:
			raise
		except ApellidoException:
			raise
		except Exception:
			raise
		except TelefonoIncorrectoException:
			raise

	def validar_datos_paquete(self, nombre, tipo, sub_tipo, esta_vigente, fecha, precio, senha, incluye, cant_pasajeros, banderita):
		print('validando...')

		try:
			if nombre == '':
				raise NombreException('Nombre incorrecto')

			if tipo == '':
				raise Exception('Tipo incorrecto')

			if sub_tipo == '':
				raise Exception('Sub-Tipo incorrecto')

			if esta_vigente == '':
				raise Exception('Vigencia incorrecto')

			if tipo == 'Terrestre' and sub_tipo == 'Estandar':
				if len(fecha) == 0:
					raise Exception('Debe introducir una fecha')

			#if precio == None or senha == None:
			#	raise Exception('Debes completar todos los campos')

			if precio == '':
				raise Exception('Precio incorrecto')

			precio = int(precio)
			if senha == '':
				raise Exception('Seña incorrecto')

			senha = int(senha)
			if senha > precio:
				raise Exception('La seña es mayor al precio')

			if cant_pasajeros != '' and cant_pasajeros != '--':
				cant_pasajeros = int(cant_pasajeros)

		except ValueError as e:
			raise ValueError('Precio o Seña incorrecto')
		except Exception:
			raise

	def validar_datos_paquete_editado(self, nombre, tipo, sub_tipo, esta_vigente, fecha, precio, senha, incluye, cant_pasajeros, banderita):
		print('validando...')

		try:
			if nombre == '':
				raise NombreException('Nombre incorrecto')

			if tipo == '':
				raise Exception('Tipo incorrecto')

			if sub_tipo == '':
				raise Exception('Sub-Tipo incorrecto')

			if esta_vigente == '':
				raise Exception('Vigencia incorrecto')

			if tipo == 'Terrestre' and sub_tipo == 'Estandar':
				if fecha == None:
					raise Exception('Debe introducir una fecha')

			#if precio == None or senha == None:
			#	raise Exception('Debes completar todos los campos')

			if precio == '':
				raise Exception('Precio incorrecto')

			precio = int(precio)
			if senha == '':
				raise Exception('Seña incorrecto')

			senha = int(senha)
			if senha > precio:
				raise Exception('La seña es mayor al precio')

			if cant_pasajeros != '' and cant_pasajeros != '--':
				cant_pasajeros = int(cant_pasajeros)

		except ValueError as e:
			raise ValueError('Precio o Seña incorrecto')
		except Exception:
			raise


	def validar_datos_pre_venta(self, precio, senha, monto_cuota, cant_cuotas, fecha_inicio, fecha_fin):
		try:
			if precio == None or senha == None or monto_cuota == None:
				raise Exception('Debes completar todos los campos')

			precio = int(precio)

			if senha == '':
				raise Exception('Seña incorrecta')

			senha = int(senha)
			if senha > precio:
				raise Exception('La seña es mayor al precio')

			monto_cuota = int(monto_cuota)
			if monto_cuota == '':
				raise Exception('Monto cuota incorrecto')

			cant_cuotas = int(cant_cuotas)
			if cant_cuotas == '':
				raise Exception('Cantidad de cuotas incorrecta')

			if fecha_inicio is None:
				raise Exception('Fecha inicio incorrecta')

			if fecha_fin is None:
				raise Exception('Fecha fin incorrecta')

			if fecha_fin < fecha_inicio:
				raise Exception('Fecha final es menor a la fecha inicial')

			if fecha_fin == fecha_inicio:
				raise Exception('Fecha final es igual a la fecha inicial')

		except ValueError as e:
			raise ValueError('Algunos valores son incorrecto')
		except Exception:
			raise

	def crear_paquete(self, nombre, tipo, sub_tipo, esta_vigente, fecha, precio, senha, incluye, cant_pasajeros):
		print('Model: creando paquete...')
		paquete = None

		print()
		if esta_vigente == 'Si':
			esta_vigente = True
		else:
			esta_vigente = False

		precio = int(precio)
		senha = int(senha)

		if tipo == 'Terrestre':
			if sub_tipo == 'Estandar':
				paquete = TerrestreEstandar(precio, senha, fecha, nombre_paquete=nombre)
			else:
				paquete = TerrestrePersonalizado(precio, senha, nombre_paquete=nombre)
				paquete.set_fecha_de_viaje(fecha)

			if cant_pasajeros != '' and cant_pasajeros != '--':
				paquete.set_cantidad_de_usuarios_total(int(cant_pasajeros))
		else:
			if sub_tipo == 'Estandar':
				paquete = AereoEstandar(precio, senha, nombre_paquete=nombre)
				paquete.set_fecha_de_viaje(fecha)
			else:
				paquete = AereoPersonalizado(precio, senha, nombre_paquete=nombre)
				paquete.set_fecha_de_viaje(fecha)

		if tipo == 'Aereo' or (tipo == 'Terrestre' and sub_tipo != 'Estandar'):
			paquete.set_fecha_de_viaje(fecha)

		paquete.set_esta_vigente(esta_vigente)
		paquete.set_incluye_descripcion(incluye)
		return paquete

	def crear_pre_venta(self, precio, senha, monto_cuota, cant_cuotas, fecha_inicio, fecha_fin):
		precio = int(precio)
		senha = int(senha)
		monto_cuota = int(monto_cuota)
		cant_cuotas = int(cant_cuotas)

		pre_venta = PreVenta(precio, senha, monto_cuota, cant_cuotas, fecha_inicio, fecha_fin)
		return pre_venta

	def guardar_cliente(self, cliente):
		result = []
		print('Model: guardando cliente...')

		try:
			archivo = open('data_base_files/clientes.pickle', 'rb')
			result = pickle.load(archivo)
			archivo.close()
			archivoNuevo = open('data_base_files/clientes.pickle', 'wb')
			result.append(cliente)
			pickle.dump(result, archivoNuevo)
			archivoNuevo.close()
		except IOError:
			archivoNuevo = open('data_base_files/clientes.pickle', 'wb')
			result.append(cliente)
			pickle.dump(result, archivoNuevo)
			archivoNuevo.close()
		return

	def guardar_paquete(self, paquete):
		result = []
		print('Model: guardando paquete...')

		try:
			archivo = open('data_base_files/paquete.pickle', 'rb')
			result = pickle.load(archivo)
			archivo.close()
			archivoNuevo = open('data_base_files/paquete.pickle', 'wb')
			result.append(paquete)
			pickle.dump(result, archivoNuevo)
			archivoNuevo.close()
		except IOError:
			archivoNuevo = open('data_base_files/paquete.pickle', 'wb')
			result.append(paquete)
			pickle.dump(result, archivoNuevo)
			archivoNuevo.close()
		return

	def guardar_paquete_editado(self, paquete, pos_paquete):
		result = []
		print('guardando paquete...')

		try:
			archivo = open('data_base_files/paquete.pickle', 'rb')
			result = pickle.load(archivo)
			archivo.close()
			archivoNuevo = open('data_base_files/paquete.pickle', 'wb')
			result[pos_paquete] = paquete
			pickle.dump(result, archivoNuevo)
			archivoNuevo.close()
		except IOError:
			archivoNuevo = open('data_base_files/paquete.pickle', 'wb')
			result[pos_paquete] = paquete
			pickle.dump(result, archivoNuevo)
			archivoNuevo.close()
		return

	def guardar_paquetes(self, paquetes):
		print('guardando paquetes...')

		try:
			archivoNuevo = open('data_base_files/paquete.pickle', 'wb')
			pickle.dump(paquetes, archivoNuevo)
			archivoNuevo.close()
		except IOError:
			archivoNuevo = open('data_base_files/paquete.pickle', 'wb')
			pickle.dump(paquetes, archivoNuevo)
			archivoNuevo.close()
		return

	def listar_paquetes(self):
		result = []
		try:
			archivo = open('data_base_files/paquete.pickle', 'rb')
			result = pickle.load(archivo)
			archivo.close()
			return result
		except IOError:
			return result
		return

	def generar_archivo_ventana(self, pos_paquete):
		#confirmacion = self.buscar_repetido(pos_paquete)

		#if confirmacion is False: return

		result = []
		print('Model: guardando info de la ventana abierta...')
		try:
			archivo = open('data_base_files/ventanas_abiertas.pickle', 'rb')
			result = pickle.load(archivo)
			archivo.close()
			archivoNuevo = open('data_base_files/ventanas_abiertas.pickle', 'wb')
			result.append(pos_paquete)
			pickle.dump(result, archivoNuevo)
			archivoNuevo.close()
		except IOError:
			archivoNuevo = open('data_base_files/ventanas_abiertas.pickle', 'wb')
			result.append(pos_paquete)
			pickle.dump(result, archivoNuevo)
			archivoNuevo.close()
		return

	def si_ventana_abierta(self, pos_paquete):
		result = []
		try:
			archivo = open('data_base_files/ventanas_abiertas.pickle', 'rb')
			result = pickle.load(archivo)
			archivo.close()

			for pos in result:
				if pos == pos_paquete:
					return True

			return False
		except IOError:
			return False
		return

	'''def listar_usuarios(self):
		result = []
		try:
			archivo = open('usuario.pickle', 'rb')
			result = pickle.load(archivo)
			archivo.close()
			return result
		except IOError:
			return result
		return
	
	def buscarPorCedula(self, cedula):
		noEncontrado = "Persona no encontrada"
		try:
			archivo = open('persona.pickle', 'rb')
			listaPersonas = pickle.load(archivo)
			archivo.close()
			for persona in listaPersonas:
				if persona.documento == cedula:
					result = {"Nombre": persona.nombre, "Apellido": persona.apellido}
					return result
			return noEncontrado
		except IOError:
			return noEncontrado
		return
	
	def guardar_usuario(self, usuario):

		result = []
		try:
			archivo = open('usuario.pickle', 'rb')
			result = pickle.load(archivo)
			archivo.close()
			archivoNuevo = open('usuario.pickle', 'wb')
			result.append(usuario)
			pickle.dump(result, archivoNuevo)
			archivoNuevo.close()
		except IOError:
			archivoNuevo = open('usuario.pickle', 'wb')
			result.append(usuario)
			pickle.dump(result, archivoNuevo)
			archivoNuevo.close()
		return

	def liquidar(self, factura):
		factura.liquidar()

	def senhar(self, factura):
		factura.senhar():'''
