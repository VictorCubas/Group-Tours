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
				print('1')
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

	#def agregar_pre_venta_editar(pre_venta):
	#	self.view.view_agregar_pre_venta_editar(pre_venta)

	def guardar_paquete(self, nombre, tipo, sub_tipo, esta_vigente, lista_fecha, precio, senha, incluye, cant_pasajeros, pre_ventas):
		#print('{}, {}, {}, {}, {}, {}, {}, {}'.format(nombre, tipo, sub_tipo, fecha, esta_vigente, precio, senha, incluye))
		if len(lista_fecha) > 0:
			try:
				self.model.validar_datos_paquete(nombre, tipo, sub_tipo, esta_vigente, lista_fecha[0], precio, senha, incluye, cant_pasajeros)
			except NombreException as e:
				self.view.view_show_message(False, e)
			except Exception as e:
				self.view.view_show_message(False, e)
			except ValueError as e:
				self.view.view_show_message(False, e)
			else:
				for fecha in lista_fecha:
					paquete = self.model.crear_paquete(nombre, tipo, sub_tipo, esta_vigente, fecha, precio, senha, incluye, cant_pasajeros)

					if len(pre_ventas) is not 0:
						paquete.set_pre_ventas(pre_ventas)

					self.model.guardar_paquete(paquete)

				self.view.view_show_message(True, 'Se ha guardado con exito')
				self.view.view_crear_paquete(True)
		else:
			self.view.view_show_message(False, 'Debe introducir una fecha')

	def listar_pre_venta(self):
		self.view.view_listar_pre_venta()

	def agregar_editar_pre_venta(self):
		#self.view.view_agregar_pre_venta()
		self.view.view_agregar_editar_pre_venta()

	def editar_pre_venta(self, pre_venta, posicion_pre_venta):
		self.view.view_editar_pre_venta(pre_venta, posicion_pre_venta)

	def guardar_pre_venta(self, precio, senha, monto_cuota, cant_cuotas, fecha_inicio, fecha_fin, frame_pre_venta, posicion_pre_venta):
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

			self.view.set_value_pre_venta(pre_venta, posicion_pre_venta)
			#SOLO CUANDO SE AGREGA LA PRIMERA PRE VENTA SE DEBERIA DE HACER ESTO
			self.view.set_value_content_button_pre_venta()
			self.view.view_show_message(True, 'Pre venta añadida con exito')
			self.view.widget_destroy(frame_pre_venta)

			if posicion_pre_venta is not None:
				#cuando se este editando/agregando una preventa de un paquete
				self.view.view_listar_pre_venta_frame()
			else:
				print('asi es, estoy aqui 1')
				#self.view.view_listar_pre_venta_frame()
				#para agregar a una lista de pre ventas vacia desde editar paquete
				self.view.show_pre_ventas(True)
				#para agregar a una lista de pre ventas vacia desde crear paquete
				#self.view.show_pre_ventas(False)
	
	def editar_paquete(self, frame, paquete, pos_paquete, pos_result_busqueda):
		self.view.view_editar_paquete(frame, paquete, pos_paquete, pos_result_busqueda)

	def guardar_paquete_editado(self, pos_paquete, pos_result_busqueda, nombre, tipo, sub_tipo, esta_vigente, fecha, precio,
																senha, incluye, cant_pasajeros, pre_ventas, parent_detalles):
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

			if len(pre_ventas) is not 0:
				paquete.set_pre_ventas(pre_ventas)

			print('guardando paquete editado...')
			self.model.guardar_paquete_editado(paquete, pos_paquete)

			self.view.widget_destroy(parent_detalles)
			print('destruyendo paquete detalles (anterior)')
			self.view.view_paquete_detalles(paquete, pos_paquete, pos_result_busqueda)
			print('reconstruyendo el nuevo paquete detalles')

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
