#controller.py
from Model import Model
from View import View
from tkinter import ttk
from tkinter import *
from exceptions.NombreException import NombreException

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
		
	def generate_image_status_file(self, last_image_number):
		self.model.generate_image_status_file(last_image_number)
	
	def get_last_image_number(self):
		return self.model.get_last_image_number()

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

		#return result_encontrando[0]
		#print('len: ' + str(len(result_encontrando[0])))
		#for i in range(len(result_encontrando[0])):
		#	print(result_encontrando[0][i].get_nombre())

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

	def generar_lista_anhos(self):
		return self.model.generar_lista_anhos()

	def crear_paquete(self, value):
		self.view.view_crear_paquete(value)

	def cancelar_editar_paquete(self):
		self.view.cancelar_editar_paquete()
		
	#def agregar_pre_venta_editar(pre_venta):
	#	self.view.view_agregar_pre_venta_editar(pre_venta)

	def guardar_paquete(self, nombre, tipo, sub_tipo, esta_vigente, lista_fecha, precio,
											senha, incluye, cant_pasajeros, pre_venta, image_path):
		#print('{}, {}, {}, {}, {}, {}, {}, {}'.format(nombre, tipo, sub_tipo, fecha, esta_vigente, precio, senha, incluye))
		if len(lista_fecha) > 0:
			try:
				self.model.validar_datos_paquete(nombre, tipo, sub_tipo, esta_vigente, lista_fecha[0],
																		precio, senha, incluye, cant_pasajeros)
			except NombreException as e:
				self.view.view_show_message(False, e)
			except Exception as e:
				self.view.view_show_message(False, e)
			except ValueError as e:
				self.view.view_show_message(False, e)
			else:
				for fecha in lista_fecha:
					print('guardanding....')
					paquete = self.model.crear_paquete(nombre, tipo, sub_tipo,
							esta_vigente, fecha, precio, senha, incluye, cant_pasajeros, image_path)

					if pre_venta is not None:
						paquete.agregar_pre_venta(pre_venta)

					self.model.guardar_paquete(paquete)

				self.view.view_show_message(True, 'Se ha guardado con exito')
				self.view.view_crear_paquete(True)
		else:
			self.view.view_show_message(False, 'Debe introducir una fecha')

			
	def agregar_editar_pre_venta(self):
		#self.view.view_agregar_pre_venta()
		self.view.view_agregar_editar_pre_venta()

	def guardar_pre_venta(self, precio, senha, monto_cuota, cant_cuotas, fecha_inicio, fecha_fin):
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
			#print('{} {} {} {} {} {}'.format(pre_venta.precio, pre_venta.senha, pre_venta.monto_cuota, pre_venta.cantidad_cuotas, pre_venta.fecha_inicio, fecha_fin))
			#self.model.guardar_pre_venta(pre_venta)
			self.view.set_value_pre_venta(pre_venta)
			self.view.view_show_message(True, 'Pre venta añdido con exito')

	
	def editar_paquete(self, frame, paquete, pos_paquete, pos_result_busqueda):
		self.view.view_editar_paquete(frame, paquete, pos_paquete, pos_result_busqueda)

	def guardar_paquete_editado(self, pos_paquete, pos_result_busqueda, nombre, tipo, sub_tipo, esta_vigente, fecha, precio, senha, incluye, cant_pasajeros, pre_venta, parent_detalles):
		#print('{}, {}, {}, {}, {}, {}, {}, {}'.format(nombre, tipo, sub_tipo, fecha, esta_vigente, precio, senha, incluye))
		success = None
		try:
			self.model.validar_datos_paquete(nombre, tipo, sub_tipo, esta_vigente, fecha, precio, senha, incluye, cant_pasajeros)
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

			if pre_venta is not None:
				paquete.agregar_pre_venta(pre_venta)

			#print('paquete a guardar: ' + paquete.get_nombre())
			#print('pos_paquete: ' + str(pos_paquete))
			#print('listando paquetes1...')
			#paq = self.model.listar_paquetes()
			#for p in paq:
			#	print('paquete: ' + p.get_nombre())

			print('guardando paquete editado..........')
			self.model.guardar_paquete_editado(paquete, pos_paquete)

			#print('listando paquetes2...')
			#paq = self.model.listar_paquetes()
			#for p in paq:
			#	print('paquete: ' + p.get_nombre())
			self.view.view_paquete_detalles(paquete, pos_paquete, pos_result_busqueda)
			self.view.widget_destroy(parent_detalles)

			#actualizamos el vector resultado de la busqueda
			#mostramos el vector resultado de la busqueda despues de la edicion
			#self.view.show_result_busqueda_paquete()
			self.view.update_buscar_paquete()

	def registrar_cliente(self, next_back_starting):
		self.view.view_registrar_cliente(next_back_starting)

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
