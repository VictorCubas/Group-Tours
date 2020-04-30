#controller.py
from Model import Model
from View import View
from tkinter import ttk
from tkinter import *
from exceptions.NombreException import NombreException
from exceptions.ApellidoException import ApellidoException
from exceptions.TelefonoIncorrectoException import TelefonoIncorrectoException
from exceptions.CorreoIncorrectoException import CorreoIncorrectoException
from exceptions.CedulaIncorrectaException import CedulaIncorrectaException
from Paquete import Paquete
from Usuario import Usuario
from Nacionalidad import Nacionalidad
from Telefono import Telefono
from Correo import Correo

class Controller:

	def __init__(self):
		self.model = Model()
		print('iniciando el controlador...1')
		self.parent = Tk()
		self.view = View(self, self.parent)
		print('iniciando el controlador...2')
		self.parent.mainloop()
		print('iniciando el controlador...3')

	def ejecutar_temporizador(self):
		self.model.ejecutar_temporizador()

	def stop_hilos(self):
		self.model.stop_hilos()

	def buscar_cliente(self, **kwargs):
		result = []
		encontrando = True
		result_encontrando = [result, encontrando, []]

		cantidad_de_filtros = self.get_cantidad_de_filtros_busqueda_cliente(kwargs)
		for key, value in kwargs.items():
			if result_encontrando[1] and key == 'content1' and value != '':
				result_encontrando = self.model.buscar_cliente_por_nombre(value, cantidad_de_filtros, result_encontrando[1])
			elif result_encontrando[1] and key == 'content2' and value != '':
				result_encontrando = self.model.buscar_cliente_por_apellido(value, cantidad_de_filtros, result_encontrando[1])
			elif result_encontrando[1] and key == 'content3' and value != '':
				result_encontrando = self.model.buscar_cliente_por_cedula(value, cantidad_de_filtros, result_encontrando[1])

		return [result_encontrando[0], result_encontrando[2]]

	def get_cantidad_de_filtros_busqueda_cliente(self, kwargs):
		filtros = 0

		for key, value in kwargs.items():
			if key == 'content1' and value != '':
				filtros += 1
			elif key == 'content2' and value != '':
				filtros += 1
			elif key == 'content3' and value != '':
				filtros += 1

		return filtros

	def buscar_paquete(self, **kwargs):
		#Busca el paquete por nombre, vigencia o por anho (de acuerdo al filtro selccionado)
		result = []
		encontrando = True
		result_encontrando = [result, encontrando, []]
		self.filtro_anho_seleccionado = False
		self.filtro_tipo_seleccionado = False
		self.filtro_sub_tipo_seleccionado = False

		cantidad_de_filtros = self.get_cantidad_de_filtros(kwargs)
		#print('cantidad_de_filtros: ' + str(cantidad_de_filtros))

		for key, value in kwargs.items():
			if result_encontrando[1] and key == 'content1' and value != '':
				#print('1')
				result_encontrando = self.model.buscar_paquete_por_nombre(value, cantidad_de_filtros, result_encontrando[1])
				#print(str(result_encontrando[1]))
			elif result_encontrando[1] and key == 'content2':
				#print('2')
				result_encontrando = self.model.buscar_paquete_por_vigencia(value, cantidad_de_filtros, self.filtro_anho_seleccionado,
										self.filtro_tipo_seleccionado, self.filtro_sub_tipo_seleccionado, result_encontrando[1])
				#print(str(result_encontrando[1]))
			elif result_encontrando[1] and key == 'content3' and value != '':
				#print('3: ' + value)
				result_encontrando = self.model.buscar_paquete_por_anho(value, cantidad_de_filtros)
			elif result_encontrando[1] and key == 'content4' and value != '':
				#print('4: ' + value)
				result_encontrando = self.model.buscar_paquete_por_tipo(value, cantidad_de_filtros)
			elif result_encontrando[1] and key == 'content5' and value != '':
				#print('5: ' + value)
				result_encontrando = self.model.buscar_paquete_por_sub_tipo(value, cantidad_de_filtros)

		return [result_encontrando[0], result_encontrando[2]]

	def get_cantidad_de_filtros(self, kwargs):
		filtros = 0
		for key, value in kwargs.items():
			if key == 'content1' and value != '':
				filtros += 1
			elif key == 'content2' and value != 'ninguno':
				filtros += 1
			elif key == 'content3' and value != '':
				self.filtro_anho_seleccionado = True
				filtros += 1
			elif key == 'content4' and value != '':
				self.filtro_tipo_seleccionado = True
				filtros += 1
			elif key == 'content5' and value != '':
				self.filtro_sub_tipo_seleccionado = True
				filtros += 1

		return filtros

	def generar_lista_edades(self):
		return self.model.generar_lista_edades()

	def generar_lista_anhos(self):
		return self.model.generar_lista_anhos()

	def generar_lista_nacionalidades(self):
		return self.model.generar_lista_nacionalidades()

	def agregar_imagen(self, frame_parent, frame_imagen, label_logo, imagenes):
		self.view.view_agregar_imagen(frame_parent, frame_imagen, label_logo, imagenes)

	def guardar_cliente(self, nombre, apellido, cedula, fecha_nacimiento, edad, nacionalidad, telefono1, telefono2, email, frame):
		try:
			self.model.validar_datos_cliente(nombre, apellido, cedula, fecha_nacimiento, edad, nacionalidad, telefono1, telefono2, email)
		except NombreException as e:
			self.view.view_show_message(False, e)
		except ApellidoException as e:
			self.view.view_show_message(False, e)
		except Exception as e:
			self.view.view_show_message(False, e)
		except TelefonoIncorrectoException as e:
			self.view.view_show_message(False, e)
		else:
			cliente = Usuario(nombre, apellido, cedula, fecha_nacimiento, edad, nacionalidad)

			if telefono1 is not None:
				cliente.set_telefono_primario(Telefono(telefono1, ''))

			if telefono2 is not None:
				cliente.set_telefono_secundario(Telefono(telefono2, ''))

			if email is not None:
				cliente.set_correo(Correo(email, ''))

			print(cliente.__str__())
			print('contacto1: {}'.format(cliente.get_telefono_primario()))
			self.model.guardar_cliente(cliente)
			self.view.view_show_message(True, 'Se ha guardado con exito')
			self.view.widget_destroy(frame)

	def crear_paquete(self, value):
		self.view.view_crear_paquete(value)

	def editar_paquete(self, frame, paquete, pos_paquete):
		self.view.view_editar_paquete(frame, paquete, pos_paquete)

	def guardar_paquete_background(self, paquete, pos_paquete, es_la_pre_venta_actual):
		print('Controller: guardando en background...')
		self.model.guardar_paquete_editado(paquete, pos_paquete)

		if es_la_pre_venta_actual:
			self.view.update_buscar_paquete()

	def es_la_pre_venta_actual(self, pre_venta):
		return self.model.es_la_pre_venta_actual(pre_venta)

	def guardar_paquete(self, nombre, tipo, sub_tipo, esta_vigente, lista_fecha, precio, senha, incluye,
											cant_pasajeros, pre_ventas, frame_agregar_paquete, imagenes):

		try:
			self.model.validar_datos_paquete(nombre, tipo, sub_tipo, esta_vigente, lista_fecha, precio, senha, incluye, cant_pasajeros, True)
		except NombreException as e:
			self.view.view_show_message(False, e)
		except Exception as e:
			self.view.view_show_message(False, e)
		except ValueError as e:
			self.view.view_show_message(False, e)
		else:
			tengo_fecha = False
			for fecha in lista_fecha:
				tengo_fecha = True
				paquete = self.model.crear_paquete(nombre, tipo, sub_tipo, esta_vigente, fecha, precio, senha, incluye, cant_pasajeros)

				if len(pre_ventas) is not 0:
					paquete.set_pre_ventas(pre_ventas)

				if len(imagenes) is not 0:
					paquete.set_imagenes(imagenes)

				print('que onda pio 1...')
				self.model.guardar_paquete(paquete)

			if tengo_fecha is False:
				#en caso de que sea un paquete PERSONALIZADO y no se le haya introducido una fecha
				fecha = None
				paquete = self.model.crear_paquete(nombre, tipo, sub_tipo, esta_vigente, fecha, precio, senha, incluye, cant_pasajeros)
				if len(pre_ventas) is not 0:
					paquete.set_pre_ventas(pre_ventas)

				if len(imagenes) is not 0:
					paquete.set_imagenes(imagenes)

				self.model.guardar_paquete(paquete)

			self.view.view_show_message(True, 'Se ha guardado con exito')
			self.view.widget_destroy(frame_agregar_paquete)
			self.view.update_buscar_paquete()

	def guardar_paquete_editado(self, pos_paquete, nombre, tipo, sub_tipo, esta_vigente, fecha, precio,
								senha, incluye, cant_pasajeros, pre_ventas, parent_detalles, imagenes):
		success = None
		try:
			self.model.validar_datos_paquete_editado(nombre, tipo, sub_tipo, esta_vigente, fecha, precio, senha, incluye, cant_pasajeros, False)
			success = True
		except NombreException as e:
			success = False
			self.view.view_show_message(False, e)
		except Exception as e:
			success = False
			self.view.view_show_message(False, e)
		except ValueError as e:
			success = False
			self.view.view_show_message(False, e)
		else:
			self.view.view_show_message(True, 'Se ha guardado con exito')
			paquete = self.model.crear_paquete(nombre, tipo, sub_tipo, esta_vigente, fecha, precio, senha, incluye, cant_pasajeros)

			if len(pre_ventas) is not 0:
				paquete.set_pre_ventas(pre_ventas)

			if len(imagenes) is not 0:
					paquete.set_imagenes(imagenes)

			print('guardando paquete editado...')
			self.model.guardar_paquete_editado(paquete, pos_paquete)
			self.view.view_paquete_detalles(parent_detalles, paquete, pos_paquete)
			self.view.update_buscar_paquete()

	def agregar_pre_venta(self, flujo):
		self.view.view_agregar_pre_venta(flujo)

	def editar_pre_venta(self, pre_venta, posicion_pre_venta):
		self.view.view_editar_pre_venta(pre_venta, posicion_pre_venta)

	def guardar_pre_venta(self, precio, senha, monto_cuota, cant_cuotas, fecha_inicio, fecha_fin, frame_pre_venta, posicion_pre_venta, agregando):
		success = None
		try:
			self.model.validar_datos_pre_venta(precio, senha, monto_cuota, cant_cuotas, fecha_inicio, fecha_fin)
			success = True
		except Exception as e:
			success = False
			self.view.view_show_message(False, e)
		except ValueError as e:
			success = False
			self.view.view_show_message(False, e)
		else:
			pre_venta = self.model.crear_pre_venta(precio, senha, monto_cuota, cant_cuotas, fecha_inicio, fecha_fin)

			#print('Controller: posicion_pre_venta: ' + str(posicion_pre_venta))
			self.view.set_value_pre_venta(pre_venta, posicion_pre_venta, agregando)
			
			self.view.view_show_message(True, 'Pre venta añadida con exito')
			self.view.widget_destroy(frame_pre_venta)
			#volvemos a mostras las pre ventas
			self.view.show_pre_ventas()

	def registrar_cliente(self):
		self.view.view_registrar_cliente()

	'''
	def welcome(self):
		self.view.welcome()


	def menu(self):
		self.view.menu()
	
	def buscarPorCedula(self):
		cedula = self.view.leerCedula()
		respuesta = self.model.buscarPorCedula(cedula)
		self.view.imprimirEnPantalla(respuesta)
	
	def agregar_usuario(self):
		usuario = self.view.vista_agregar_usuario()
		self.model.guardar_usuario(usuario)
		
	def listar_usuarios(self):
		lista_usuarios = self.model.listar_usuarios()
		self.view.vista_listar_usuarios(lista_usuarios)
		return lista_usuarios

	def liquidar(self):
		factura = self.view.vista_liquidar_in()
		self.model.liquidar(factura)
		factura = self.view.vista_liquidar_out()

	def senhar(self):
		factura = self.view.vista_senhar_in()
		self.model.senhar(factura)
		factura = self.view.vista_senhar_out()
	'''
