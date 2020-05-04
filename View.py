#view.py
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfilename
#import tkFont
from Usuario import Usuario
from Calendar import Calendar
from TemporizadorVigencia import TemporizadorVigencia
import PIL
from PIL import Image
from PIL import ImageTk
import datetime

import copy

class View:
	'''
	Implementando la vista de la app
	'''
	CANTIDAD_CARACTERES = 23

	def __init__(self, controller, parent):
		self.controller = controller
		#self.parent = Tk()
		self.parent = parent
		self.parent.title('Group Tours')
		self.parent.geometry('1300x800+300+80')
		self.parent.resizable(width=False, height=False)
		#self.parent.iconbitmap('imagenes/inicio.png')
		self.parent.iconphoto(False, PhotoImage(file='imagenes/group_tours.png'))
		#self.parent.winfo_name('Group Tours')

		self.main_frame = Frame(self.parent, width='1300', height='800', bg='#F9F9F9')
		self.main_frame.pack_propagate(0)
		self.left_frame = Frame(self.main_frame, width='365', height='400', bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		self.right_frame = None

		self.anterior = 'inicio'
		self.buttons = {'inicio': Button(self.left_frame, text=' Inicio', font=('tahoma', 17), bg='#F9F9F9', width='300', height='90'),
						'paquetes': Button(self.left_frame, text=' Paquetes', font=('tahoma', 17), bg='#F9F9F9', width='300', height='90'),
						'usuarios': Button(self.left_frame, text=' Clientes', font=('tahoma', 17), bg='#F9F9F9', width='300', height='90'),
						'facturas': Button(self.left_frame, text=' Facturas', font=('tahoma', 17), bg='#F9F9F9', width='300', height='90')}

		self.imagenes = {'inicio_icon': PhotoImage(file="imagenes/inicio.png"),
						'paquete_icon': PhotoImage(file='imagenes/paquete.png'),
						'usuario_icon': PhotoImage(file='imagenes/usuario.png'),
						'factura_icon': PhotoImage(file='imagenes/factura.png'),
						'lupa_icon': PhotoImage(file='imagenes/lupa.png'),
						'next_available_icon': PhotoImage(file='imagenes/next1.png'),
						'next_not_available_icon': PhotoImage(file='imagenes/next2.png'),
						'back_available_icon': PhotoImage(file='imagenes/back1.png'),
						'back_not_available_icon': PhotoImage(file='imagenes/back2.png'),
						'save_icon': PhotoImage(file='imagenes/save_icon.png'),
						'cancel_icon': PhotoImage(file='imagenes/cancel_icon.png'),
						'ok_icon': PhotoImage(file='imagenes/ok_icon.png'),
						'not_ok_icon': PhotoImage(file='imagenes/not_ok_icon.png'),
						'edit_icon': PhotoImage(file='imagenes/edit_icon.png'),
						'add_icon': PhotoImage(file='imagenes/add_icon.png'),
						'camara_icon': PhotoImage(file='imagenes/camara_icon.png')}

		#self.inicio_button = Button(self.left_frame, text=' Inicio', font=('tahoma', 17), bg='#F9F9F9', width='300', height='90')
		#self.inicio_button.config(font=('arial', 19, "bold"))
		#self.inicio_button.config(justify=RIGHT)
		self.buttons['inicio'].config(image=self.imagenes['inicio_icon'], compound=LEFT)
		self.buttons['inicio'].config(anchor=W)  #posicionamos el texto a la izquierda
		self.buttons['inicio'].config(command=lambda:self.view_inicio())
		self.buttons['inicio'].pack()

		self.buttons['paquetes'].config(image=self.imagenes['paquete_icon'], compound=LEFT)
		self.buttons['paquetes'].config(anchor=W)
		self.buttons['paquetes'].config(command=lambda:self.view_paquetes())
		self.buttons['paquetes'].pack()

		self.buttons['usuarios'].config(image=self.imagenes['usuario_icon'], compound=LEFT)
		self.buttons['usuarios'].config(anchor=W)
		self.buttons['usuarios'].config(command=lambda:self.view_usuarios())
		self.buttons['usuarios'].pack()	

		self.buttons['facturas'].config(image=self.imagenes['factura_icon'], compound=LEFT)
		self.buttons['facturas'].config(anchor=W)
		self.buttons['facturas'].config(command=lambda:self.view_facturas())
		self.buttons['facturas'].pack()

		self.left_frame.pack(side='left', padx=20, pady=80, anchor=NW)
		self.main_frame.pack()
		
		self.view_inicio()

		#ejecutamos una serie de hilos para la actualizacion de los paquetes
		self.controller.ejecutar_temporizador()
		#detectamos el cierre de la aplicacion.
		self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
		#self.show_parent()

	def on_closing(self):
		#le damos quit a la ejecucion
		self.controller.stop_hilos()
		self.parent.destroy()

	def view_inicio(self):
		self.set_button_bold('inicio')
		self.anterior = 'inicio'

		frame = Frame(self.main_frame, width='900', height='700', bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		frame.pack(padx=20, pady=50, anchor=NE)

		label_welcome = Label(frame, text='Bienvenido', font=('tahoma', 55, 'bold'), width=9, height=3, relief=GROOVE, borderwidth=0)
		label_welcome.config(bg='#F9F9F9')

		#********************************************************
		#	CREAMOS UNA ETIQUETA Y LE COLOCAMOS UN ICONO		*
		#********************************************************
		label_logo = Label(frame, width=336, height=336, relief=GROOVE, borderwidth=0)
		label_logo.config(bg='#F9F9F9')
		logo = PhotoImage(file='imagenes/logo.png')
		label_logo.config(image=logo)
		label_logo.photo = logo

		#********************************************************
		#				CREAMOS TODOS LOS BOTONES				*
		#********************************************************
		frame_bottom = Frame(frame, width='850', height='180', bg='#66CDFC', relief=GROOVE, borderwidth=0)
		button_buscar_paquete = Button(frame_bottom, text='Buscar Paquete', font=('tahoma', 11),
									bg='#66CDFC', width='100', height='100', highlightthickness=0, borderwidth=0)
		button_buscar_paquete.config(activebackground='#48C2FA')
		button_buscar_usuario = Button(frame_bottom, text='Buscar Usuario', font=('tahoma', 11),
									bg='#66CDFC', width='100', height='100', highlightthickness=0, borderwidth=0)
		button_buscar_usuario.config(activebackground='#48C2FA')

		#********************************************************
		#			AGREGAMOS ICONOS A LOS BOTONES				*
		#********************************************************
		button_buscar_paquete.config(image=self.imagenes['lupa_icon'], compound=TOP)
		button_buscar_usuario.config(image=self.imagenes['lupa_icon'], compound=TOP)

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************
		button_buscar_paquete.config(command=lambda:self.view_buscar_paquete())
		button_buscar_usuario.config(command=lambda:self.view_usuarios())

		#********************************************************
		#				PACK A TODOS LOS BOTONES				*
		#********************************************************

		label_welcome.pack(side='left',padx=20, pady=50, anchor=NW)
		label_logo.pack(padx=20, pady=50, anchor=NE)
		button_buscar_paquete.pack(side='left',padx=150)
		button_buscar_usuario.pack(side='right', padx=150)
		button_buscar_usuario.pack_propagate(0)
		frame_bottom.place(relx=0.5, rely=0.9, anchor=S)
		frame_bottom.pack_propagate(0)

		self.switch_frame(frame)

	def view_paquetes(self):
		self.set_button_bold('paquetes')
		self.anterior = 'paquetes'

		self.view_buscar_paquete()

	def view_buscar_paquete(self):
		self.set_button_bold('paquetes')
		self.anterior = 'paquetes'

		#DEFINIMOS EL FRAME 
		frame = Frame(self.main_frame, width='900', height='700', bg='#F9F9F9', relief=GROOVE, borderwidth=0)

		#declaramos el un string que alamacena el contenido ingresado
		self.content_entry = StringVar()
		self.radio_variable = StringVar()
		self.radio_variable.set('ninguno')
		self.filtro_anho_value = None
		self.filtro_tipo_value = None
		self.filtro_sub_tipo_value = None
		#result es una lista que almacena todos los paquetes como resultado de la busqueda
		#RESETEAMOS LA LISTA DE RESULTADOS EN CASO DE ENTRAR POR PRIMERA VEZ A BUSCAR PAQUETE
		self.paquetes = []

		#********************************************************

		label_nombre_paquete = Label(frame, text='Nombre/Destino:', font=('tahoma', 14, 'bold'), width=14, height=1, bg='#F9F9F9')
		label_nombre_paquete.config(fg='#48C2FA')
		#declaramos una entreada para ingresar los datos
		entry = Entry(frame, width='15', font=('tahoma', 15), textvariable=self.content_entry)
		#insertamos RADIO BUTTON para la busqueda por vigencia
		label_radio_button = Label(frame, text='Vigente', font=('tahoma', 14, 'bold'), width=7, height=3, relief=GROOVE, borderwidth=0)
		label_radio_button.config(bg='#F9F9F9', fg='#48C2FA')

		radio_button_si = Radiobutton(frame, text='Si', font=('tahoma', 15), variable=self.radio_variable, value='si', width=2, height=2)
		radio_button_si.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)
		radio_button_no = Radiobutton(frame, text='No', font=('tahoma', 15), variable=self.radio_variable, value='no', width=2, height=2)
		radio_button_no.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)
		radio_button_ninguno = Radiobutton(frame, text='Ninguno', font=('tahoma', 15), variable=self.radio_variable, value='ninguno', width=8, height=2)
		radio_button_ninguno.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)

		#insertamos un COMBOBOX para la busqueda por anho
		label_anho = Label(frame, text='Año', font=('tahoma', 14, 'bold'), width=4, height=2, relief=GROOVE, borderwidth=0)
		label_anho.config(bg='#F9F9F9', fg='#48C2FA', highlightthickness=0)

		lista_anhos = self.controller.generar_lista_anhos()
		self.combobox_anhos = ttk.Combobox(frame, values=lista_anhos)
		#seteamos el valor inicial de la busqueda por anho en caso de que se haya sellecionado algun valor
		#y que se haya se haya sellecionado los botones de next o back
		if self.filtro_anho_value != None:
			self.combobox_anhos.set(self.filtro_anho_value)

		self.combobox_anhos.config(state='readonly', font=(15), width='7', height='6', background='#F9F9F9')

		#insertamos un MENUBUTTON para la busqueda por tipo
		label_tipo_paquete = Label(frame, text='Tipo', font=('tahoma', 14, 'bold'), width='4', height='2', relief=GROOVE, borderwidth=0)
		label_tipo_paquete.config(bg='#F9F9F9', fg='#48C2FA')

		#insertamos un COMBOBOX para la busqueda por tipo
		lista_tipos = ['', 'Terrestre', 'Aereo']
		self.combobox_tipos = ttk.Combobox(frame, values=lista_tipos)
		if self.filtro_tipo_value != None:
			self.combobox_tipos.set(self.filtro_tipo_value)

		self.combobox_tipos.config(state='readonly', font=(15), width='9', height='6', background='#F9F9F9')

		#insertamos un COMBOBOX para la busqueda por sub-tipo
		lista_sub_tipos = ['', 'Estandar', 'Personalizado']
		self.combobox_sub_tipos = ttk.Combobox(frame, values=lista_sub_tipos)
		if self.filtro_sub_tipo_value != None:
			self.combobox_sub_tipos.set(self.filtro_sub_tipo_value)

		self.combobox_sub_tipos.config(state='readonly', font=(15), width='11', height='6', background='#F9F9F9')

		#agregar paquete view
		agregar_paquete_button = Button(frame, text='Agregar un paquete', width='210', height='27', relief=GROOVE, borderwidth=0)
		agregar_paquete_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#27A221', activeforeground='#27A221', highlightthickness=0, anchor=W)

		agregar_paquete_button.config(image=self.imagenes['add_icon'], compound=LEFT)

		#mostramos los RESULTADOS DE LA BUSQUEDA
		#creamos un frame, un canvas y un scrollbar para luego conectarlos
		frame_result = Frame(frame, width='800', height='450', bg='#FFFFFF', relief=GROOVE, borderwidth=1)
		self.canvas=Canvas(frame_result,bg='#FFFFFF',width=800,height=450)
		vbar=Scrollbar(frame_result,orient=VERTICAL)
		vbar.pack(side=RIGHT,fill=Y)
		vbar.config(command=self.canvas.yview)
		self.canvas.config(yscrollcommand=vbar.set)
		self.canvas.pack()
		frame_result.pack(side='bottom', pady=20)
		frame_result.pack_propagate(0)

		#los botones estan dentro de un frame auxiliar
		self.frame_result_aux = Frame(self.canvas, bg='#FFFFFF', borderwidth=0, relief=GROOVE)
		self.canvas.create_window(0, 0, window=self.frame_result_aux, anchor=NW)
		self.frame_result_aux.bind("<Configure>", self.on_frame_configure)

		#almacenamos los resultados en forma de botones (views)
		self.view_result_busqueda_paquete = []

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************
		#detectamos los cambios cada vez que se escribe algo
		self.content_entry.trace("w", self.buscar_paquete_por_nombre)
		radio_button_si.config(command=lambda:self.buscar_paquete_por_vigencia(self.radio_variable.get()))
		radio_button_no.config(command=lambda:self.buscar_paquete_por_vigencia(self.radio_variable.get()))
		radio_button_ninguno.config(command=lambda:self.buscar_paquete_por_vigencia(self.radio_variable.get()))
		self.combobox_anhos.bind("<<ComboboxSelected>>", self.buscar_paquete_por_anho)
		self.combobox_tipos.bind("<<ComboboxSelected>>", self.buscar_paquete_por_tipo)
		self.combobox_sub_tipos.bind("<<ComboboxSelected>>", self.buscar_paquete_por_sub_tipo)
		agregando = True
		agregar_paquete_button.config(command=lambda: self.view_agregar_and_detalles_toplevel(None, None, None, agregando))

		#********************************************************
		#				PACK A TODOS LOS BOTONES				*
		#********************************************************
		#label_nombre_paquete.pack(side='left', padx=25, pady=42, anchor=NW)
		label_nombre_paquete.place(relx=0.028, rely=0.06)
		#entry.pack(pady=40, anchor=NW)
		entry.place(relx=0.237, rely=0.0525)
		label_radio_button.place(relx=0.5, rely=0.027)
		radio_button_si.place(relx=0.6, rely=0.042)
		radio_button_no.place(relx=0.68, rely=0.042)
		radio_button_ninguno.place(relx=0.76, rely=0.042)
		label_anho.place(relx=0.025, rely=0.135)
		self.combobox_anhos.place(relx=0.1, rely=0.152)
		label_tipo_paquete.place(relx=0.25, rely=0.135)
		self.combobox_tipos.place(relx=0.33, rely=0.152)
		self.combobox_sub_tipos.place(relx=0.46, rely=0.152)
		agregar_paquete_button.place(relx=0.03, rely=0.23)
		frame.pack(padx=20, pady=20, anchor=NE)
		frame.pack_propagate(0)

		self.show_paquetes()

		self.switch_frame(frame)

	def set_values_paquetes_posiciones(self, result_busqueda_paquete):
		self.paquetes = result_busqueda_paquete[0]
		self.paquetes_posiciones = result_busqueda_paquete[1]

	def buscar_paquete_por_nombre(self, *args):
		result_busqueda_paquete = self.controller.buscar_paquete(content1=self.content_entry.get(), content2=self.radio_variable.get(),
									content3=self.combobox_anhos.get(), content4=self.combobox_tipos.get(), content5=self.combobox_sub_tipos.get())
		self.set_values_paquetes_posiciones(result_busqueda_paquete)
		self.show_paquetes()

	def buscar_paquete_por_vigencia(self, radio_variable):
		result_busqueda_paquete = self.controller.buscar_paquete(content1=self.content_entry.get(), content2=radio_variable,
									content3=self.combobox_anhos.get(), content4=self.combobox_tipos.get(), content5=self.combobox_sub_tipos.get())
		self.set_values_paquetes_posiciones(result_busqueda_paquete)
		self.show_paquetes()

	def buscar_paquete_por_anho(self, *args):
		self.filtro_anho_value = self.combobox_anhos.get()
		result_busqueda_paquete = self.controller.buscar_paquete(content1=self.content_entry.get(), content2=self.radio_variable.get(),
									content3=self.combobox_anhos.get(), content4=self.combobox_tipos.get(), content5=self.combobox_sub_tipos.get())
		self.set_values_paquetes_posiciones(result_busqueda_paquete)
		self.show_paquetes()

	def buscar_paquete_por_tipo(self, *args):
		self.filtro_tipo_value = self.combobox_tipos.get()
		result_busqueda_paquete = self.controller.buscar_paquete(content1=self.content_entry.get(), content2=self.radio_variable.get(),
									content3=self.combobox_anhos.get(), content4=self.combobox_tipos.get(), content5=self.combobox_sub_tipos.get())
		self.set_values_paquetes_posiciones(result_busqueda_paquete)
		self.show_paquetes()

	def buscar_paquete_por_sub_tipo(self, *args):
		self.filtro_sub_tipo_value = self.combobox_sub_tipos.get()
		result_busqueda_paquete = self.controller.buscar_paquete(content1=self.content_entry.get(), content2=self.radio_variable.get(),
									content3=self.combobox_anhos.get(), content4=self.combobox_tipos.get(), content5=self.combobox_sub_tipos.get())
		self.set_values_paquetes_posiciones(result_busqueda_paquete)
		self.show_paquetes()

	def update_buscar_paquete(self):
		self.filtro_anho_value = self.combobox_anhos.get()
		self.filtro_tipo_value = self.combobox_tipos.get()
		self.filtro_sub_tipo_value = self.combobox_sub_tipos.get()
		result_busqueda_paquete = self.controller.buscar_paquete(content1=self.content_entry.get(), content2=self.radio_variable.get(),
									content3=self.combobox_anhos.get(), content4=self.combobox_tipos.get(), content5=self.combobox_sub_tipos.get())

		self.set_values_paquetes_posiciones(result_busqueda_paquete)
		self.show_paquetes()

	def on_frame_configure(self, event=None):
	    self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def on_frame_pre_venta_configure(self, event=None):
	    self.canvas_pre_ventas.configure(scrollregion=self.canvas_pre_ventas.bbox("all"))

	def show_paquetes(self):
		paquete_view = None

		#eliminamos los resultados anteriores a la busqueda actual (si elminamos la lista anterior tambien se elimina la lista actual, por ref)
		for paquete_view in self.view_result_busqueda_paquete:
			paquete_view.destroy()

		self.view_result_busqueda_paquete = []

		#aplicamos los nuevos resultados de la busqueda
		paquete_view = None
		aux = -1

		for paquete in self.paquetes:
			aux += 1

			paquete_view = Frame(self.frame_result_aux, bg='#F9F9F9', width='770', height='150', relief=GROOVE, borderwidth=0)
			paquete_view.pack(padx=10, pady=5)

			#imagen view
			image_frame = Frame(paquete_view, bg='#F9F9F9', width='120', height='140', relief=GROOVE, borderwidth=0)
			image_frame.place(relx=0.02, rely=0.02)

			imagen_original = None
			if paquete.get_cantidad_de_imagenes() == 0:
				imagen_original = Image.open('imagenes/group_tours.png')
			else:
				imagen_original = paquete.get_imagenes()[0]

			imagen_original = imagen_original.resize((170, 140), Image.ANTIALIAS)

			logo = ImageTk.PhotoImage(imagen_original)
			label_logo = Label(image_frame, width=230, height=140, relief=GROOVE, borderwidth=0)
			label_logo.config(bg='#F9F9F9')
			label_logo.config(image=logo)
			label_logo.photo = logo
			label_logo.pack()
			label_logo.pack_propagate(0)

			paquete_name_view = Label(paquete_view, text=paquete.get_nombre(), width='18', height='1', relief=GROOVE, borderwidth=0)
			paquete_name_view.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535',
											activeforeground='#343535', anchor=W) #posicionamos el texto a la izquierda
			paquete_name_view.place(relx=0.38, rely=0.05)

			#fecha view
			date = paquete.get_fecha_de_viaje()
			texto = self.convert_date_to_string(date)

			paquete_fecha_de_viaje_view = Label(paquete_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
			paquete_fecha_de_viaje_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030',
									activeforeground='#2F3030', highlightthickness=0, anchor=W)
			paquete_fecha_de_viaje_view.place(relx=0.38, rely=0.29)

			#vigente view
			texto = 'Vigente'
			if paquete.get_esta_vigente() == False:
				texto = 'No vigente'

			paquete_fecha_de_viaje_view = Label(paquete_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
			paquete_fecha_de_viaje_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030',
											activeforeground='#2F3030', highlightthickness=0, anchor=W)
			paquete_fecha_de_viaje_view.place(relx=0.38, rely=0.52)

			texto = 'Tipo: ' + paquete.TRASLADO
			paquete_fecha_de_viaje_view = Label(paquete_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
			paquete_fecha_de_viaje_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030',
												activeforeground='#2F3030', highlightthickness=0, anchor=W)
			paquete_fecha_de_viaje_view.place(relx=0.38, rely=0.75)

			#SEGUNDA CULUMNA
			#precio view
			texto = ''

			if paquete.si_pre_venta():
				texto = self.convert_amount_to_string(paquete.get_precio_pre_venta(), True)
			else:
				texto = self.convert_amount_to_string(paquete.get_precio(), True)

			paquete_precio_view = Label(paquete_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
			paquete_precio_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
			paquete_precio_view.place(relx=0.72, rely=0.07)

			#pre venta view
			if paquete.si_pre_venta():
				texto = 'Pre venta: si'
			else:
				texto = 'Pre venta: no'

			paquete_pre_venta_view = Label(paquete_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
			paquete_pre_venta_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
			paquete_pre_venta_view.place(relx=0.72, rely=0.29)

			#lugares disponibles view
			texto = 'Lugares disponible: '
			lugares_disponibles = paquete.get_lugares_disponibles()
			color = '#2F3030'
			if lugares_disponibles > 0:
				texto = texto + str(lugares_disponibles)
			elif lugares_disponibles == 0:
				texto = 'SOLD OUT'
				color = '#E60700'
			else:
				texto = texto + '--'

			paquete_pre_venta_view = Label(paquete_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
			paquete_pre_venta_view.config(font=('tahoma', 13), bg='#F9F9F9', fg=color, activeforeground=color, highlightthickness=0, anchor=W)
			paquete_pre_venta_view.place(relx=0.72, rely=0.52)

			pos_paquete = self.paquetes_posiciones[aux]

			#detalles view
			texto = 'Ver detalles      >'
			paquete_detalles_view = Button(paquete_view, text=texto, width='16', height='1', relief=GROOVE, borderwidth=0)
			paquete_detalles_view.config(font=('tahoma', 13), bg='#27A221', fg='#FFFFFF', activeforeground='#FFFFFF',
										activebackground='#20801B', highlightthickness=0, anchor=W)
			paquete_detalles_view.place(relx=0.72, rely=0.75)
			paquete_detalles_view.config(command=lambda paquete=paquete, pos_paquete=pos_paquete:
									self.view_agregar_and_detalles_toplevel(None, paquete, pos_paquete, False))
			#print(paquete_name_view.config("text")[-1])
			#print(paquete_detalles_view.config("text")[-1])

			self.view_result_busqueda_paquete.append(paquete_view)

	def view_agregar_and_detalles_toplevel(self, frame, paquete, pos_paquete, agregando):
		print('preparando: Crear paquete/Viendo detalles')
		self.paquete_detalles_top_level = Toplevel(self.parent, bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		self.paquete_detalles_top_level.geometry('1000x800+450+100')
		self.paquete_detalles_top_level.resizable(width=False, height=False)

		if agregando:
			self.view_agregar_paquete()
		else:
			self.view_paquete_detalles(frame, paquete, pos_paquete)

	def view_paquete_detalles(self, frame_detalles, paquete, pos_paquete):
		print('viendo detalles')
		self.paquete_detalles_top_level.title('Paquete Detalles')

		if frame_detalles is not None:
			self.widget_destroy(frame_detalles)

		frame_detalles = Frame(self.paquete_detalles_top_level, width='1000', height='900', bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		frame_detalles.pack()
		frame_detalles.pack_propagate(0)
		paquete_name_label = Label(frame_detalles, text=paquete.get_nombre(), width='20', height='2', relief=GROOVE, borderwidth=0)
		paquete_name_label.config(font=('tahoma', 25, 'bold'), bg='#F9F9F9', fg='#48C2FA') #posicionamos el texto a la izquierda
		paquete_name_label.pack()

		#fecha view
		fecha_label = Label(frame_detalles, text='Fecha:', width='6', height='1', relief=GROOVE, borderwidth=0)
		fecha_label.config(font=('tahoma', 14, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		fecha_label.place(relx=0.02, rely=0.11)

		texto = self.convert_date_to_string(paquete.get_fecha_de_viaje())

		fecha_value_label = Label(frame_detalles, text=texto, width='10', height='1', relief=GROOVE, borderwidth=0)
		fecha_value_label.config(font=('tahoma', 14), bg='#F9F9F9', fg='#2F3030', anchor=W)
		fecha_value_label.place(relx=0.105, rely=0.11)

		#vigente view
		vigente_label = Label(frame_detalles, text='Vigente:', width='7', height='1', relief=GROOVE, borderwidth=0)
		vigente_label.config(font=('tahoma', 14, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		vigente_label.place(relx=0.02, rely=0.155)
		texto = 'Si'
		if paquete.get_esta_vigente() == False:
			texto = 'No'

		vigente_value_label = Label(frame_detalles, text=texto, width='2', height='1', relief=GROOVE, borderwidth=0)
		vigente_value_label.config(font=('tahoma', 14), bg='#F9F9F9', fg='#2F3030', anchor=W)
		vigente_value_label.place(relx=0.116, rely=0.155)

		#tipo view
		tipo_label = Label(frame_detalles, text='Tipo:', width='4', height='1', relief=GROOVE, borderwidth=0)
		tipo_label.config(font=('tahoma', 14, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		tipo_label.place(relx=0.02, rely=0.20)

		texto = paquete.TRASLADO
		tipo_value_label = Label(frame_detalles, text=texto, width='8', height='1', relief=GROOVE, borderwidth=0)
		tipo_value_label.config(font=('tahoma', 14), bg='#F9F9F9', fg='#2F3030', anchor=W)
		tipo_value_label.place(relx=0.078, rely=0.20)

		#incluye view
		incluye_label = Label(frame_detalles, text='Incluye:', width='7', height='1', relief=GROOVE, borderwidth=0)
		incluye_label.config(font=('tahoma', 14, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		incluye_label.place(relx=0.02, rely=0.245)

		frame = Frame(frame_detalles, width='400', height='200', bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		frame.place(relx=0.02, rely=0.29)

		scroll = Scrollbar(frame, orient=VERTICAL)
		scroll.pack(side=RIGHT, fill=Y)

		texto = paquete.get_incluye_descripcion()
		incluye_text_widget = Text(frame, height=7, width=35, relief=GROOVE, borderwidth=0)
		incluye_text_widget.insert(END, texto)
		
		incluye_text_widget.config(state='disabled', font=('tahoma', 12), bg='#F9F9F9', fg='#2F3030')
		incluye_text_widget.pack(side=LEFT, fill=Y)

		scroll.config(command=incluye_text_widget.yview)
		incluye_text_widget.config(wrap=WORD, yscrollcommand=scroll.set)

		#SEGUNDA COLUMNA
		#precio view
		#agregamos los puntos al precio, ej: 3000000 ---> 3.000.000Gs
		precio_label = Label(frame_detalles, text='Precio:', width='6', height='1', relief=GROOVE, borderwidth=0)
		precio_label.config(font=('tahoma', 14, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		precio_label.place(relx=0.35, rely=0.11)

		if paquete.si_pre_venta():
			texto = self.convert_amount_to_string(paquete.get_precio_pre_venta(), True)
		else:
			texto = self.convert_amount_to_string(paquete.get_precio(), True)

		self.precio_value_paquete_det = StringVar()
		self.precio_value_paquete_det.set(texto)
		precio_value_label = Label(frame_detalles, textvariable=self.precio_value_paquete_det, width='12', height='1', relief=GROOVE, borderwidth=0)
		precio_value_label.config(font=('tahoma', 14), bg='#F9F9F9', fg='#2F3030', anchor=W)
		precio_value_label.place(relx=0.435, rely=0.11)

		#senha view
		#agregamos los puntos al precio, ej: 3000000 ---> 3.000.000Gs
		senha_label = Label(frame_detalles, text='Seña:', width='6', height='1', relief=GROOVE, borderwidth=0)
		senha_label.config(font=('tahoma', 14, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		senha_label.place(relx=0.35, rely=0.155)

		if paquete.si_pre_venta():
			texto = self.convert_amount_to_string(paquete.get_senha_pre_venta(), True)
		else:
			texto = self.convert_amount_to_string(paquete.get_senha(), True)


		self.senha_value_paquete_det = StringVar()
		self.senha_value_paquete_det.set(texto)
		senha_value_label = Label(frame_detalles, textvariable=self.senha_value_paquete_det, width='12', height='1', relief=GROOVE, borderwidth=0)
		senha_value_label.config(font=('tahoma', 14), bg='#F9F9F9', fg='#2F3030', anchor=W)
		senha_value_label.place(relx=0.435, rely=0.155)

		#pre venta view
		pre_venta_label = Label(frame_detalles, text='Pre venta:', width='9', height='1', relief=GROOVE, borderwidth=0)
		pre_venta_label.config(font=('tahoma', 14, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		pre_venta_label.place(relx=0.35, rely=0.20)

		texto = 'Si'
		if paquete.si_pre_venta() == False:
			texto = 'No'

		pre_venta_label = Label(frame_detalles, text=texto, width='2', height='1', relief=GROOVE, borderwidth=0)
		pre_venta_label.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', anchor=W)
		pre_venta_label.place(relx=0.474, rely=0.20)

		texto = 'Ver precio en detalles      >'
		precio_detalles_button = Button(frame_detalles, text=texto, width='19', height='1', relief=GROOVE, borderwidth=2)
		precio_detalles_button.config(font=('tahoma', 13), bg='#27A221', fg='#FFFFFF', activeforeground='#FFFFFF',
										activebackground='#20801B', highlightthickness=0, anchor=W)

		if paquete.si_pre_venta():
			precio_detalles_button.config(bg='#27A221', activebackground='#20801B')
			self.paquete = paquete
			self.pos_paquete = pos_paquete
			self.estoy_en_precio_detalles = True
			precio_detalles_button.config(command=lambda:self.view_precio_detalles(paquete.get_precio(), paquete.get_senha(), paquete.get_pre_ventas()))
		else:
			precio_detalles_button.config(bg='#A6A0A0', activebackground='#A6A0A0')

		precio_detalles_button.place(relx=0.35, rely=0.24)

		#TERCERA COLUMNA
		#cantidad de pasajeros view
		cantidad_usuarios_label = Label(frame_detalles, text='Cantidad de pasajeros:', width='19', height='1', relief=GROOVE, borderwidth=0)
		cantidad_usuarios_label.config(font=('tahoma', 14, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		cantidad_usuarios_label.place(relx=0.65, rely=0.11)

		texto = paquete.get_cantidad_de_usuarios_actual()
		cantidad_usuarios_value_label = Label(frame_detalles, text=texto, width='2', height='1', relief=GROOVE, borderwidth=0)
		cantidad_usuarios_value_label.config(font=('tahoma', 14), bg='#F9F9F9', fg='#2F3030', anchor=W)
		cantidad_usuarios_value_label.place(relx=0.903, rely=0.11)

		#lugares disponibles view
		lugares_disponibles_label = Label(frame_detalles, text='Lugares disponibles:', width='17', height='1', relief=GROOVE, borderwidth=0)
		lugares_disponibles_label.config(font=('tahoma', 14, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		lugares_disponibles_label.place(relx=0.65, rely=0.155)

		lugares_disponibles = paquete.get_lugares_disponibles()
		color = '#2F3030'
		if lugares_disponibles > 0:
			texto = str(lugares_disponibles)
		elif lugares_disponibles == 0:
			texto = 'SOLD OUT'
			color = '#E60700'
		else:
			texto = '--'

		lugares_disponibles_value_label = Label(frame_detalles, text=texto, width='9', height='1', relief=GROOVE, borderwidth=0)
		lugares_disponibles_value_label.config(font=('tahoma', 14), bg='#F9F9F9', fg=color, anchor=W)
		lugares_disponibles_value_label.place(relx=0.877, rely=0.155)

		#maxima cantidad de pasajeros
		max_cantidad_pasajeros_label = Label(frame_detalles, text='Total pasajeros:', width='15', height='1', relief=GROOVE, borderwidth=0)
		max_cantidad_pasajeros_label.config(font=('tahoma', 14, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		max_cantidad_pasajeros_label.place(relx=0.65, rely=0.20)

		texto = paquete.get_cantidad_de_usuarios_total()
		if texto == -1:
			texto = '--'

		max_cantidad_value_pasajeros_label = Label(frame_detalles, text=texto, width='2', height='1', relief=GROOVE, borderwidth=0)
		max_cantidad_value_pasajeros_label.config(font=('tahoma', 14), bg='#F9F9F9', fg='#2F3030', anchor=W)
		max_cantidad_value_pasajeros_label.place(relx=0.852, rely=0.20)

		#Habitaciones view
		habitaciones_label = Label(frame_detalles, text='Habitaciones:', width='11', height='1', relief=GROOVE, borderwidth=0)
		habitaciones_label.config(font=('tahoma', 14, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		habitaciones_label.place(relx=0.65, rely=0.245)

		#texto = paquete.get_cantidad_de_usuarios_actual()
		habitaciones_value_label = Label(frame_detalles, text='En proceso...', width='11', height='1', relief=GROOVE, borderwidth=0)
		habitaciones_value_label.config(font=('tahoma', 14), bg='#F9F9F9', fg='#2F3030', anchor=W)
		habitaciones_value_label.place(relx=0.8, rely=0.245)

		#view editar and salir
		salir_button = Button(frame_detalles, text='Salir', width=110, height=30, relief=GROOVE, borderwidth=0)
		salir_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		salir_button.config(image=self.imagenes['not_ok_icon'], compound=LEFT)
		salir_button.place(relx=0.34, rely=0.85)

		editar_button = Button(frame_detalles, text='Editar', width=110, height=30, relief=GROOVE, borderwidth=0)
		editar_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		editar_button.config(image=self.imagenes['edit_icon'], compound=LEFT)
		editar_button.place(relx=0.5, rely=0.85)

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************
		salir_button.config(command=lambda:self.widget_destroy(self.paquete_detalles_top_level))
		editar_button.config(command=lambda:self.controller.editar_paquete(frame_detalles, paquete, pos_paquete))
		#editar_button.config(command=lambda:self.widget_destroy(frame_detalles))

	def view_precio_detalles(self, precio, senha, pre_ventas):
		print('viendo precio en detalles....')
		precio_parent = Toplevel(self.parent, bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		precio_parent.title('Precio Detalles')
		#frame.tittle('Pre Venta')
		precio_parent.geometry('650x500+650+150')
		precio_parent.resizable(width=False, height=False)

		#anhadimos un separador
		separator_top = ttk.Separator(precio_parent, orient=HORIZONTAL)
		separator_top.pack(side=TOP, fill=X, padx=30, pady=15)

		#view detalles precio con pre venta
		label = Label(precio_parent, text='Precio de venta', width='18', height='1', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 10), bg='#F9F9F9') #posicionamos el texto a la izquierda
		label.place(relx=0.38, rely=0.01)

		#view precio
		label = Label(precio_parent, text='Precio:', width='7', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.05)

		texto = self.convert_amount_to_string(precio, True)

		label = Label(precio_parent, text=texto, width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13), bg='#F9F9F9', anchor=W)
		label.place(relx=0.16, rely=0.05)

		#view senha
		label = Label(precio_parent, text='Seña:', width='7', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.15)

		texto = self.convert_amount_to_string(senha, True)

		label = Label(precio_parent, text=texto, width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13), bg='#F9F9F9', anchor=W)
		label.place(relx=0.16, rely=0.15)

		#anhadimos un separador
		separator = ttk.Separator(precio_parent, orient=HORIZONTAL)
		separator.pack(side=TOP, fill=X, padx=30, pady=100)

		#view detalles precio con pre venta
		label = Label(precio_parent, text='Precio de pre venta', width='18', height='1', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 10), bg='#F9F9F9') #posicionamos el texto a la izquierda
		label.place(relx=0.38, rely=0.245)

		#view precio
		self.pre_ventas = pre_ventas
		self.pre_venta = None

		width='480'
		height='250'
		relx=0.125
		rely=0.3

		self.view_result_pre_ventas = []
		self.building_frame_where_to_show_lista_pre_venta(precio_parent, width, height, relx, rely)
		#almacenamos los resultados en forma de botones de las pre ventas(views)
		self.show_pre_ventas()

		#view ok
		ok_button = Button(precio_parent, text='OK', width=110, height=30, relief=GROOVE, borderwidth=0)
		ok_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		ok_button.config(image=self.imagenes['ok_icon'], compound=LEFT)
		ok_button.place(relx=0.39, rely=0.85)
		ok_button.config(command=lambda:self.widget_destroy(precio_parent))

	def view_agregar_paquete(self):
		print('View: creando paquete...')
		#self.set_button_bold('paquetes')
		#self.anterior = 'paquetes'

		#DEFINIMOS EL FRAME
		self.frame_pre_venta = None
		self.paquete_detalles_top_level.title('Agregar paquete')
		self.frame_agregar_paquete = Frame(self.paquete_detalles_top_level, width='1000', height='900', bg='#F9F9F9', relief=GROOVE, borderwidth=0)

		#********************************************************
		#  AGREGAMOS LAS ETIQUETAS CORRESPONDIENTE A LOS DATOS	*
		#********************************************************

		#view nombre paquete
		label = Label(self.frame_agregar_paquete, text='Nombre:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.06)

		name_content_entry = StringVar()
		name_entry = Entry(self.frame_agregar_paquete, width='25', font=('tahoma', 13), textvariable=name_content_entry)
		name_entry.place(relx=0.17, rely=0.075)

		#view tipo de paquete
		label = Label(self.frame_agregar_paquete, text='Tipo:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.132)

		lista_tipos = ['Terrestre', 'Aereo']
		combobox_tipos = ttk.Combobox(self.frame_agregar_paquete, values=lista_tipos)
		combobox_tipos.config(state='readonly', font=(13), width='9', height='6', background='#F9F9F9')
		combobox_tipos.place(relx=0.17, rely=0.149)

		lista_sub_tipos = ['Estandar', 'Personalizado']
		combobox_sub_tipos = ttk.Combobox(self.frame_agregar_paquete, values=lista_sub_tipos)
		combobox_sub_tipos.config(state='readonly', font=(13), width='12', height='6', background='#F9F9F9')
		combobox_sub_tipos.place(relx=0.3, rely=0.149)

		#view vigente
		label = Label(self.frame_agregar_paquete, text='Vigente:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.204)

		lista_vigencia = ['Si', 'No']
		combobox_vigencia = ttk.Combobox(self.frame_agregar_paquete, values=lista_vigencia)
		combobox_vigencia.config(state='readonly', font=(13), width='9', height='6', background='#F9F9F9')
		combobox_vigencia.place(relx=0.17, rely=0.221)

		#view fecha
		label = Label(self.frame_agregar_paquete, text='Salida/as:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.276)

		self.lista_fecha = []
		self.lista_fecha_combobox = []
		self.combobox_add_fecha = ttk.Combobox(self.frame_agregar_paquete, values=self.lista_fecha_combobox)
		self.combobox_add_fecha.config(state='readonly', font=(13), width='9', height='6', background='#F9F9F9')
		self.combobox_add_fecha.set('-- / -- / --')
		self.combobox_add_fecha.place(relx=0.17, rely=0.292)

		button_fecha_de_viaje = Button(self.frame_agregar_paquete, width='25', height='25', relief=GROOVE, borderwidth=0)
		button_fecha_de_viaje.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
		button_fecha_de_viaje.config(image=self.imagenes['add_icon'])
		button_fecha_de_viaje.place(relx=0.3, rely=0.289)

		#view precio
		label = Label(self.frame_agregar_paquete, text='Precio:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.347)

		self.price_content_entry = StringVar()
		self.price_value = None
		self.price_entry = Entry(self.frame_agregar_paquete, width='25', font=('tahoma', 13), textvariable=self.price_content_entry)
		self.price_entry.place(relx=0.17, rely=0.36)

		#view senha
		label = Label(self.frame_agregar_paquete, text='Seña:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.42)

		self.senha_content_entry = StringVar()
		self.senha_value = None
		self.senha_entry = Entry(self.frame_agregar_paquete, width='25', font=('tahoma', 13), textvariable=self.senha_content_entry)
		self.senha_entry.place(relx=0.17, rely=0.43)

		#view pre venta
		self.pre_ventas = []
		self.si_pre_venta = False
		#para almacenar las pre_ventas mostrados al usuario
		self.view_result_pre_ventas = []
		label = Label(self.frame_agregar_paquete, text='Pre venta:', width='13', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		label.place(relx=0.02, rely=0.492)

		self.content_pre_venta_button = StringVar()
		self.content_pre_venta_button.set('Agregar')
		pre_venta_button = Button(self.frame_agregar_paquete, textvariable=self.content_pre_venta_button, width=10, height=1, relief=GROOVE, borderwidth=0)
		pre_venta_button.config(font=('tahoma', 13), bg='#F9F9F9')
		pre_venta_button.place(relx=0.17, rely=0.496)

		width='480'
		height='250'
		relx=0.02
		rely=0.544

		self.view_result_pre_ventas = []
		self.building_frame_where_to_show_lista_pre_venta(self.frame_agregar_paquete, width, height, relx, rely)

		#view cantidad de pasajeros
		label = Label(self.frame_agregar_paquete, text='Cant pasajeros:', width='13', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		label.place(relx=0.56, rely=0.06)

		cant_pasajeros_content_entry = StringVar()
		cant_pasajeros_entry = Entry(self.frame_agregar_paquete, width='15', font=('tahoma', 13), textvariable=cant_pasajeros_content_entry)
		cant_pasajeros_entry.place(relx=0.742, rely=0.075)

		#incluye view
		label = Label(self.frame_agregar_paquete, text='Incluye:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		label.place(relx=0.56, rely=0.132)

		incluye_frame = Frame(self.frame_agregar_paquete, width='400', height='200', bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		incluye_frame.place(relx=0.561, rely=0.203)

		scroll = Scrollbar(incluye_frame, orient=VERTICAL)
		scroll.pack(side=RIGHT, fill=Y)

		incluye_content = StringVar()
		incluye_text_widget = Text(incluye_frame, height=7, width=30, relief=GROOVE, borderwidth=0)
		incluye_text_widget.insert(END, '')
		
		incluye_text_widget.config(font=('tahoma', 12), bg='#FFFFFF', fg='#2F3030')
		incluye_text_widget.pack(side=LEFT, fill=Y)

		scroll.config(command=incluye_text_widget.yview)
		incluye_text_widget.config(wrap=WORD, yscrollcommand=scroll.set)

		#agregar imagen view
		imagenes = []
		frame_imagen = Frame(self.frame_agregar_paquete, width='280', height='250', bg='#F9F9F9', relief=GROOVE, borderwidth=1)
		frame_imagen.place(relx=0.6, rely=0.45)
		frame_imagen.pack_propagate(0)

		imagen_predeterminada = Image.open('imagenes/group_tours.png')
		imagen_predeterminada = imagen_predeterminada.resize((270, 260), Image.ANTIALIAS)

		logo = ImageTk.PhotoImage(imagen_predeterminada)
		label_logo = Label(frame_imagen, width=270, height=260, relief=GROOVE, borderwidth=0)
		label_logo.config(bg='#F9F9F9')
		label_logo.config(image=logo)
		label_logo.photo = logo
		label_logo.pack()
		label_logo.pack_propagate(0)

		add_image_button = Button(self.frame_agregar_paquete, text='Agregar', width=110, height=30, relief=GROOVE, borderwidth=0)
		add_image_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535', highlightthickness=0)
		add_image_button.config(image=self.imagenes['camara_icon'], compound=LEFT)

		add_image_button.config(command=lambda:self.controller.agregar_imagen(self.frame_agregar_paquete, frame_imagen, label_logo, imagenes))
		add_image_button.place(relx=0.675, rely=0.8)


		#view ok and cancel	
		save_button = Button(self.frame_agregar_paquete, text='Guardar', width=110, height=30, relief=GROOVE, borderwidth=0)
		save_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		save_button.config(image=self.imagenes['save_icon'], compound=LEFT)
		save_button.place(relx=0.5, rely=0.90)

		cancel_button = Button(self.frame_agregar_paquete, text='Cancelar', width=110, height=30, relief=GROOVE, borderwidth=0)
		cancel_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		cancel_button.config(image=self.imagenes['not_ok_icon'], compound=LEFT)
		cancel_button.place(relx=0.34, rely=0.90)

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************
		self.price_content_entry.trace("w", self.update_price_content_entry)
		self.senha_content_entry.trace("w", self.update_senha_content_entry)
		button_fecha_de_viaje.config(command=lambda:self.view_calendar(self.frame_agregar_paquete, None, 0, 0.17, 0.277))
		agregando = True

		pre_venta_button.config(command=lambda:self.controller.agregar_pre_venta(agregando))
		save_button.config(command=lambda:self.controller.guardar_paquete(name_content_entry.get(), combobox_tipos.get(), combobox_sub_tipos.get(),
				combobox_vigencia.get(), self.lista_fecha, self.price_value, self.senha_value, incluye_text_widget.get(1.0, END),
				cant_pasajeros_content_entry.get(), self.pre_ventas, self.paquete_detalles_top_level, imagenes))

		cancel_button.config(command=lambda:self.widget_destroy(self.paquete_detalles_top_level))

		#********************************************************
		#				PACK A TODOS LOS BOTONES				*
		#********************************************************
		self.frame_agregar_paquete.pack(padx=20, pady=20, anchor=NE)
		self.frame_agregar_paquete.pack_propagate(0)

	def view_agregar_imagen(self, frame_parent, frame_imagen, label_logo, imagenes):
		filepath = askopenfilename(parent=frame_parent, filetypes=[('Imagen','*.png'), ('Imagen','*.jpg'), ('Imagen','*.jpeg')])

		#ESTO DEBERIA DE ESTA EN EL MODEL Y EN UN TRY-CATCH
		if filepath:
			self.widget_destroy(label_logo)

			imagen_original = Image.open(filepath)
			imagen_original = imagen_original.resize((270, 260), Image.ANTIALIAS)
			logo = ImageTk.PhotoImage(imagen_original)
			label_logo = Label(frame_imagen, width=270, height=260, relief=GROOVE, borderwidth=0)
			label_logo.config(bg='#F9F9F9')
			label_logo.config(image=logo)
			label_logo.photo = logo
			label_logo.pack()
			label_logo.pack_propagate(0)

			imagenes.append(imagen_original)

	def view_editar_paquete(self, frame_editar_paquete, paquete, pos_paquete):
		print('editando paquete...')
		self.paquete_detalles_top_level.title('Editar paquete')
		#DEFINIMOS EL FRAME 
		self.widget_destroy(frame_editar_paquete)

		self.frame_pre_venta = None
		frame_detalles = Frame(self.paquete_detalles_top_level, width='1000', height='900', bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		#frame_detalles.place(relx=0, rely=0)
		frame_detalles.pack()
		frame_detalles.pack_propagate(0)

		#********************************************************
		#  AGREGAMOS LAS ETIQUETAS CORRESPONDIENTE A LOS DATOS	*
		#********************************************************

		#view nombre paquete
		label = Label(frame_detalles, text='Nombre:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 15, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.065)

		name_content_entry = StringVar()
		name_content_entry.set(paquete.get_nombre())
		name_entry = Entry(frame_detalles, width='25', font=('tahoma', 13), textvariable=name_content_entry)
		name_entry.place(relx=0.17, rely=0.078)

		#view tipo de paquete
		label = Label(frame_detalles, text='Tipo:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 15, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.125)

		lista_tipos = ['Terrestre', 'Aereo']
		combobox_tipos = ttk.Combobox(frame_detalles, values=lista_tipos)
		combobox_tipos.config(state='readonly', font=(13), width='9', height='6', background='#F9F9F9')
		combobox_tipos.set(paquete.TRASLADO)
		combobox_tipos.place(relx=0.17, rely=0.142)

		lista_sub_tipos = ['Estandar', 'Personalizado']
		combobox_sub_tipos = ttk.Combobox(frame_detalles, values=lista_sub_tipos)
		combobox_sub_tipos.config(state='readonly', font=(13), width='12', height='6', background='#F9F9F9')
		combobox_sub_tipos.set(paquete.TIPO)
		combobox_sub_tipos.place(relx=0.3, rely=0.142)

		#view vigente
		label = Label(frame_detalles, text='Vigente:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 15, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.185)

		lista_vigencia = ['Si', 'No']
		combobox_vigencia = ttk.Combobox(frame_detalles, values=lista_vigencia)
		combobox_vigencia.config(state='readonly', font=(13), width='9', height='6', background='#F9F9F9')
		esta_vigente = paquete.get_esta_vigente()
		if esta_vigente:
			esta_vigente = 'Si'
		else:
			esta_vigente = 'No'
		combobox_vigencia.set(esta_vigente)
		combobox_vigencia.place(relx=0.17, rely=0.2)

		#view fecha
		label = Label(frame_detalles, text='Fecha:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 15, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.245)

		content_button_fecha = StringVar()
		date = paquete.get_fecha_de_viaje()

		self.fecha_de_viaje = date
		date_texto = self.convert_date_to_string(date)
		content_button_fecha.set(date_texto)
		button_fecha_de_viaje = Button(frame_detalles, textvariable=content_button_fecha, width='8', height='1', relief=GROOVE, borderwidth=0)
		button_fecha_de_viaje.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
		button_fecha_de_viaje.place(relx=0.17, rely=0.258)

		#view precio
		label = Label(frame_detalles, text='Precio:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 15, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.305)

		self.price_value = paquete.get_precio()
		self.price_content_entry = StringVar()

		texto = self.convert_amount_to_string(paquete.get_precio(), False)
		self.price_content_entry.set(texto)

		self.price_entry = Entry(frame_detalles, width='20', font=('tahoma', 13), textvariable=self.price_content_entry)
		self.price_entry.place(relx=0.17, rely=0.318)

		self.simbol_label = StringVar()
		self.simbol_label.set('')
		label = Label(frame_detalles, textvariable=self.simbol_label, width='2', height='1', relief=GROOVE, borderwidth=2)
		label.config(font=('tahoma', 15, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.4, rely=0.317)

		#view senha
		label = Label(frame_detalles, text='Seña:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 15, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.365)

		self.senha_value = paquete.get_senha()
		self.senha_content_entry = StringVar()

		#print('senha value: {}'.format(self.senha_value))
		#print('senha value content: {}'.format())

		texto = self.convert_amount_to_string(paquete.get_senha(), False)
		self.senha_content_entry.set(texto)

		self.senha_entry = Entry(frame_detalles, width='20', font=('tahoma', 13), textvariable=self.senha_content_entry)
		self.senha_entry.place(relx=0.17, rely=0.378)

		#view pre venta
		self.pre_ventas = paquete.get_pre_ventas()
		label = Label(frame_detalles, text='Pre venta:', width='13', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 15, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		#label.place(relx=0.56, rely=0.125)
		label.place(relx=0.02, rely=0.425)

		self.content_pre_venta_button = StringVar()
		self.si_pre_venta = paquete.si_pre_venta()
		self.content_pre_venta_button.set('Agregar')

		pre_venta_button = Button(frame_detalles, textvariable=self.content_pre_venta_button, width=10, height=1, relief=GROOVE, borderwidth=0)
		pre_venta_button.config(font=('tahoma', 13), bg='#F9F9F9')
		pre_venta_button.place(relx=0.17, rely=0.432)

		width='480'
		height='270'
		relx=0.02
		rely=0.485

		self.view_result_pre_ventas = []
		self.building_frame_where_to_show_lista_pre_venta(frame_detalles, width, height, relx, rely)
		self.show_pre_ventas()

		#incluye view
		label = Label(frame_detalles, text='Incluye:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 15, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		label.place(relx=0.56, rely=0.125)

		incluye_frame = Frame(frame_detalles, width='400', height='200', bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		incluye_frame.place(relx=0.56, rely=0.185)

		scroll = Scrollbar(incluye_frame, orient=VERTICAL)
		scroll.pack(side=RIGHT, fill=Y)

		incluye_content = StringVar()
		incluye_text_widget = Text(incluye_frame, height=7, width=30, relief=GROOVE, borderwidth=0)
		incluye_text_widget.insert(END, paquete.get_incluye_descripcion())
		
		incluye_text_widget.config(font=('tahoma', 12), bg='#FFFFFF', fg='#2F3030')
		incluye_text_widget.pack(side=LEFT, fill=Y)

		scroll.config(command=incluye_text_widget.yview)
		incluye_text_widget.config(wrap=WORD, yscrollcommand=scroll.set)

		#view cantidad de pasajeros
		label = Label(frame_detalles, text='Total pasajeros:', width='13', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 15, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		label.place(relx=0.56, rely=0.065)

		cant_pasajeros_content_entry = StringVar()
		texto = paquete.get_cantidad_de_usuarios_total()
		if texto == -1:
			texto = '--'
		cant_pasajeros_content_entry.set(texto)
		cant_pasajeros_entry = Entry(frame_detalles, width='15', font=('tahoma', 13), textvariable=cant_pasajeros_content_entry)
		cant_pasajeros_entry.place(relx=0.748, rely=0.078)


		#agregar imagen view
		imagenes = paquete.get_imagenes()
		frame_imagen = Frame(frame_detalles, width='280', height='250', bg='#F9F9F9', relief=GROOVE, borderwidth=1)
		frame_imagen.place(relx=0.6, rely=0.45)
		frame_imagen.pack_propagate(0)

		imagen_original = None
		if paquete.get_cantidad_de_imagenes() == 0:
			imagen_original = Image.open('imagenes/group_tours.png')
		else:
			imagen_original = paquete.get_imagenes()[0]

		imagen_original = imagen_original.resize((270, 260), Image.ANTIALIAS)

		logo = ImageTk.PhotoImage(imagen_original)
		label_logo = Label(frame_imagen, width=270, height=260, relief=GROOVE, borderwidth=0)
		label_logo.config(bg='#F9F9F9')
		label_logo.config(image=logo)
		label_logo.photo = logo
		label_logo.pack()
		label_logo.pack_propagate(0)

		add_image_button = Button(frame_detalles, text='Agregar', width=110, height=30, relief=GROOVE, borderwidth=0)
		add_image_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535', highlightthickness=0)
		add_image_button.config(image=self.imagenes['camara_icon'], compound=LEFT)
		self.ya_se_agrego_una_imagen = True
		add_image_button.config(command=lambda:self.controller.agregar_imagen(frame_detalles, frame_imagen, label_logo, imagenes))
		add_image_button.place(relx=0.675, rely=0.775)

		#view ok and cancel
		save_button = Button(frame_detalles, text='Guardar', width=110, height=30, relief=GROOVE, borderwidth=0)
		save_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		save_button.config(image=self.imagenes['save_icon'], compound=LEFT)
		save_button.place(relx=0.5, rely=0.85)

		cancel_button = Button(frame_detalles, text='Salir', width=110, height=30, relief=GROOVE, borderwidth=0)
		cancel_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		cancel_button.config(image=self.imagenes['not_ok_icon'], compound=LEFT)
		cancel_button.place(relx=0.34, rely=0.85)
		#********************************************************

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************

		#button_anterior.config(command=lambda:self.pop_pila_anterior(View.VIEW_CREAR_PAQUETE))
		#button_siguiente.config(command=lambda:self.pop_pila_siguiente())
		self.price_content_entry.trace("w", self.update_price_content_entry)
		self.senha_content_entry.trace("w", self.update_senha_content_entry)
		button_fecha_de_viaje.config(command=lambda:self.view_calendar(frame_detalles, content_button_fecha, 1, 0.17, 0.258))

		agregando_pre_venta = True
		pre_venta_button.config(command=lambda:self.controller.agregar_pre_venta(agregando_pre_venta))

		save_button.config(command=lambda:self.controller.guardar_paquete_editado(pos_paquete, name_content_entry.get(),
				combobox_tipos.get(), combobox_sub_tipos.get(), combobox_vigencia.get(), self.fecha_de_viaje, self.price_value, self.senha_value,
				incluye_text_widget.get(1.0, END), cant_pasajeros_content_entry.get(), self.pre_ventas, frame_detalles, imagenes))

		cancel_button.config(command=lambda:self.view_paquete_detalles(frame_detalles, paquete, pos_paquete))
		
	def building_frame_where_to_show_lista_pre_venta(self, frame_container, width, height, relx, rely):
		#crearmos una seccion para mostrar la lista de pre ventas que se van creando
		#creamos un frame, un canvas y un scrollbar para luego conectarlos
		self.frame_pre_venta = Frame(frame_container, bg='#F9F9F9', width=width, height=height, relief=GROOVE, borderwidth=0)
		#self.frame_pre_venta.pack()
		self.frame_pre_venta.place(relx=relx, rely=rely)
		self.frame_pre_venta.pack_propagate(0)

		frame_result_pre_venta = Frame(self.frame_pre_venta, width=width, height=height, bg='#FFFFFF', relief=GROOVE, borderwidth=0)
		self.canvas_pre_ventas=Canvas(frame_result_pre_venta,bg='#FFFFFF',width=width,height=height)
		vbar=Scrollbar(frame_result_pre_venta, orient=VERTICAL)
		vbar.pack(side=RIGHT,fill=Y)
		vbar.config(command=self.canvas_pre_ventas.yview)
		self.canvas_pre_ventas.config(yscrollcommand=vbar.set)
		self.canvas_pre_ventas.pack()
		frame_result_pre_venta.pack(side='top', pady=20)
		#frame_result_pre_venta.place(relx=0.15, rely=0.1)

		#los botones estan dentro de un frame auxiliar
		self.frame_pre_ventas = Frame(self.canvas_pre_ventas, bg='#FFFFFF', borderwidth=0, relief=GROOVE)
		self.canvas_pre_ventas.create_window(0, 0, window=self.frame_pre_ventas, anchor=NW)
		self.frame_pre_ventas.bind("<Configure>", self.on_frame_pre_venta_configure)

	def view_editar_pre_venta(self, pre_venta, posicion_pre_venta):
		#if posicion_pre_venta is None
		#	self.view_result_pre_ventas = []
		#self.widget_destroy(self.frame_pre_venta)

		self.toplevel_pre_venta = Toplevel(self.parent, bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		self.toplevel_pre_venta.title('Pre Venta')
		#frame.tittle('Pre Venta')
		self.toplevel_pre_venta.geometry('600x400+650+150')
		self.toplevel_pre_venta.resizable(width=False, height=False)

		frame_pre_venta = Frame(self.toplevel_pre_venta, bg='#F9F9F9', width='600', height='400', relief=GROOVE, borderwidth=0)
		frame_pre_venta.pack()
		frame_pre_venta.pack_propagate(0)

		label = Label(frame_pre_venta, text='Precio:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.05)

		self.price_pre_venta_content_entry = StringVar()
		self.price_pre_venta_value = pre_venta.get_precio()
		texto = self.convert_amount_to_string(self.price_pre_venta_value, False)
		self.price_pre_venta_content_entry.set(texto)

		self.price_entry = Entry(frame_pre_venta, width='10', font=('tahoma', 13), textvariable=self.price_pre_venta_content_entry)
		self.price_entry.place(relx=0.25, rely=0.075)

		#view senha
		label = Label(frame_pre_venta, text='Seña:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.176)

		self.senha_pre_venta_content_entry = StringVar()
		self.senha_pre_venta_value = pre_venta.get_senha()
		texto = self.convert_amount_to_string(self.senha_pre_venta_value, False)
		self.senha_pre_venta_content_entry.set(texto)

		self.senha_entry = Entry(frame_pre_venta, width='10', font=('tahoma', 13), textvariable=self.senha_pre_venta_content_entry)
		self.senha_entry.place(relx=0.25, rely=0.2)

		#view monto cuota
		label = Label(frame_pre_venta, text='Monto cuota:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.301)

		self.monto_cuota_content_entry = StringVar()
		self.monto_cuota_value = pre_venta.get_monto_cuota()
		texto = self.convert_amount_to_string(self.monto_cuota_value, False)
		self.monto_cuota_content_entry.set(texto)

		self.monto_cuota_entry = Entry(frame_pre_venta, width='10', font=('tahoma', 13), textvariable=self.monto_cuota_content_entry)
		self.monto_cuota_entry.place(relx=0.25, rely=0.325)

		#view cantidad de cuotas
		label = Label(frame_pre_venta, text='Cant cuotas:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.425)

		cant_cuota_content_entry = StringVar()
		cant_cuota_content_entry.set(pre_venta.get_cantidad_cuotas())
		cant_cuota_entry = Entry(frame_pre_venta, width='10', font=('tahoma', 13), textvariable=cant_cuota_content_entry)
		cant_cuota_entry.place(relx=0.25, rely=0.448)

		#view fecha inicio
		label = Label(frame_pre_venta, text='Fecha inicio:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.5, rely=0.05)

		content_button_fecha_inicio = StringVar()
		date = pre_venta.get_fecha_inicio()
		texto = self.convert_date_to_string(date)
		content_button_fecha_inicio.set(texto)

		self.pre_venta_fecha_inicio = pre_venta.get_fecha_inicio()

		button_fecha_inicio = Button(frame_pre_venta, textvariable=content_button_fecha_inicio, width='8', height='1',
									relief=GROOVE, borderwidth=0)
		button_fecha_inicio.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
		button_fecha_inicio.place(relx=0.73, rely=0.07)

		#view fecha fin
		label = Label(frame_pre_venta, text='Fecha fin:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.5, rely=0.174)

		content_button_fecha_fin = StringVar()
		date = pre_venta.get_fecha_fin()
		texto = self.convert_date_to_string(date)
		content_button_fecha_fin.set(texto)

		self.pre_venta_fecha_fin = pre_venta.get_fecha_fin()
		button_fecha_fin = Button(frame_pre_venta, textvariable=content_button_fecha_fin, width='8', height='1', relief=GROOVE, borderwidth=0)
		button_fecha_fin.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
		button_fecha_fin.place(relx=0.73, rely=0.195)

		#view ok and cancel
		save_button = Button(frame_pre_venta, text='Guardar', width=110, height=30, relief=GROOVE, borderwidth=0)
		save_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		save_button.config(image=self.imagenes['save_icon'], compound=LEFT)
		save_button.place(relx=0.52, rely=0.75)

		cancel_button = Button(frame_pre_venta, text='Salir', width=110, height=30, relief=GROOVE, borderwidth=0)
		cancel_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		cancel_button.config(image=self.imagenes['not_ok_icon'], compound=LEFT)
		cancel_button.place(relx=0.28, rely=0.75)

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************s
		button_fecha_inicio.config(command=lambda:self.view_calendar(frame_pre_venta, content_button_fecha_inicio, 2, 0.55, 0.06))
		button_fecha_fin.config(command=lambda:self.view_calendar(frame_pre_venta, content_button_fecha_fin, 3, 0.55, 0.13))
		self.price_pre_venta_content_entry.trace("w", self.update_price_pre_venta_content_entry)
		self.senha_pre_venta_content_entry.trace("w", self.update_senha_pre_venta_content_entry)
		self.monto_cuota_content_entry.trace("w", self.update_monto_cuota_content_entry)
		agregando = False
		save_button.config(command=lambda:self.controller.guardar_pre_venta(self.price_pre_venta_value,
							self.senha_pre_venta_value, self.monto_cuota_value, cant_cuota_content_entry.get(),
							self.pre_venta_fecha_inicio, self.pre_venta_fecha_fin, self.toplevel_pre_venta, posicion_pre_venta, agregando))

		cancel_button.config(command=lambda:self.widget_destroy(self.toplevel_pre_venta))

	def view_agregar_pre_venta(self, flujo):
		print('Agregando pre venta...')
		self.toplevel_pre_venta = Toplevel(self.parent, bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		self.toplevel_pre_venta.title('Pre Venta')
		#frame.tittle('Pre Venta')
		self.toplevel_pre_venta.geometry('600x400+650+150')
		self.toplevel_pre_venta.resizable(width=False, height=False)

		frame_pre_venta = Frame(self.toplevel_pre_venta, bg='#F9F9F9', width='600', height='400', relief=GROOVE, borderwidth=0)
		frame_pre_venta.pack()
		frame_pre_venta.pack_propagate(0)

		#view precio
		label = Label(frame_pre_venta, text='Precio:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.05)
		#label.grid(row=0, column=1, padx=10, pady=20)

		self.price_pre_venta_content_entry = StringVar()
		self.price_pre_venta_content_entry.set('')
		self.price_pre_venta_value = None

		self.price_entry = Entry(frame_pre_venta, width='10', font=('tahoma', 13), textvariable=self.price_pre_venta_content_entry)
		self.price_entry.place(relx=0.25, rely=0.075)

		#view senha
		label = Label(frame_pre_venta, text='Seña:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.176)

		self.senha_pre_venta_content_entry = StringVar()
		self.senha_pre_venta_content_entry.set('')
		self.senha_pre_venta_value = None

		self.senha_entry = Entry(frame_pre_venta, width='10', font=('tahoma', 13), textvariable=self.senha_pre_venta_content_entry)
		self.senha_entry.place(relx=0.25, rely=0.2)

		#view monto cuota
		label = Label(frame_pre_venta, text='Monto cuota:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.301)

		self.monto_cuota_content_entry = StringVar()
		self.monto_cuota_content_entry.set('')
		self.monto_cuota_value = None

		self.monto_cuota_entry = Entry(frame_pre_venta, width='10', font=('tahoma', 13), textvariable=self.monto_cuota_content_entry)
		self.monto_cuota_entry.place(relx=0.25, rely=0.325)

		#view cantidad de cuotas
		label = Label(frame_pre_venta, text='Cant cuotas:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.425)

		cant_cuota_content_entry = StringVar()
		cant_cuota_content_entry.set('')

		cant_cuota_entry = Entry(frame_pre_venta, width='10', font=('tahoma', 13), textvariable=cant_cuota_content_entry)
		cant_cuota_entry.place(relx=0.25, rely=0.448)

		#view fecha inicio
		label = Label(frame_pre_venta, text='Fecha inicio:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.5, rely=0.05)

		content_button_fecha_inicio = StringVar()
		content_button_fecha_inicio.set('-- / -- / --')

		self.pre_venta_fecha_inicio = None

		button_fecha_inicio = Button(frame_pre_venta, textvariable=content_button_fecha_inicio, width='8', height='1',
									relief=GROOVE, borderwidth=0)
		button_fecha_inicio.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
		button_fecha_inicio.place(relx=0.73, rely=0.07)

		#view fecha fin
		label = Label(frame_pre_venta, text='Fecha fin:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.5, rely=0.174)

		content_button_fecha_fin = StringVar()
		content_button_fecha_fin.set('-- / -- / --')

		self.pre_venta_fecha_fin = None
		button_fecha_fin = Button(frame_pre_venta, textvariable=content_button_fecha_fin, width='8', height='1', relief=GROOVE, borderwidth=0)
		button_fecha_fin.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
		button_fecha_fin.place(relx=0.73, rely=0.195)

		#view ok and cancel
		save_button = Button(frame_pre_venta, text='Guardar', width=110, height=30, relief=GROOVE, borderwidth=0)
		save_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		save_button.config(image=self.imagenes['save_icon'], compound=LEFT)
		save_button.place(relx=0.52, rely=0.75)

		cancel_button = Button(frame_pre_venta, text='Salir', width=110, height=30, relief=GROOVE, borderwidth=0)
		cancel_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		cancel_button.config(image=self.imagenes['not_ok_icon'], compound=LEFT)
		cancel_button.place(relx=0.28, rely=0.75)

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************
		button_fecha_inicio.config(command=lambda:self.view_calendar(frame_pre_venta, content_button_fecha_inicio, 2, 0.55, 0.06))
		button_fecha_fin.config(command=lambda:self.view_calendar(frame_pre_venta, content_button_fecha_fin, 3, 0.55, 0.13))
		self.price_pre_venta_content_entry.trace("w", self.update_price_pre_venta_content_entry)
		self.senha_pre_venta_content_entry.trace("w", self.update_senha_pre_venta_content_entry)
		self.monto_cuota_content_entry.trace("w", self.update_monto_cuota_content_entry)

		save_button.config(command=lambda:self.controller.guardar_pre_venta(self.price_pre_venta_value,
					self.senha_pre_venta_value, self.monto_cuota_value, cant_cuota_content_entry.get(),
					self.pre_venta_fecha_inicio, self.pre_venta_fecha_fin, self.toplevel_pre_venta, None, flujo))

		cancel_button.config(command=lambda:self.widget_destroy(self.toplevel_pre_venta))

	def show_pre_ventas(self):
		#pre_venta_view = None

		#eliminamos los resultados anteriores a la busqueda actual (si elminamos la lista anterior tambien se elimina la lista actual, por ref)
		for pre_venta_view in self.view_result_pre_ventas:
			pre_venta_view.destroy()

		self.view_result_pre_ventas = []

		#aplicamos los nuevos resultados a la lista de pre ventas agregados
		pre_venta_frame = None

		frame_width = 445
		frame_height = 80

		if len(self.pre_ventas) != 0:
			posicion_pre_venta = -1
			for pre_venta in self.pre_ventas:
				posicion_pre_venta += 1

				pre_venta_frame = Frame(self.frame_pre_ventas, bg='#F9F9F9', width=frame_width, height=frame_height, relief=GROOVE, borderwidth=1)
				pre_venta_frame.pack(padx=10, pady=5)

				#pre venta label view
				label = Label(pre_venta_frame, text='Pre venta ' + str(posicion_pre_venta+1), width='10', height='1', relief=GROOVE, borderwidth=0)
				label.config(font=('tahoma', 10, 'bold'), bg='#F9F9F9', fg='#27A221', anchor=W) #posicionamos el texto a la izquierda
				label.place(relx=0.02, rely=0.05)

				#precio label view
				label = Label(pre_venta_frame, text='Precio:', width='6', height='1', relief=GROOVE, borderwidth=0)
				label.config(font=('tahoma', 10, 'bold'), bg='#F9F9F9', fg='#2F3030', anchor=W) #posicionamos el texto a la izquierda
				label.place(relx=0.02, rely=0.34)

				texto = self.convert_amount_to_string(pre_venta.get_precio(), True)

				label = Label(pre_venta_frame, text=texto, width='11', height='1', relief=GROOVE, borderwidth=0)
				label.config(font=('tahoma', 10), bg='#F9F9F9', fg='#2F3030', anchor=W) #posicionamos el texto a la izquierda
				label.place(relx=0.17, rely=0.34)
				
				#senha label view
				label = Label(pre_venta_frame, text='Seña:', width='6', height='1', relief=GROOVE, borderwidth=0)
				label.config(font=('tahoma', 10, 'bold'), bg='#F9F9F9', fg='#2F3030', anchor=W) #posicionamos el texto a la izquierda
				label.place(relx=0.02, rely=0.63)

				texto = self.convert_amount_to_string(pre_venta.get_senha(), True)

				label = Label(pre_venta_frame, text=texto, width='11', height='1', relief=GROOVE, borderwidth=0)
				label.config(font=('tahoma', 10), bg='#F9F9F9', fg='#2F3030', anchor=W) #posicionamos el texto a la izquierda
				label.place(relx=0.17, rely=0.63)
				
				#monto cuota label view
				label = Label(pre_venta_frame, text='Monto cuota:', width='11', height='1', relief=GROOVE, borderwidth=0)
				label.config(font=('tahoma', 10, 'bold'), bg='#F9F9F9', fg='#2F3030', anchor=W) #posicionamos el texto a la izquierda
				label.place(relx=0.44, rely=0.34)

				texto = self.convert_amount_to_string(pre_venta.get_monto_cuota(), True)

				label = Label(pre_venta_frame, text=texto, width='11', height='1', relief=GROOVE, borderwidth=0)
				label.config(font=('tahoma', 10), bg='#F9F9F9', fg='#2F3030', anchor=W) #posicionamos el texto a la izquierda
				label.place(relx=0.70, rely=0.34)

				#cantidad de cuotas label view
				label = Label(pre_venta_frame, text='Cant cuotas:', width='11', height='1', relief=GROOVE, borderwidth=0)
				label.config(font=('tahoma', 10, 'bold'), bg='#F9F9F9', fg='#2F3030', anchor=W) #posicionamos el texto a la izquierda
				label.place(relx=0.44, rely=0.63)

				texto = str(pre_venta.get_cantidad_cuotas())

				label = Label(pre_venta_frame, text=texto, width='11', height='1', relief=GROOVE, borderwidth=0)
				label.config(font=('tahoma', 10), bg='#F9F9F9', fg='#2F3030', anchor=W) #posicionamos el texto a la izquierda
				label.place(relx=0.70, rely=0.63)

				#fecha inicio label view
				texto = self.convert_date_to_string(pre_venta.get_fecha_inicio())

				label = Label(pre_venta_frame, text=texto, width='9', height='1', relief=GROOVE, borderwidth=0)
				label.config(font=('tahoma', 10, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
				label.place(relx=0.35, rely=0.05)

				#separador label view
				label = Label(pre_venta_frame, text='-', width='1', height='1', relief=GROOVE, borderwidth=0)
				label.config(font=('tahoma', 10, 'bold'), bg='#F9F9F9', fg='#2F3030', anchor=W) #posicionamos el texto a la izquierda
				label.place(relx=0.59, rely=0.05)

				#fecha fin label view
				texto = self.convert_date_to_string(pre_venta.get_fecha_fin())

				label = Label(pre_venta_frame, text=texto, width='9', height='1', relief=GROOVE, borderwidth=0)
				label.config(font=('tahoma', 10, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
				label.place(relx=0.65, rely=0.05)

				#view editar
				editar_button = Button(pre_venta_frame, width=30, height=30, relief=GROOVE, borderwidth=0)
				editar_button.config(bg='#F9F9F9', fg='#343535', highlightthickness=0)
				editar_button.config(image=self.imagenes['edit_icon'], compound=LEFT)
				editar_button.place(relx=0.9, rely=0.28)
				editar_button.config(command=lambda pre_venta=pre_venta, posicion_pre_venta=posicion_pre_venta:
													self.controller.editar_pre_venta(pre_venta, posicion_pre_venta))

				self.view_result_pre_ventas.append(pre_venta_frame)


	def convert_date_to_string(self, fecha):
		date_texto = ''

		if fecha != None:
			if fecha.day < 10:
				date_texto = '0'

			date_texto = date_texto + str(fecha.day) + '/'

			if fecha.month < 10:
				date_texto = date_texto + '0'

			date_texto = date_texto + str(fecha.month) + '/' + str(fecha.year)
		else:
			date_texto = '-- / -- / --'

		return date_texto

	def convert_amount_to_string(self, monto, add_simbol):
		#agregamos los puntos al precio, ej: 3000000 ---> 3.000.000Gs
		texto = ''
		monto_texto = str(monto)
		j = 1
		if len(monto_texto) > 3:
			for i in range(len(monto_texto) - 1, -1, -1):
				texto = monto_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = monto_texto

		if add_simbol:
			if monto < 100000: #significa que el precio esta en dolares, ya que en guaranies se considera 5 digitos como minimo
				texto = texto + '$'
			else:
				texto = texto + 'Gs.'

		return texto

	def update_price_pre_venta_content_entry(self, *args):
		texto = ''
		precio_texto = self.price_pre_venta_content_entry.get()

		cantidad_puntos_antes = 0
		#eliminamos los puntos '.'
		if len(precio_texto) > 3:
			for i in range(len(precio_texto)):
				if precio_texto[i] != '.':
					texto += precio_texto[i]
				else:
					cantidad_puntos_antes += 1

			precio_texto = texto
			self.price_pre_venta_value = texto
			texto = ''
		else:
			self.price_pre_venta_value = precio_texto

		#agregamos los puntitos
		cantidad_puntos_despues = 0
		j = 1
		if len(precio_texto) > 3:
			for i in range(len(precio_texto) -1, -1, -1):
				texto = precio_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto
					cantidad_puntos_despues += 1

				j += 1
		else:
			texto = precio_texto

		self.price_pre_venta_content_entry.set(texto)
		posicion_cursor = self.price_entry.index(INSERT)
		posicion_final = len(texto)

		#reajustamos la posicion del cursor de texto		
		if posicion_cursor == posicion_final or posicion_cursor + 1 == posicion_final:
			self.price_entry.delete(0, END)
			self.price_entry.insert(0, texto)

			if cantidad_puntos_despues < cantidad_puntos_antes:
				self.price_entry.icursor(posicion_cursor-1)
			elif cantidad_puntos_despues > cantidad_puntos_antes:
				self.price_entry.icursor(posicion_final)
			elif posicion_cursor + 1 == posicion_final:
				self.price_entry.icursor(posicion_cursor)
			else:
				self.price_entry.icursor(posicion_final)
		else:
			if cantidad_puntos_despues > cantidad_puntos_antes:
				self.price_entry.icursor(posicion_cursor+1)
			elif cantidad_puntos_despues < cantidad_puntos_antes:
				self.price_entry.icursor(posicion_cursor-1)

	def update_senha_pre_venta_content_entry(self, *args):
		texto = ''
		senha_texto = self.senha_pre_venta_content_entry.get()

		cantidad_puntos_antes = 0
		#eliminamos los puntos '.'
		if len(senha_texto) > 3:
			for i in range(len(senha_texto)):
				if senha_texto[i] != '.':
					texto += senha_texto[i]
				else:
					cantidad_puntos_antes += 1

			senha_texto = texto
			self.senha_pre_venta_value = texto
			texto = ''
		else:
			self.senha_pre_venta_value = senha_texto

		j = 1
		cantidad_puntos_despues = 0
		if len(senha_texto) > 3:
			for i in range(len(senha_texto) -1, -1, -1):
				texto = senha_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto
					cantidad_puntos_despues += 1

				j += 1
		else:
			texto = senha_texto

		self.senha_pre_venta_content_entry.set(texto)
		posicion_cursor = self.senha_entry.index(INSERT)
		posicion_final = len(texto)

		#reajustamos la posicion del cursor de texto		
		if posicion_cursor == posicion_final or posicion_cursor + 1 == posicion_final:
			self.senha_entry.delete(0, END)
			self.senha_entry.insert(0, texto)

			if cantidad_puntos_despues < cantidad_puntos_antes:
				self.senha_entry.icursor(posicion_cursor-1)
			elif cantidad_puntos_despues > cantidad_puntos_antes:
				self.senha_entry.icursor(posicion_final)
			elif posicion_cursor + 1 == posicion_final:
				self.senha_entry.icursor(posicion_cursor)
			else:
				self.senha_entry.icursor(posicion_final)
		else:
			if cantidad_puntos_despues > cantidad_puntos_antes:
				self.senha_entry.icursor(posicion_cursor+1)
			elif cantidad_puntos_despues < cantidad_puntos_antes:
				self.senha_entry.icursor(posicion_cursor-1)

	def update_price_content_entry(self, *args):
		texto = ''
		precio_texto = self.price_content_entry.get()

		cantidad_puntos_antes = 0
		#eliminamos los puntos '.'
		if len(precio_texto) > 3:
			for i in range(len(precio_texto)):
				if precio_texto[i] != '.':
					texto += precio_texto[i]
				else:
					cantidad_puntos_antes += 1

			precio_texto = texto
			self.price_value = texto
			texto = ''
		else:
			self.price_value = precio_texto

		cantidad_puntos_despues = 0
		j = 1
		if len(precio_texto) > 3:
			for i in range(len(precio_texto) -1, -1, -1):
				texto = precio_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto
					cantidad_puntos_despues += 1

				j += 1
		else:
			texto = precio_texto

		self.price_content_entry.set(texto)
		posicion_cursor = self.price_entry.index(INSERT)
		posicion_final = len(texto)

		#reajustamos la posicion del cursor de texto		
		if posicion_cursor == posicion_final or posicion_cursor + 1 == posicion_final:
			self.price_entry.delete(0, END)
			self.price_entry.insert(0, texto)

			if cantidad_puntos_despues < cantidad_puntos_antes:
				self.price_entry.icursor(posicion_cursor-1)
			elif cantidad_puntos_despues > cantidad_puntos_antes:
				self.price_entry.icursor(posicion_final)
			elif posicion_cursor + 1 == posicion_final:
				self.price_entry.icursor(posicion_cursor)
			else:
				self.price_entry.icursor(posicion_final)
		else:
			if cantidad_puntos_despues > cantidad_puntos_antes:
				self.price_entry.icursor(posicion_cursor+1)
			elif cantidad_puntos_despues < cantidad_puntos_antes:
				self.price_entry.icursor(posicion_cursor-1)

	def update_senha_content_entry(self, *args):
		#self.price_value_int = self.price_content_entry.get()
		texto = ''
		senha_texto = self.senha_content_entry.get()

		cantidad_puntos_antes = 0
		#eliminamos los puntos '.'
		if len(senha_texto) > 3:
			for i in range(len(senha_texto)):
				if senha_texto[i] != '.':
					texto += senha_texto[i]
				else:
					cantidad_puntos_antes += 1

			senha_texto = texto
			self.senha_value = texto
			texto = ''
		else:
			self.senha_value = senha_texto

		j = 1
		cantidad_puntos_despues = 0
		if len(senha_texto) > 3:
			for i in range(len(senha_texto) -1, -1, -1):
				texto = senha_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto
					cantidad_puntos_despues += 1

				j += 1
		else:
			texto = senha_texto

		self.senha_content_entry.set(texto)
		posicion_cursor = self.senha_entry.index(INSERT)
		posicion_final = len(texto)

		#reajustamos la posicion del cursor de texto		
		if posicion_cursor == posicion_final or posicion_cursor + 1 == posicion_final:
			self.senha_entry.delete(0, END)
			self.senha_entry.insert(0, texto)

			if cantidad_puntos_despues < cantidad_puntos_antes:
				self.senha_entry.icursor(posicion_cursor-1)
			elif cantidad_puntos_despues > cantidad_puntos_antes:
				self.senha_entry.icursor(posicion_final)
			elif posicion_cursor + 1 == posicion_final:
				self.senha_entry.icursor(posicion_cursor)
			else:
				self.senha_entry.icursor(posicion_final)
		else:
			if cantidad_puntos_despues > cantidad_puntos_antes:
				self.senha_entry.icursor(posicion_cursor+1)
			elif cantidad_puntos_despues < cantidad_puntos_antes:
				self.senha_entry.icursor(posicion_cursor-1)


	def update_monto_cuota_content_entry(self, *args):
		#self.price_value_int = self.price_content_entry.get()
		texto = ''
		monto_cuota_texto = self.monto_cuota_content_entry.get()

		#eliminamos los puntos '.'
		cantidad_puntos_antes = 0
		if len(monto_cuota_texto) > 3:
			for i in range(len(monto_cuota_texto)):
				if monto_cuota_texto[i] != '.':
					texto += monto_cuota_texto[i]
				else:
					cantidad_puntos_antes += 1

			monto_cuota_texto = texto
			self.monto_cuota_value = texto
			texto = ''
		else:
			self.monto_cuota_value = monto_cuota_texto

		j = 1
		cantidad_puntos_despues = 0
		if len(monto_cuota_texto) > 3:
			for i in range(len(monto_cuota_texto) -1, -1, -1):
				texto = monto_cuota_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto
					cantidad_puntos_despues += 1

				j += 1
		else:
			texto = monto_cuota_texto

		self.monto_cuota_content_entry.set(texto)
		posicion_cursor = self.monto_cuota_entry.index(INSERT)
		posicion_final = len(texto)

		#reajustamos la posicion del cursor de texto		
		if posicion_cursor == posicion_final or posicion_cursor + 1 == posicion_final:
			self.monto_cuota_entry.delete(0, END)
			self.monto_cuota_entry.insert(0, texto)
			if cantidad_puntos_despues < cantidad_puntos_antes:
				self.monto_cuota_entry.icursor(posicion_cursor-1)
			elif cantidad_puntos_despues > cantidad_puntos_antes:
				self.monto_cuota_entry.icursor(posicion_final)
			elif posicion_cursor + 1 == posicion_final:
				self.monto_cuota_entry.icursor(posicion_cursor)
			else:
				self.monto_cuota_entry.icursor(posicion_final)
		else:
			if cantidad_puntos_despues > cantidad_puntos_antes:
				self.monto_cuota_entry.icursor(posicion_cursor+1)
			elif cantidad_puntos_despues < cantidad_puntos_antes:
				self.monto_cuota_entry.icursor(posicion_cursor-1)
	
	def set_value_pre_venta(self, pre_venta, posicion_pre_venta, agregando):
		if agregando:
			#en caso de que se este agregando una pre_venta y el paquete no tenga ninguna pre_venta todavia
			self.pre_ventas.append(pre_venta)
			self.si_pre_venta = True
		else:
			#en caso de editar una pre_venta
			self.pre_ventas[posicion_pre_venta] = pre_venta

			if self.estoy_en_precio_detalles:
				es_la_pre_venta_actual = self.controller.es_la_pre_venta_actual(pre_venta)
				self.controller.guardar_paquete_background(self.paquete, self.pos_paquete, es_la_pre_venta_actual)

				if es_la_pre_venta_actual:
					texto = self.convert_amount_to_string(self.paquete.get_precio_pre_venta(), True)
					self.precio_value_paquete_det.set(texto)
					texto = self.convert_amount_to_string(self.paquete.get_senha_pre_venta(), True)
					self.senha_value_paquete_det.set(texto)

				self.estoy_en_precio_detalles = False

	def view_show_message(self, success, msj):
		message = Toplevel(self.parent, bg='#F9F9F9')
		message.geometry('300x100+750+440')
		message.resizable(width=False, height=False)

		message_label = Label(message, text=msj, width='40', height='2', bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		message_label.config(font=('tahoma', 10))
		message_label.pack()

		ok = Button(message, width=35, height=30, bg='#F9F9F9', highlightthickness=0, relief=GROOVE, borderwidth=0)
		ok.config(font=('tahoma', 10))
		if success:
			ok.config(image=self.imagenes['ok_icon'])
		else:
			ok.config(image=self.imagenes['not_ok_icon'])

		#if self.frame_pre_venta is not None and success:
		#	print('CUANDO ENTRO ACA???**************')
		#	self.widget_destroy(self.frame_pre_venta)
		#	self.frame_pre_venta = None
			#self.content_pre_venta_button.set('Disponible')

		ok.config(command=lambda:self.widget_destroy(message))
		ok.pack(pady=10)

	def widget_destroy(self, widget):
		widget.destroy()

	def view_calendar(self, frame, content, cod_fecha, x, y):
		'''
		cod = 0 fecha de viaje al momento de creacion un paquete
		cod = 1 fecha de viaje al momento de edicion de paquete
		cod = 2 fecha de inicio de pre venta
		cod = 3 fecha de fin de pre venta
		'''
		frame_calendar = Frame(frame, bg='#F9F9F9', width='260', height='280', relief=GROOVE, borderwidth=1)
		frame_calendar.place(relx=x, rely=y)
		frame_calendar.pack_propagate(0)

		frame_date = Frame(frame_calendar, bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		frame_date.pack()

		fecha = None
		if cod_fecha == 1:
			#en caso de que se este editando el paquete
			fecha = self.fecha_de_viaje
		elif cod_fecha == 2:
			#en caso de que vayemos a seleccionar la fecha de inicio de la pre venta
			fecha = self.pre_venta_fecha_inicio
		elif cod_fecha == 3:
			#en caso de que vayemos a seleccionar la fecha de fin de la pre venta
			fecha = self.pre_venta_fecha_fin
		elif cod_fecha == 4:
			#en caso de que selecciones una fecha de nacimiento
			fecha = self.fecha_nacimiento_value

		calendario = Calendar(frame_date, fecha)
		ok = Button(frame_calendar, width=5, bg='#F9F9F9', text='OK', command=lambda:
				self.update_button_fecha_de_viaje(frame_calendar, content, calendario, cod_fecha))
		ok.pack(pady=2)

	def update_button_fecha_de_viaje(self, frame_calendar, content, calendario, cod_fecha):
		'''
		cod = 0 fecha de viaje al momento de creacion un paquete
		cod = 1 fecha de viaje al momento de edicion de paquete
		cod = 2 fecha de inicio de pre venta
		cod = 3 fecha de fin de pre venta
		'''

		frame_calendar.destroy()
		date = calendario.get_date_selected()

		if cod_fecha == 1 or cod_fecha == 0:
			self.fecha_de_viaje = date
		elif cod_fecha == 2:
			if date is not None:
				self.pre_venta_fecha_inicio = date
		elif cod_fecha == 3:
			if date is not None:
				self.pre_venta_fecha_fin = date
		elif cod_fecha == 4:
			#en caso de que selecciones una fecha de nacimiento
			if date is not None:
				self.fecha_nacimiento_value = date

		if date is None:
			return

		if date.day < 10:
			day = '0' + str(date.day)
		else:
			day = str(date.day)

		if date.month < 10:
			month = '0' + str(date.month)
		else:
			month = str(date.month)

		if cod_fecha == 0:
			self.combobox_add_fecha.destroy()
			self.lista_fecha.append(date)
			self.lista_fecha_combobox.append(day + '/' + month + '/' + str(date.year))
			self.combobox_add_fecha = ttk.Combobox(self.frame_agregar_paquete, values=self.lista_fecha_combobox)
			self.combobox_add_fecha.config(state='readonly', font=(13), width='9', height='6', background='#F9F9F9')
			self.combobox_add_fecha.set(day + '/' + month + '/' + str(date.year))
			self.combobox_add_fecha.place(relx=0.17, rely=0.292)
		else:
			content.set(day + '/' + month + '/' + str(date.year))

	def view_usuarios(self):
		self.view_buscar_cliente()

	def view_buscar_cliente(self):
		self.set_button_bold('usuarios')
		self.anterior = 'usuarios'

		#DEFINIMOS EL FRAME 
		frame = Frame(self.main_frame, width='900', height='700', bg='#F9F9F9', relief=GROOVE, borderwidth=0)

		#declaramos el un string que alamacena el contenido ingresado
		self.clientes = []

		#********************************************************

		label_nombre_cliente = Label(frame, text='Nombre:', font=('tahoma', 14, 'bold'), width=14, height=2, bg='#F9F9F9')
		label_nombre_cliente.config(fg='#48C2FA', relief=GROOVE, borderwidth=0)
		#declaramos una entreada para ingresar los datos
		self.nombre_buscado_content_entry = StringVar()
		entry = Entry(frame, width='15', font=('tahoma', 15), textvariable=self.nombre_buscado_content_entry)

		label_apellido_cliente = Label(frame, text='Apellido:', font=('tahoma', 14, 'bold'), width=7, height=2, bg='#F9F9F9')
		label_apellido_cliente.config(fg='#48C2FA', relief=GROOVE, borderwidth=0, anchor=W)
		#declaramos una entreada para ingresar los datos
		self.apellido_buscado_content_entry = StringVar()
		apellido_entry = Entry(frame, width='15', font=('tahoma', 15), textvariable=self.apellido_buscado_content_entry)

		#view cedula cliente
		label_cedula = Label(frame, text='Cedula:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label_cedula.config(font=('tahoma', 14, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)

		self.cedula_busqueda_content_entry = StringVar()
		self.cedula_buscada_value = None
		self.cedula_buscada_entry = Entry(frame, width='15', font=('tahoma', 15), textvariable=self.cedula_busqueda_content_entry)
		
		#agregar paquete view
		agregar_cliente_button = Button(frame, text='Registrar un cliente', width='210', height='27', relief=GROOVE, borderwidth=0)
		agregar_cliente_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#27A221', activeforeground='#27A221', highlightthickness=0, anchor=W)
		agregar_cliente_button.config(image=self.imagenes['add_icon'], compound=LEFT)

		#mostramos los RESULTADOS DE LA BUSQUEDA
		#creamos un frame, un canvas y un scrollbar para luego conectarlos
		self.view_result_busqueda_cliente = []
		frame_result = Frame(frame, width='800', height='450', bg='#FFFFFF', relief=GROOVE, borderwidth=1)
		self.canvas=Canvas(frame_result,bg='#FFFFFF',width=800,height=450)
		vbar=Scrollbar(frame_result,orient=VERTICAL)
		vbar.pack(side=RIGHT,fill=Y)
		vbar.config(command=self.canvas.yview)
		self.canvas.config(yscrollcommand=vbar.set)
		self.canvas.pack()
		frame_result.pack(side='bottom', pady=20)
		frame_result.pack_propagate(0)

		#los botones estan dentro de un frame auxiliar
		self.frame_result_aux = Frame(self.canvas, bg='#FFFFFF', borderwidth=0, relief=GROOVE)
		self.canvas.create_window(0, 0, window=self.frame_result_aux, anchor=NW)
		self.frame_result_aux.bind("<Configure>", self.on_frame_configure)

		#almacenamos los resultados en forma de botones (views)
		self.view_result_busqueda_paquete = []

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************
		#detectamos los cambios cada vez que se escribe algo
		self.nombre_buscado_content_entry.trace("w", self.buscar_cliente_por_nombre)
		self.apellido_buscado_content_entry.trace("w", self.buscar_cliente_por_apellido)
		self.cedula_busqueda_content_entry.trace("w", self.buscar_cliente_por_cedula)
		agregando = True
		agregar_cliente_button.config(command=lambda: self.view_cliente_toplevel(None, None, None, agregando))

		#********************************************************
		#				PACK A TODOS LOS BOTONES				*
		#********************************************************
		#label_nombre_paquete.pack(side='left', padx=25, pady=42, anchor=NW)
		label_nombre_cliente.place(relx=0.028, rely=0.04)
		label_apellido_cliente.place(relx=0.43, rely=0.04)
		entry.place(relx=0.19, rely=0.0525)
		apellido_entry.place(relx=0.55, rely=0.0525)
		label_cedula.place(relx=0.08, rely=0.13)
		self.cedula_buscada_entry.place(relx=0.19, rely=0.14)
		agregar_cliente_button.place(relx=0.065, rely=0.23)
		frame.pack(padx=20, pady=20, anchor=NE)
		frame.pack_propagate(0)

		self.show_clientes()

		self.switch_frame(frame)

	def buscar_cliente_por_nombre(self, *args):
		#result_busqueda_paquete = self.controller.buscar_paquete(content1=self.content_entry.get(), content2=self.radio_variable.get(),
		#							content3=self.combobox_anhos.get(), content4=self.combobox_tipos.get(), content5=self.combobox_sub_tipos.get())
		result_busqueda_cliente = self.controller.buscar_cliente(content1=self.nombre_buscado_content_entry.get(),
													content2=self.apellido_buscado_content_entry.get(), content3=self.cedula_buscada_value)
		self.set_values_clientes_posiciones(result_busqueda_cliente)
		for cliente in self.clientes:
			print('Nombre:{} Cedula:{}'.format(cliente.get_nombre(), cliente.get_cedula()))
		self.show_clientes()

	def set_values_clientes_posiciones(self, result_busqueda_clientes):
		self.clientes = result_busqueda_clientes[0]
		self.clientes_posiciones = result_busqueda_clientes[1]

	def buscar_cliente_por_apellido(self, *args):
		#result_busqueda_paquete = self.controller.buscar_paquete(content1=self.content_entry.get(), content2=self.radio_variable.get(),
		#							content3=self.combobox_anhos.get(), content4=self.combobox_tipos.get(), content5=self.combobox_sub_tipos.get())
		result_busqueda_cliente = self.controller.buscar_cliente(content1=self.nombre_buscado_content_entry.get(),
													content2=self.apellido_buscado_content_entry.get(), content3=self.cedula_buscada_value)
		self.set_values_clientes_posiciones(result_busqueda_cliente)
		for cliente in self.clientes:
			print('Nombre:{} Cedula:{}'.format(cliente.get_nombre(), cliente.get_cedula()))
		self.show_clientes()

	def buscar_cliente_por_cedula(self, *args):
		self.update_cedula_buscada_content_entry()
		result_busqueda_cliente = self.controller.buscar_cliente(content1=self.nombre_buscado_content_entry.get(),
													content2=self.apellido_buscado_content_entry.get(), content3=self.cedula_buscada_value)
		self.set_values_clientes_posiciones(result_busqueda_cliente)
		for cliente in self.clientes:
			print('Nombre:{} Cedula:{}'.format(cliente.get_nombre(), cliente.get_cedula()))

		self.show_clientes()

	def view_registrar_cliente(self):
		self.set_button_bold('usuarios')
		self.anterior = 'usuarios'

		print('View: creando cliente...')

		#DEFINIMOS EL FRAME
		#self.frame_pre_venta = None
		self.cliente_top_level.title('Registrar Cliente')
		self.frame_registrar_cliente = Frame(self.cliente_top_level, width='1000', height='900', bg='#F9F9F9', relief=GROOVE, borderwidth=0)

		#********************************************************
		#  AGREGAMOS LAS ETIQUETAS CORRESPONDIENTE A LOS DATOS	*
		#********************************************************

		#view nombre cliente
		label = Label(self.frame_registrar_cliente, text='Nombre:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.06)

		name_content_entry = StringVar()
		name_entry = Entry(self.frame_registrar_cliente, width='20', font=('tahoma', 13), textvariable=name_content_entry)
		name_entry.place(relx=0.16, rely=0.075)

		#view apellido cliente
		label = Label(self.frame_registrar_cliente, text='Apellido:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.128)

		apellido_content_entry = StringVar()
		apellido_entry = Entry(self.frame_registrar_cliente, width='20', font=('tahoma', 13), textvariable=apellido_content_entry)
		apellido_entry.place(relx=0.16, rely=0.141)

		#view cedula cliente
		label = Label(self.frame_registrar_cliente, text='Cedula:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.195)

		self.cedula_content_entry = StringVar()
		self.cedula_value = None
		self.cedula_entry_registrar_cliente = Entry(self.frame_registrar_cliente, width='20', font=('tahoma', 13), textvariable=self.cedula_content_entry)
		self.cedula_entry_registrar_cliente.place(relx=0.16, rely=0.207)

		#view fecha de nacimiento cliente
		label = Label(self.frame_registrar_cliente, text='Nacimiento:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.262)

		content_button_fecha_nacimiento = StringVar()
		content_button_fecha_nacimiento.set('-- / -- / --')
		self.fecha_nacimiento_value = None
		button_fecha_nacimiento = Button(self.frame_registrar_cliente, textvariable=content_button_fecha_nacimiento, width='8', height='1', relief=GROOVE, borderwidth=0)
		button_fecha_nacimiento.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
		button_fecha_nacimiento.place(relx=0.16, rely=0.272)

		#view edad cliente
		label = Label(self.frame_registrar_cliente, text='Edad:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.329)

		#insertamos un COMBOBOX para listar la edad de las personas
		lista_edades = self.controller.generar_lista_edades()
		self.combobox_edad = ttk.Combobox(self.frame_registrar_cliente, values=lista_edades)

		self.combobox_edad.set('')
		self.combobox_edad.config(state='readonly', font=(15), width='3', height='6', background='#F9F9F9')#insertamos un COMBOBOX para seleccionar la edad
		self.combobox_edad.place(relx=0.16, rely=0.345)

		#view nacionalidad
		label = Label(self.frame_registrar_cliente, text='Nacionalidad:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.396)

		#insertamos un COMBOBOX para listar las nacionalidades de las personas
		lista_nacionalidades = self.controller.generar_lista_nacionalidades()
		self.combobox_nacionalidades = ttk.Combobox(self.frame_registrar_cliente, values=lista_nacionalidades)
		self.combobox_nacionalidades.set('Paraguay')

		self.combobox_nacionalidades.config(state='readonly', font=(15), width='15', height='6', background='#F9F9F9')#insertamos un COMBOBOX para seleccionar la edad
		self.combobox_nacionalidades.place(relx=0.17, rely=0.413)

		#view telefono 1
		label = Label(self.frame_registrar_cliente, text='Telefono 1:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.55, rely=0.06)

		self.telefono1_content_entry = StringVar()
		self.telefono1_value = None
		telefono1_entry = Entry(self.frame_registrar_cliente, width='20', font=('tahoma', 13), textvariable=self.telefono1_content_entry)
		telefono1_entry.place(relx=0.68, rely=0.075)

		#view telefono 2
		label = Label(self.frame_registrar_cliente, text='Telefono 2:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.55, rely=0.128)

		self.telefono2_content_entry = StringVar()
		self.telefono2_value = None
		telefono2_entry = Entry(self.frame_registrar_cliente, width='20', font=('tahoma', 13), textvariable=self.telefono2_content_entry)
		telefono2_entry.place(relx=0.68, rely=0.141)

		#view email
		label = Label(self.frame_registrar_cliente, text='Email:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.55, rely=0.195)

		self.email_content_entry = StringVar()
		#self.email_value = None
		email_entry = Entry(self.frame_registrar_cliente, width='20', font=('tahoma', 13), textvariable=self.email_content_entry)
		email_entry.place(relx=0.68, rely=0.207)

		#view ok and cancel
		save_button = Button(self.frame_registrar_cliente, text='Guardar', width=110, height=30, relief=GROOVE, borderwidth=0)
		save_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		save_button.config(image=self.imagenes['save_icon'], compound=LEFT)
		save_button.place(relx=0.5, rely=0.85)

		cancel_button = Button(self.frame_registrar_cliente, text='Cancelar', width=110, height=30, relief=GROOVE, borderwidth=0)
		cancel_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		cancel_button.config(image=self.imagenes['not_ok_icon'], compound=LEFT)
		cancel_button.place(relx=0.34, rely=0.85)
		#********************************************************

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************
		self.cedula_content_entry.trace("w", self.update_cedula_content_entry)
		button_fecha_nacimiento.config(command=lambda:self.view_calendar(self.frame_registrar_cliente, content_button_fecha_nacimiento, 4, 0.17, 0.277))
		save_button.config(command=lambda:self.controller.guardar_cliente(name_content_entry.get(), apellido_content_entry.get(), self.cedula_value,
															self.fecha_nacimiento_value, self.combobox_edad.get(), self.combobox_nacionalidades.get(),
															self.telefono1_content_entry.get(), self.telefono2_content_entry.get(), 
															self.email_content_entry.get(), self.cliente_top_level))

		cancel_button.config(command=lambda:self.widget_destroy(self.cliente_top_level))

		self.frame_registrar_cliente.pack(padx=20, pady=20, anchor=NE)
		self.frame_registrar_cliente.pack_propagate(0)

	def view_cliente_toplevel(self, frame, paquete, pos_paquete, agregando):
		print('preparando: view_cliente_toplevel')
		self.cliente_top_level = Toplevel(self.parent, bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		self.cliente_top_level.geometry('1000x800+450+100')
		self.cliente_top_level.resizable(width=False, height=False)

		if agregando:
			self.view_registrar_cliente()
		else:
			self.view_paquete_detalles(frame, paquete, pos_paquete)

	def update_cedula_buscada_content_entry(self):
		texto = ''
		cedula_texto = self.cedula_busqueda_content_entry.get()

		cantidad_puntos_antes = 0
		#eliminamos los puntos '.'
		if len(cedula_texto) > 3:
			for i in range(len(cedula_texto)):
				if cedula_texto[i] != '.':
					texto += cedula_texto[i]
				else:
					cantidad_puntos_antes += 1

			cedula_texto = texto
			self.cedula_buscada_value = texto
			texto = ''
		else:
			self.cedula_buscada_value= cedula_texto

		cantidad_puntos_despues = 0
		j = 1
		#agregamos los puntos
		if len(cedula_texto) > 3:
			for i in range(len(cedula_texto) -1, -1, -1):
				texto = cedula_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto
					cantidad_puntos_despues += 1

				j += 1
		else:
			texto = cedula_texto

		self.cedula_busqueda_content_entry.set(texto)
		posicion_cursor = self.cedula_buscada_entry.index(INSERT)
		posicion_final = len(texto)

		#reajustamos la posicion del cursor de texto		
		if posicion_cursor == posicion_final or posicion_cursor + 1 == posicion_final:
			self.cedula_buscada_entry.delete(0, END)
			self.cedula_buscada_entry.insert(0, texto)

			if cantidad_puntos_despues < cantidad_puntos_antes:
				self.cedula_buscada_entry.icursor(posicion_cursor-1)
			elif cantidad_puntos_despues > cantidad_puntos_antes:
				self.cedula_buscada_entry.icursor(posicion_final)
			elif posicion_cursor + 1 == posicion_final:
				self.cedula_buscada_entry.icursor(posicion_cursor)
			else:
				self.cedula_buscada_entry.icursor(posicion_final)
		else:
			if cantidad_puntos_despues > cantidad_puntos_antes:
				self.cedula_buscada_entry.icursor(posicion_cursor+1)
			elif cantidad_puntos_despues < cantidad_puntos_antes:
				self.cedula_buscada_entry.icursor(posicion_cursor-1)

	def update_cedula_content_entry(self, *args):
		texto = ''
		cedula_texto = self.cedula_content_entry.get()

		cantidad_puntos_antes = 0
		#eliminamos los puntos '.'
		if len(cedula_texto) > 3:
			for i in range(len(cedula_texto)):
				if cedula_texto[i] != '.':
					texto += cedula_texto[i]
				else:
					cantidad_puntos_antes += 1

			cedula_texto = texto
			self.cedula_value = texto
			texto = ''
		else:
			self.cedula_value = cedula_texto

		cantidad_puntos_despues = 0
		j = 1
		if len(cedula_texto) > 3:
			for i in range(len(cedula_texto) -1, -1, -1):
				texto = cedula_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto
					cantidad_puntos_despues += 1

				j += 1
		else:
			texto = cedula_texto

		self.cedula_content_entry.set(texto)
		posicion_cursor = self.cedula_entry_registrar_cliente.index(INSERT)
		posicion_final = len(texto)

		#reajustamos la posicion del cursor de texto		
		if posicion_cursor == posicion_final or posicion_cursor + 1 == posicion_final:
			self.cedula_entry_registrar_cliente.delete(0, END)
			self.cedula_entry_registrar_cliente.insert(0, texto)

			if cantidad_puntos_despues < cantidad_puntos_antes:
				self.cedula_entry_registrar_cliente.icursor(posicion_cursor-1)
			elif cantidad_puntos_despues > cantidad_puntos_antes:
				self.cedula_entry_registrar_cliente.icursor(posicion_final)
			elif posicion_cursor + 1 == posicion_final:
				self.cedula_entry_registrar_cliente.icursor(posicion_cursor)
			else:
				self.cedula_entry_registrar_cliente.icursor(posicion_final)
		else:
			if cantidad_puntos_despues > cantidad_puntos_antes:
				self.cedula_entry_registrar_cliente.icursor(posicion_cursor+1)
			elif cantidad_puntos_despues < cantidad_puntos_antes:
				self.cedula_entry_registrar_cliente.icursor(posicion_cursor-1)

	def show_clientes(self):
		cliente_view = None

		#eliminamos los resultados anteriores a la busqueda actual (si elminamos la lista anterior tambien se elimina la lista actual, por ref)
		for cliente_view in self.view_result_busqueda_cliente:
			cliente_view.destroy()

		self.view_result_busqueda_cliente = []

		#aplicamos los nuevos resultados de la busqueda
		cliente_view = None
		aux = -1

		for cliente in self.clientes:
			aux += 1

			cliente_view = Frame(self.frame_result_aux, bg='#F9F9F9', width='770', height='150', relief=GROOVE, borderwidth=0)
			cliente_view.pack(padx=10, pady=5)

			'''
			#imagen view
			image_frame = Frame(cliente_view, bg='#F9F9F9', width='120', height='140', relief=GROOVE, borderwidth=0)
			image_frame.place(relx=0.02, rely=0.02)

			imagen_original = None
			if paquete.get_cantidad_de_imagenes() == 0:
				imagen_original = Image.open('imagenes/group_tours.png')
			else:
				imagen_original = paquete.get_imagenes()[0]

			imagen_original = imagen_original.resize((170, 140), Image.ANTIALIAS)

			logo = ImageTk.PhotoImage(imagen_original)
			label_logo = Label(image_frame, width=230, height=140, relief=GROOVE, borderwidth=0)
			label_logo.config(bg='#F9F9F9')
			label_logo.config(image=logo)
			label_logo.photo = logo
			label_logo.pack()
			label_logo.pack_propagate(0)
			'''
			#view nombre
			cliente_name_view = Label(cliente_view, text=cliente.get_nombre(), width='18', height='1', relief=GROOVE, borderwidth=1)
			cliente_name_view.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535',
											activeforeground='#343535', anchor=W) #posicionamos el texto a la izquierda
			#cliente_name_view.place(relx=0.05, rely=0.05)

			#view apellido
			cliente_lastname_view = Label(cliente_view, text=cliente.get_apellido(), width='18', height='1', relief=GROOVE, borderwidth=1)
			cliente_lastname_view.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535',
											activeforeground='#343535', anchor=W) #posicionamos el texto a la izquierda
			#cliente_lastname_view.place(relx=0.05, rely=0.25)

			cliente_nombre_apellido_view = Label(cliente_view, width='20', height='1', relief=GROOVE, borderwidth=1)
			cliente_nombre_apellido_view.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535',
											activeforeground='#343535', anchor=W) #posicionamos el texto a la izquierda
			cliente_nombre_apellido_view.place(relx=0.05, rely=0.05)
			texto = cliente.get_nombre() + ' ' + cliente.get_apellido()
			nombre_apellido1 = ''
			nombre_apellido2 = ''
			pos_y = 0.25
			if len(texto) <= View.CANTIDAD_CARACTERES:
				cliente_nombre_apellido_view.config(text=texto)
			else:
				[nombre_apellido1, nombre_apellido2] = self.dividir_nombre_apellido(texto, nombre_apellido1, nombre_apellido2)
				cliente_nombre_apellido_view.config(text=nombre_apellido1)

				cliente_nombre_apellido_view_aux = Label(cliente_view, width='20', height='1', relief=GROOVE, borderwidth=1)
				cliente_nombre_apellido_view_aux.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535',
												activeforeground='#343535', anchor=W) #posicionamos el texto a la izquierda
				cliente_nombre_apellido_view_aux.config(text=nombre_apellido2)
				cliente_nombre_apellido_view_aux.place(relx=0.05, rely=pos_y)
				pos_y += 0.2

			#view cedula
			texto = self.convert_amount_to_string(cliente.get_cedula(), False)
			cliente_cedula_view = Label(cliente_view, text=texto, width='20', height='1', relief=GROOVE, borderwidth=1)
			cliente_cedula_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535',
											activeforeground='#343535', anchor=W) #posicionamos el texto a la izquierda
			cliente_cedula_view.place(relx=0.05, rely=pos_y)
			pos_y += 0.2

			#view nacionalidad
			cliente_nacionalidad_view = Label(cliente_view, text=cliente.get_nacionalidad(), width='20', height='1', relief=GROOVE, borderwidth=1)
			cliente_nacionalidad_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535',
											activeforeground='#343535', anchor=W) #posicionamos el texto a la izquierda
			cliente_nacionalidad_view.place(relx=0.05, rely=pos_y)
			'''
			#fecha view
			date = paquete.get_fecha_de_viaje()
			texto = self.convert_date_to_string(date)

			paquete_fecha_de_viaje_view = Label(cliente_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
			paquete_fecha_de_viaje_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030',
									activeforeground='#2F3030', highlightthickness=0, anchor=W)
			paquete_fecha_de_viaje_view.place(relx=0.38, rely=0.29)

			#vigente view
			texto = 'Vigente'
			if paquete.get_esta_vigente() == False:
				texto = 'No vigente'

			paquete_fecha_de_viaje_view = Label(cliente_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
			paquete_fecha_de_viaje_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030',
											activeforeground='#2F3030', highlightthickness=0, anchor=W)
			paquete_fecha_de_viaje_view.place(relx=0.38, rely=0.52)

			texto = 'Tipo: ' + paquete.TRASLADO
			paquete_fecha_de_viaje_view = Label(cliente_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
			paquete_fecha_de_viaje_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030',
												activeforeground='#2F3030', highlightthickness=0, anchor=W)
			paquete_fecha_de_viaje_view.place(relx=0.38, rely=0.75)

			#SEGUNDA CULUMNA
			#precio view
			texto = ''

			if paquete.si_pre_venta():
				texto = self.convert_amount_to_string(paquete.get_precio_pre_venta(), True)
			else:
				texto = self.convert_amount_to_string(paquete.get_precio(), True)

			paquete_precio_view = Label(cliente_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
			paquete_precio_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
			paquete_precio_view.place(relx=0.72, rely=0.07)

			#pre venta view
			if paquete.si_pre_venta():
				texto = 'Pre venta: si'
			else:
				texto = 'Pre venta: no'

			paquete_pre_venta_view = Label(cliente_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
			paquete_pre_venta_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
			paquete_pre_venta_view.place(relx=0.72, rely=0.29)

			#lugares disponibles view
			texto = 'Lugares disponible: '
			lugares_disponibles = paquete.get_lugares_disponibles()
			color = '#2F3030'
			if lugares_disponibles > 0:
				texto = texto + str(lugares_disponibles)
			elif lugares_disponibles == 0:
				texto = 'SOLD OUT'
				color = '#E60700'
			else:
				texto = texto + '--'

			paquete_pre_venta_view = Label(cliente_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
			paquete_pre_venta_view.config(font=('tahoma', 13), bg='#F9F9F9', fg=color, activeforeground=color, highlightthickness=0, anchor=W)
			paquete_pre_venta_view.place(relx=0.72, rely=0.52)

			pos_paquete = self.paquetes_posiciones[aux]

			#detalles view
			texto = 'Ver detalles      >'
			paquete_detalles_view = Button(cliente_view, text=texto, width='16', height='1', relief=GROOVE, borderwidth=0)
			paquete_detalles_view.config(font=('tahoma', 13), bg='#27A221', fg='#FFFFFF', activeforeground='#FFFFFF',
										activebackground='#20801B', highlightthickness=0, anchor=W)
			paquete_detalles_view.place(relx=0.72, rely=0.75)
			paquete_detalles_view.config(command=lambda paquete=paquete, pos_paquete=pos_paquete:
									self.view_agregar_and_detalles_toplevel(None, paquete, pos_paquete, False))
			#print(paquete_name_view.config("text")[-1])
			#print(paquete_detalles_view.config("text")[-1])

		'''
			self.view_result_busqueda_cliente.append(cliente_view)

	def dividir_nombre_apellido(self, nombre_completo, nombre_apellido1, nombre_apellido2):
		#separamos el nombre completo en dos partes

		marcador = 0
		for i in reversed(range(View.CANTIDAD_CARACTERES)):
			if nombre_completo[i] == ' ':
				marcador = i
				break
		i = 0
		for i in range(marcador+1):
			nombre_apellido1 += nombre_completo[i]

		i = marcador + 1
		while i < len(nombre_completo):
			nombre_apellido2 += nombre_completo[i]
			i += 1

		return [nombre_apellido1, nombre_apellido2]

	def view_facturas(self):
		self.set_button_bold('facturas')
		self.anterior = 'facturas'

		frame = Frame(self.main_frame, width='900', height='700', bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		frame.pack(padx=20, pady=50, anchor=NE)

		label_paquetes = Label(frame, text='Facturas', font=('tahoma', 55, 'bold'), width=9, height=3, relief=GROOVE, borderwidth=2)
		label_paquetes.config(bg='#F9F9F9')
		label_paquetes.pack()

		self.switch_frame(frame)

	def switch_frame(self, frame):
		if self.right_frame is not None:
			self.right_frame.destroy()

		self.right_frame = frame
		self.right_frame.pack_propagate(0)
		self.right_frame.pack(padx=20, pady=50, anchor=NE)

	def set_button_bold(self, nuevo_bold):
		self.buttons[nuevo_bold].config(font=('tahoma', 17, "bold"))

		if self.anterior is not nuevo_bold:
			self.buttons[self.anterior].config(font=('tahoma', 17))

	#@staticmethod
	def show_parent(self):
		self.parent.mainloop()

	'''def leerCedula(self):
		cedula = input("Ingrese el numero de documento de la persona a buscar: ")
		return cedula
		
	def imprimirEnPantalla(self, resultado):
		print('La persona encontrada es: {}'.format(resultado))
	

	def vista_agregar_usuario(self):
		print("Crear nueva usuario")
		cedula = input("Ingrese documento del nuevo usuario: ")
		nombre = input("Ingrese nombre del nuevo usuario ")
		apellido = input("Ingrese apellido del nuevo usuario: ")
		nuevo_usuario = Usuario(cedula, nombre, apellido)
		#nuevo_usuario = Usuario( "Victor", "Cubas", "4028760", "18/11/1991", 20, "Paraguay" )
		return nuevo_usuario
	
	def vista_listar_usuarios(self, lista_usuarios):
		print ("Listado de usuarios en la base de datos: \n")
		if lista_usuarios:
			for usuario in lista_usuarios:
				print(usuario.__str__())
				#print('Nombre: {}; Apellido: {}; Documento: {}.'.format(usuario.persona, usuario.apellido, usuario.documento))

	def vista_liquidar_in(self):
		print("Ingrese los datos correspondiente a la factura")
		tipo_factura = input("Tipo de factura: ")
		nombre_razon_social = input("Nombre o razon social: ")
		numero_factura = input("Numero de factura: ")
		fecha_de_pago = input("Fecha de pago: ")
		hora_de_pago = input("Hora de pago: ")
		
		if tipo == "CREDITO":
			fecha_vencimiento = input("Fecha de vencimiento: ")

	def vista_liquidar_out(self):
		pass

	def vista_senhar_in(self):
		pass

	def vista_senhar_out(self):
		pass'''
