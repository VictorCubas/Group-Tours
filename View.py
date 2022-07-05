#view.py
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
#import tkFont
from Usuario import Usuario
from Calendar import Calendar
from TemporizadorVigencia import TemporizadorVigencia

import copy

class View:
	'''
	Implementando la vista de la app
	'''

	VIEW_PAQUETES_COD = 1
	VIEW_BUSCAR_PAQUETE = 2
	VIEW_CREAR_PAQUETE = 3
	VIEW_USUARIOS_COD = 4

	def __init__(self, controller, parent):
		self.controller = controller
		#self.parent = Tk()
		self.parent = parent
		self.parent.title('Group Tours')
		self.parent.geometry('1300x800+300+80')
		self.parent.resizable(width=False, height=False)
		#self.parent.configure(background='white')

		self.main_frame = Frame(self.parent, width='1300', height='800', bg='#F9F9F9')
		self.main_frame.pack_propagate(0)
		self.left_frame = Frame(self.main_frame, width='365', height='400', bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		self.right_frame = None
		#self.right_frame = Frame(self.main_frame, width='900', height='700', bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		#self.right_frame.pack_propagate(0)

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
						'add_icon': PhotoImage(file='imagenes/add_icon.png')}

		#self.inicio_button = Button(self.left_frame, text=' Inicio', font=('tahoma', 17), bg='#F9F9F9', width='300', height='90')
		#self.inicio_button.config(font=('arial', 19, "bold"))
		#self.inicio_button.config(justify=RIGHT)
		self.buttons['inicio'].config(image=self.imagenes['inicio_icon'], compound=LEFT)
		self.buttons['inicio'].config(anchor=W)  #posicionamos el texto a la izquierda
		self.buttons['inicio'].config(command=lambda:self.view_inicio())
		self.buttons['inicio'].pack()

		self.buttons['paquetes'].config(image=self.imagenes['paquete_icon'], compound=LEFT)
		self.buttons['paquetes'].config(anchor=W)
		self.buttons['paquetes'].config(command=lambda:self.view_paquetes(True))
		self.buttons['paquetes'].pack()

		self.buttons['usuarios'].config(image=self.imagenes['usuario_icon'], compound=LEFT)
		self.buttons['usuarios'].config(anchor=W)
		self.buttons['usuarios'].config(command=lambda:self.view_usuarios(True))
		self.buttons['usuarios'].pack()	

		self.buttons['facturas'].config(image=self.imagenes['factura_icon'], compound=LEFT)
		self.buttons['facturas'].config(anchor=W)
		self.buttons['facturas'].config(command=lambda:self.view_facturas())
		self.buttons['facturas'].pack()

		self.left_frame.pack(side='left', padx=20, pady=80, anchor=NW)
		self.main_frame.pack()

		self.pila_anterior = []
		self.pila_siguiente = []
		
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

		label_welcome = Label(frame, text='Bienvenido', font=('tahoma', 55, 'bold'), width=10, height=3, relief=GROOVE, borderwidth=0)
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
		button_buscar_paquete = Button(frame_bottom, text='Buscar Paquete', font=('tahoma', 11), bg='#66CDFC', width='100', height='100', highlightthickness=0, borderwidth=0)
		button_buscar_paquete.config(activebackground='#48C2FA')
		button_buscar_usuario = Button(frame_bottom, text='Buscar Usuario', font=('tahoma', 11), bg='#66CDFC', width='100', height='100', highlightthickness=0, borderwidth=0)
		button_buscar_usuario.config(activebackground='#48C2FA')

		#********************************************************
		#			AGREGAMOS ICONOS A LOS BOTONES				*
		#********************************************************
		button_buscar_paquete.config(image=self.imagenes['lupa_icon'], compound=TOP)
		button_buscar_usuario.config(image=self.imagenes['lupa_icon'], compound=TOP)

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************
		button_buscar_paquete.config(command=lambda:self.view_buscar_paquete(True))
		button_buscar_usuario.config(command=lambda:self.view_usuarios(True))

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

	def view_paquetes(self, next_back_starting):
		self.set_button_bold('paquetes')
		self.anterior = 'paquetes'

		if next_back_starting:
			self.pila_anterior = []
			self.pila_siguiente = []

		#********************************************************
		#				CREAMOS TODOS LOS BOTONES				*
		#********************************************************
		frame = Frame(self.main_frame, width='900', height='700', bg='#F9F9F9', relief=GROOVE, borderwidth=2)

		button_anterior = Button(frame, width='33', height='30', relief=GROOVE, borderwidth=0)
		button_anterior.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)

		button_siguiente = Button(frame, width='33', height='30', relief=GROOVE, borderwidth=0)
		button_siguiente.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)

		button_search = Button(frame, text=' Buscar paquete', font=('tahoma', 15), bg='#F9F9F9', width='390', height='90', highlightthickness=0, borderwidth=2)
		button_search.config(anchor=W)  #posicionamos el texto a la izquierda
		button_search.config(fg='#48C2FA', activeforeground='#48C2FA')

		button_create = Button(frame, text=' Registrar nuevo paquete', font=('tahoma', 15), bg='#F9F9F9', width='390', height='90', highlightthickness=0, borderwidth=2)
		button_create.config(anchor=W)  #posicionamos el texto a la izquierda
		button_create.config(fg='#48C2FA', activeforeground='#48C2FA')

		#********************************************************
		#			AGREGAMOS ICONOS A LOS BOTONES				*
		#********************************************************
		button_anterior.config(image=self.imagenes['back_not_available_icon'], compound=CENTER)
		if len(self.pila_siguiente) == 0:
			button_siguiente.config(image=self.imagenes['next_not_available_icon'], compound=CENTER)
		else:
			button_siguiente.config(image=self.imagenes['next_available_icon'], compound=CENTER)

		button_search.config(image=self.imagenes['lupa_icon'], compound=LEFT)
		button_create.config(image=self.imagenes['lupa_icon'], compound=LEFT)

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************
		button_search.config(command=lambda:self.view_buscar_paquete(True))
		button_siguiente.config(command=lambda:self.pop_pila_siguiente())
		#button_create.config(command=lambda:self.view_crear_paquete(True))
		button_create.config(command=lambda:self.controller.crear_paquete(True))

		#********************************************************
		#				PACK A TODOS LOS BOTONES				*
		#********************************************************
		#button_search.pack(side='left', padx=20, pady=20, anchor=NW)
		#button_create.pack(side='right', padx=100, pady=20, anchor=NE)
		button_anterior.place(relx=0.025, rely=0.00155)
		button_siguiente.place(relx=0.08, rely=0)
		button_create.place(relx=0.028, rely=0.06, anchor=NW)
		button_search.place(relx=0.978,rely=0.06, anchor=NE)
		frame.pack(padx=20, pady=50, anchor=NE)
		frame.pack_propagate(0)

		self.switch_frame(frame)

	def view_buscar_paquete(self, next_back_starting):
		self.set_button_bold('paquetes')
		self.anterior = 'paquetes'

		#DEFINIMOS EL FRAME 
		frame = Frame(self.main_frame, width='900', height='700', bg='#F9F9F9', relief=GROOVE, borderwidth=0)

		#almacemamos los frame en una pila para los botones de 'anterior y siguiente'
		self.add_pila_anterior(View.VIEW_PAQUETES_COD)

		if next_back_starting:
			#declaramos el un string que alamacena el contenido ingresado
			self.content_entry = StringVar()
			self.radio_variable = StringVar()
			self.radio_variable.set('ninguno')
			self.filtro_anho_value = None
			self.filtro_tipo_value = None
			self.filtro_sub_tipo_value = None
			#result es una lista que almacena todos los paquetes como resultado de la busqueda
			#RESETEAMOS LA LISTA DE RESULTADOS EN CASO DE ENTRAR POR PRIMERA VEZ A BUSCAR PAQUETE
			self.result_busqueda_paquete = []

		#********************************************************
		#				CREAMOS TODOS LOS BOTONES				*
		#********************************************************
		button_anterior = Button(frame, width='33', height='30', relief=GROOVE, borderwidth=0)
		button_anterior.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)

		button_siguiente = Button(frame, width='33', height='30', relief=GROOVE, borderwidth=0)
		button_siguiente.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)

		#********************************************************
		#			AGREGAMOS ICONOS A LOS BOTONES				*
		#********************************************************
		button_anterior.config(image=self.imagenes['back_available_icon'], compound=CENTER)
		if len(self.pila_siguiente) == 0:
			button_siguiente.config(image=self.imagenes['next_not_available_icon'], compound=CENTER)
		else:
			button_siguiente.config(image=self.imagenes['next_available_icon'], compound=CENTER)
		#********************************************************

		label_nombre_paquete = Label(frame, text='Nombre/Destino:', font=('tahoma', 15), width=14, height=1, bg='#F9F9F9')
		label_nombre_paquete.config(fg='#48C2FA')
		#declaramos una entreada para ingresar los datos
		entry = Entry(frame, width='15', font=('tahoma', 15), textvariable=self.content_entry)
		#insertamos RADIO BUTTON para la busqueda por vigencia
		label_radio_button = Label(frame, text='Vigente', font=('tahoma', 15), width=7, height=3, relief=GROOVE, borderwidth=0)
		label_radio_button.config(bg='#F9F9F9', fg='#48C2FA')

		radio_button_si = Radiobutton(frame, text='Si', font=('tahoma', 15), variable=self.radio_variable, value='si', width=2, height=2)
		radio_button_si.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)
		radio_button_no = Radiobutton(frame, text='No', font=('tahoma', 15), variable=self.radio_variable, value='no', width=2, height=2)
		radio_button_no.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)
		radio_button_ninguno = Radiobutton(frame, text='Ninguno', font=('tahoma', 15), variable=self.radio_variable, value='ninguno', width=8, height=2)
		radio_button_ninguno.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)

		#insertamos un COMBOBOX para la busqueda por anho
		label_anho = Label(frame, text='Año', font=('tahoma', 15), width=4, height=2, relief=GROOVE, borderwidth=0)
		label_anho.config(bg='#F9F9F9', fg='#48C2FA', highlightthickness=0)

		lista_anhos = self.controller.generar_lista_anhos()
		self.combobox_anhos = ttk.Combobox(frame, values=lista_anhos)
		#seteamos el valor inicial de la busqueda por anho en caso de que se haya sellecionado algun valor
		#y que se haya se haya sellecionado los botones de next o back
		if self.filtro_anho_value != None:
			self.combobox_anhos.set(self.filtro_anho_value)

		self.combobox_anhos.config(state='readonly', font=(15), width='7', height='6', background='#F9F9F9')

		#insertamos un MENUBUTTON para la busqueda por tipo
		label_tipo_paquete = Label(frame, text='Tipo', font=('tahoma', 15), width='4', height='2', relief=GROOVE, borderwidth=0)
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
		self.next_back_starting_aux = next_back_starting

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************
		button_anterior.config(command=lambda:self.pop_pila_anterior(View.VIEW_BUSCAR_PAQUETE))
		button_siguiente.config(command=lambda:self.pop_pila_siguiente())
		#detectamos los cambios cada vez que se escribe algo
		self.content_entry.trace("w", self.buscar_paquete_por_nombre)
		radio_button_si.config(command=lambda:self.buscar_paquete_por_vigencia(self.radio_variable.get()))
		radio_button_no.config(command=lambda:self.buscar_paquete_por_vigencia(self.radio_variable.get()))
		radio_button_ninguno.config(command=lambda:self.buscar_paquete_por_vigencia(self.radio_variable.get()))
		self.combobox_anhos.bind("<<ComboboxSelected>>", self.buscar_paquete_por_anho)
		self.combobox_tipos.bind("<<ComboboxSelected>>", self.buscar_paquete_por_tipo)
		self.combobox_sub_tipos.bind("<<ComboboxSelected>>", self.buscar_paquete_por_sub_tipo)

		#********************************************************
		#				PACK A TODOS LOS BOTONES				*
		#********************************************************
		button_anterior.place(relx=0.025, rely=0.001)
		button_siguiente.place(relx=0.08, rely=0)
		label_nombre_paquete.pack(side='left', padx=20, pady=42, anchor=NW)
		entry.pack(pady=40, anchor=NW)
		label_radio_button.place(relx=0.5, rely=0.027)
		radio_button_si.place(relx=0.6, rely=0.042)
		radio_button_no.place(relx=0.7, rely=0.042)
		radio_button_ninguno.place(relx=0.8, rely=0.042)
		label_anho.place(relx=0.025, rely=0.15)
		self.combobox_anhos.place(relx=0.1, rely=0.165)
		label_tipo_paquete.place(relx=0.25, rely=0.145)
		self.combobox_tipos.place(relx=0.33, rely=0.165)
		self.combobox_sub_tipos.place(relx=0.46, rely=0.165)
		frame.pack(padx=20, pady=20, anchor=NE)
		frame.pack_propagate(0)

		#REPONEMOS EL ESTADO DE LA BUSQUEDA EN CASO DE SE VUELVA ATRAS O ADELANTE CON LOS BOTONES
		if next_back_starting == False:
			self.show_result_busqueda_paquete()

		self.switch_frame(frame)

	def buscar_paquete_por_nombre(self, *args):
		self.result_busqueda_paquete = self.controller.buscar_paquete(content1=self.content_entry.get(), content2=self.radio_variable.get(),
									content3=self.combobox_anhos.get(), content4=self.combobox_tipos.get(), content5=self.combobox_sub_tipos.get())
		self.show_result_busqueda_paquete()

	def buscar_paquete_por_vigencia(self, radio_variable):
		self.result_busqueda_paquete = self.controller.buscar_paquete(content1=self.content_entry.get(), content2=radio_variable,
									content3=self.combobox_anhos.get(), content4=self.combobox_tipos.get(), content5=self.combobox_sub_tipos.get())
		self.show_result_busqueda_paquete()

	def buscar_paquete_por_anho(self, *args):
		self.filtro_anho_value = self.combobox_anhos.get()
		self.result_busqueda_paquete = self.controller.buscar_paquete(content1=self.content_entry.get(), content2=self.radio_variable.get(),
									content3=self.combobox_anhos.get(), content4=self.combobox_tipos.get(), content5=self.combobox_sub_tipos.get())
		self.show_result_busqueda_paquete()

	def buscar_paquete_por_tipo(self, *args):
		self.filtro_tipo_value = self.combobox_tipos.get()
		self.result_busqueda_paquete = self.controller.buscar_paquete(content1=self.content_entry.get(), content2=self.radio_variable.get(),
									content3=self.combobox_anhos.get(), content4=self.combobox_tipos.get(), content5=self.combobox_sub_tipos.get())
		self.show_result_busqueda_paquete()

	def buscar_paquete_por_sub_tipo(self, *args):
		self.filtro_sub_tipo_value = self.combobox_sub_tipos.get()
		self.result_busqueda_paquete = self.controller.buscar_paquete(content1=self.content_entry.get(), content2=self.radio_variable.get(),
									content3=self.combobox_anhos.get(), content4=self.combobox_tipos.get(), content5=self.combobox_sub_tipos.get())
		self.show_result_busqueda_paquete()

	def update_buscar_paquete(self):
		self.filtro_anho_value = self.combobox_anhos.get()
		self.filtro_tipo_value = self.combobox_tipos.get()
		self.filtro_sub_tipo_value = self.combobox_sub_tipos.get()
		#print('content nombre: ' + self.content_entry.get())
		self.result_busqueda_paquete = self.controller.buscar_paquete(content1=self.content_entry.get(), content2=self.radio_variable.get(),
									content3=self.combobox_anhos.get(), content4=self.combobox_tipos.get(), content5=self.combobox_sub_tipos.get())
		self.show_result_busqueda_paquete()

	def on_frame_configure(self, event=None):
	    self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def show_result_busqueda_paquete(self):
		paquete_view = None

		#eliminamos los resultados anteriores a la busqueda actual (si elminamos la lista anterior tambien se elimina la lista actual, por ref)
		#if self.next_back_starting_aux == False and len(self.view_result_busqueda_paquete) != 0:
		if len(self.view_result_busqueda_paquete) != 0:
			f = 0
			for paquete_view in self.view_result_busqueda_paquete:
				#print('index before destroy: ' + str(paquete_view[f][1]))
				#paquete_view[f][0].destroy()
				paquete_view.destroy()
				f += 1

			self.view_result_busqueda_paquete = []

		#aplicamos los nuevos resultados de la busqueda
		paquete_view = None
		#print(str(len(self.result_busqueda_paquete[0])))
		if len(self.result_busqueda_paquete[0]) != 0:
			pos_result_busqueda = -1
			aux = -1
			for paquete in self.result_busqueda_paquete[0]:
				pos_result_busqueda += 1
				aux += 1

				paquete_view = Frame(self.frame_result_aux, bg='#F9F9F9', width='770', height='150', relief=GROOVE, borderwidth=0)
				paquete_view.pack(padx=10, pady=5)


				#********************************************************
				#	CREAMOS UNA ETIQUETA Y LE COLOCAMOS UN ICONO		*
				#********************************************************
				'''
				label_logo = Label(paquete_view, width=225, height=142, relief=GROOVE, borderwidth=1)
				label_logo.config(bg='#F9F9F9')
				logo = PhotoImage(file='imagenes/logo.png')
				label_logo.config(image=logo)
				label_logo.photo = logo
				label_logo.place(relx=0.01, rely=0.02)
				'''
				
				#falta corregir aqui
				#para agregar dinamicamente las imagenes
				img = Image.open('imagenes/logo.png')
				img = img.resize((190,142), Image.ANTIALIAS)
				logo = ImageTk.PhotoImage(img)
				
				label_logo = Label(paquete_view, width=225, height=142, relief=GROOVE, borderwidth=1)
				label_logo.config(bg='#F9F9F9')
				label_logo.config(image=logo)
				label_logo.photo = logo
				label_logo.place(relx=0.01, rely=0.02)

				#lab_im = Label(image=my_image)
				#lab_im.pack()
				
				

				paquete_name_view = Label(paquete_view, text=paquete.get_nombre(), width='20', height='1', relief=GROOVE, borderwidth=0)
				paquete_name_view.config(font=('tahoma', 15, 'bold'), bg='#F9F9F9', fg='#343535', activeforeground='#343535', anchor=W) #posicionamos el texto a la izquierda
				paquete_name_view.place(relx=0.315, rely=0.05)

				#fecha view
				texto = ''
				date = paquete.get_fecha_de_viaje()
				if date!= None:
					if date.day < 10:
						texto = '0'

					texto = texto + str(date.day) + '/'

					if date.month < 10:
						texto = texto + '0'

					texto = texto + str(date.month) + '/' + str(date.year)
				else:
					texto = '-- / -- / --'

				paquete_fecha_de_viaje_view = Button(paquete_view, text=texto, width='21', height='1', relief=GROOVE, borderwidth=0)
				paquete_fecha_de_viaje_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
				paquete_fecha_de_viaje_view.place(relx=0.3, rely=0.25)

				#vigente view
				texto = 'Vigente'
				if paquete.get_esta_vigente() == False:
					texto = 'No vigente'

				paquete_fecha_de_viaje_view = Button(paquete_view, text=texto, width='21', height='1', relief=GROOVE, borderwidth=0)
				paquete_fecha_de_viaje_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
				paquete_fecha_de_viaje_view.place(relx=0.3, rely=0.50)

				texto = 'Tipo: ' + paquete.TRASLADO
				paquete_fecha_de_viaje_view = Button(paquete_view, text=texto, width='21', height='1', relief=GROOVE, borderwidth=0)
				paquete_fecha_de_viaje_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
				paquete_fecha_de_viaje_view.place(relx=0.3, rely=0.75)

				#SEGUNDA CULUMNA
				#precio view
				#agregamos los puntos al precio, ej: 3000000 ---> 3.000.000Gs
				texto = ''
				#precio_texto = str(paquete.get_precio())
				if paquete.si_pre_venta():
					precio_texto = str(paquete.get_precio_pre_venta())
				else:
					precio_texto = str(paquete.get_precio())

				j = 1
				if len(precio_texto) > 3:
					for i in range(len(precio_texto) - 1, -1, -1):
						texto = precio_texto[i] + texto
						if j % 3 == 0 and i != 0:
							texto = '.' + texto

						j += 1
				else:
					texto = precio_texto

				if paquete.get_precio() < 100000: #significa que el precio esta en dolares, ya que en guaranies se considera 5 digitos como minimo
					texto = 'Precio: ' + texto + '$'
				else:
					texto = 'Precio: ' + texto + 'Gs.'

				paquete_precio_view = Button(paquete_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
				paquete_precio_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
				paquete_precio_view.place(relx=0.7, rely=0)

				#pre venta view
				if paquete.si_pre_venta():
					texto = 'Pre venta: si'
				else:
					texto = 'Pre venta: no'

				paquete_pre_venta_view = Button(paquete_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
				paquete_pre_venta_view.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
				paquete_pre_venta_view.place(relx=0.7, rely=0.25)

				#lugares disponibles view
				texto = 'Lugares disponible: '
				lugares_disponibles = paquete.get_lugares_disponibles()
				color = '#2F3030'
				if lugares_disponibles > 0:
					texto = texto + str(lugares_disponibles)
				elif lugares_disponibles == 0:
					texto = 'SOLD OUT'
					color = '#E60700'
				#elif paquete.get_esta_vigente() is False:
				#	texto = 'No disponible'
				else:
					texto = texto + '--'

				#print('esta vigente: ' + str(paquete.get_esta_vigente()))

				paquete_pre_venta_view = Button(paquete_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
				paquete_pre_venta_view.config(font=('tahoma', 13), bg='#F9F9F9', fg=color, activeforeground=color, highlightthickness=0, anchor=W)
				paquete_pre_venta_view.place(relx=0.7, rely=0.5)

				pos_paquete = self.result_busqueda_paquete[1][aux]
				#detalles view
				texto = 'Ver detalles      >'
				paquete_detalles_view = Button(paquete_view, text=texto, width='18', height='1', relief=GROOVE, borderwidth=0)
				paquete_detalles_view.config(font=('tahoma', 13), bg='#27A221', fg='#FFFFFF', activeforeground='#FFFFFF', activebackground='#20801B', highlightthickness=0, anchor=W)
				paquete_detalles_view.place(relx=0.7, rely=0.75)
				paquete_detalles_view.config(command=lambda paquete=paquete, pos_paquete=pos_paquete,
						pos_result_busqueda=pos_result_busqueda:self.view_paquete_detalles(paquete, pos_paquete, pos_result_busqueda))
				#print(paquete_name_view.config("text")[-1])
				#print(paquete_detalles_view.config("text")[-1])

				self.view_result_busqueda_paquete.append(paquete_view)

	def view_paquete_detalles(self, paquete, pos_paquete, pos_result_busqueda):
		print('viendo detalles')
		self.parent_detalles = Toplevel(self.parent, bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		self.parent_detalles.title('Paquete Detalles')
		self.parent_detalles.geometry('1000x800+450+100')
		self.parent_detalles.resizable(width=False, height=False)

		frame_detalles = Frame(self.parent_detalles, width='1000', height='900', bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		frame_detalles.pack()
		frame_detalles.pack_propagate(0)
		paquete_name_label = Label(frame_detalles, text=paquete.get_nombre(), width='20', height='2', relief=GROOVE, borderwidth=0)
		paquete_name_label.config(font=('tahoma', 25, 'bold'), bg='#F9F9F9', fg='#48C2FA') #posicionamos el texto a la izquierda
		paquete_name_label.pack()

		#fecha view
		fecha_label = Label(frame_detalles, text='Fecha:', width='6', height='1', relief=GROOVE, borderwidth=0)
		fecha_label.config(font=('tahoma', 14, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		fecha_label.place(relx=0.02, rely=0.11)

		texto = ''
		date = paquete.get_fecha_de_viaje()
		if date!= None:
			if date.day < 10:
				texto = '0'

			texto = texto + str(date.day) + '/'

			if date.month < 10:
				texto = texto + '0'

			texto = texto + str(date.month) + '/' + str(date.year)
		else:
			texto = '-- / -- / --'

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

		texto = ''
		#precio_texto = str(paquete.get_precio())
		if paquete.si_pre_venta():
			precio_texto = str(paquete.get_precio_pre_venta())
		else:
			precio_texto = str(paquete.get_precio())

		j = 1
		if len(precio_texto) > 3:
			for i in range(len(precio_texto) -1, -1, -1):
				texto = precio_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = precio_texto

		if paquete.get_precio() < 100000: #significa que el precio esta en dolares, ya que en guaranies se considera 5 digitos como minimo
			texto = texto + '$'
		else:
			texto = texto + 'Gs.'

		precio_value_label = Label(frame_detalles, text=texto, width='12', height='1', relief=GROOVE, borderwidth=0)
		precio_value_label.config(font=('tahoma', 14), bg='#F9F9F9', fg='#2F3030', anchor=W)
		precio_value_label.place(relx=0.435, rely=0.11)

		#senha view
		#agregamos los puntos al precio, ej: 3000000 ---> 3.000.000Gs
		senha_label = Label(frame_detalles, text='Seña:', width='6', height='1', relief=GROOVE, borderwidth=0)
		senha_label.config(font=('tahoma', 14, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		senha_label.place(relx=0.35, rely=0.155)

		texto = ''
		senha_texto = str(paquete.get_senha())
		if paquete.si_pre_venta():
			senha_texto = str(paquete.get_senha_pre_venta())
		else:
			senha_texto = str(paquete.get_senha())

		j = 1
		if len(senha_texto) > 3:
			for i in range(len(senha_texto) - 1, -1, -1):
				texto = senha_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = senha_texto

		if paquete.get_senha() < 100000: #significa que el precio esta en dolares, ya que en guaranies se considera 5 digitos como minimo
			texto = texto + '$'
		else:
			texto = texto + 'Gs.'

		senha_value_label = Label(frame_detalles, text=texto, width='12', height='1', relief=GROOVE, borderwidth=0)
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
		precio_detalles_button.config(font=('tahoma', 13), bg='#27A221', fg='#FFFFFF', activeforeground='#FFFFFF', activebackground='#20801B', highlightthickness=0, anchor=W)
		if paquete.si_pre_venta():
			precio_detalles_button.config(bg='#27A221', activebackground='#20801B')
			precio_detalles_button.config(command=lambda:self.view_precio_detalles(paquete.get_precio(), paquete.get_senha(), paquete.get_pre_venta()))
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
		max_cantidad_pasajeros_label = Label(frame_detalles, text='Max de pasajeros:', width='15', height='1', relief=GROOVE, borderwidth=0)
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
		salir_button.config(command=lambda:self.widget_destroy(self.parent_detalles))
		editar_button.config(command=lambda:self.controller.editar_paquete(frame_detalles, paquete, pos_paquete, pos_result_busqueda))
		#editar_button.config(command=lambda:self.widget_destroy(frame_detalles))

	def view_precio_detalles(self, precio, senha, pre_venta):
		print('viendo precio en detalles....')
		precio_parent = Toplevel(self.parent, bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		precio_parent.title('Precio Detalles')
		#frame.tittle('Pre Venta')
		precio_parent.geometry('600x400+650+150')
		precio_parent.resizable(width=False, height=False)

		#anhadimos un separador
		separator_top = ttk.Separator(precio_parent, orient=HORIZONTAL)
		separator_top.pack(side=TOP, fill=X, padx=30, pady=15)

		#view detalles precio con pre venta
		label = Label(precio_parent, text='Precio del paquete', width='18', height='1', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 10), bg='#F9F9F9') #posicionamos el texto a la izquierda
		label.place(relx=0.38, rely=0.01)

		#view precio
		label = Label(precio_parent, text='Precio:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.07)

		texto = ''
		precio_texto = str(precio)

		j = 1
		if len(precio_texto) > 3:
			for i in range(len(precio_texto) -1, -1, -1):
				texto = precio_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = precio_texto

		if precio < 100000: #significa que el precio esta en dolares, ya que en guaranies se considera 5 digitos como minimo
			texto = texto + '$'
		else:
			texto = texto + 'Gs.'

		label = Label(precio_parent, text=texto, width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13), bg='#F9F9F9', anchor=W)
		label.place(relx=0.25, rely=0.07)

		#view senha
		label = Label(precio_parent, text='Seña:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.19)

		texto = ''
		senha_texto = str(senha)

		j = 1
		if len(senha_texto) > 3:
			for i in range(len(senha_texto) -1, -1, -1):
				texto = senha_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = senha_texto

		if senha < 100000: #significa que el precio esta en dolares, ya que en guaranies se considera 5 digitos como minimo
			texto = texto + '$'
		else:
			texto = texto + 'Gs.'

		label = Label(precio_parent, text=texto, width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13), bg='#F9F9F9', anchor=W)
		label.place(relx=0.25, rely=0.19)

		#anhadimos un separador
		separator = ttk.Separator(precio_parent, orient=HORIZONTAL)
		separator.pack(side=TOP, fill=X, padx=30, pady=106)

		#view detalles precio con pre venta
		label = Label(precio_parent, text='Precio de pre venta', width='18', height='1', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 10), bg='#F9F9F9') #posicionamos el texto a la izquierda
		label.place(relx=0.38, rely=0.32)

		#view precio
		label = Label(precio_parent, text='Precio', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		label.place(relx=0.02, rely=0.38)

		texto = ''
		precio_texto = str(pre_venta.get_precio())

		j = 1
		if len(precio_texto) > 3:
			for i in range(len(precio_texto) -1, -1, -1):
				texto = precio_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = precio_texto

		if precio < 100000: #significa que el precio esta en dolares, ya que en guaranies se considera 5 digitos como minimo
			texto = texto + '$'
		else:
			texto = texto + 'Gs.'

		label = Label(precio_parent, text=texto, width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13), bg='#F9F9F9', anchor=W)
		label.place(relx=0.25, rely=0.38)

		#view sehna
		label = Label(precio_parent, text='Seña', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		label.place(relx=0.02, rely=0.5)

		texto = ''
		senha_texto = str(pre_venta.get_senha())

		j = 1
		if len(senha_texto) > 3:
			for i in range(len(senha_texto) -1, -1, -1):
				texto = senha_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = senha_texto

		if senha < 100000: #significa que el precio esta en dolares, ya que en guaranies se considera 5 digitos como minimo
			texto = texto + '$'
		else:
			texto = texto + 'Gs.'

		label = Label(precio_parent, text=texto, width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13), bg='#F9F9F9', anchor=W)
		label.place(relx=0.25, rely=0.5)

		#view monto cuota
		label = Label(precio_parent, text='Monto cuota:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		label.place(relx=0.02, rely=0.62)

		texto = ''
		monto_cuota = pre_venta.get_monto_cuota()
		monto_cuota_texto = str(monto_cuota)
		j = 1
		if len(monto_cuota_texto) > 3:
			for i in range(len(monto_cuota_texto) -1, -1, -1):
				texto = monto_cuota_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = monto_cuota_texto

		if monto_cuota < 100000: #significa que el precio esta en dolares, ya que en guaranies se considera 5 digitos como minimo
			texto = texto + '$'
		else:
			texto = texto + 'Gs.'

		label = Label(precio_parent, text=texto, width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13), bg='#F9F9F9', anchor=W)
		label.place(relx=0.25, rely=0.62)

		#view cantidad de cuotas
		label = Label(precio_parent, text='Cant cuotas:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		label.place(relx=0.02, rely=0.74)

		label = Label(precio_parent, text=pre_venta.get_cantidad_cuotas(), width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13), bg='#F9F9F9', anchor=W)
		label.place(relx=0.25, rely=0.74)

		#view fecha inicio
		label = Label(precio_parent, text='Fecha inicio:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.5, rely=0.38)

		date_texto = ''
		date = pre_venta.get_fecha_inicio()
		if date!= None:
			if date.day < 10:
				date_texto = '0'

			date_texto = date_texto + str(date.day) + '/'

			if date.month < 10:
				date_texto = date_texto + '0'

			date_texto = date_texto + str(date.month) + '/' + str(date.year)
		else:
			date_texto = '-- / -- / --'

		button_fecha_inicio = Label(precio_parent, text=date_texto, width='11', height='2', relief=GROOVE, borderwidth=0)
		button_fecha_inicio.config(font=('tahoma', 13), bg='#F9F9F9', anchor=W)
		button_fecha_inicio.place(relx=0.73, rely=0.38)

		#view fecha fin
		label = Label(precio_parent, text='Fecha fin:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.5, rely=0.5)

		date_texto = ''
		date = pre_venta.get_fecha_fin()
		if date!= None:
			if date.day < 10:
				date_texto = '0'

			date_texto = date_texto + str(date.day) + '/'

			if date.month < 10:
				date_texto = date_texto + '0'

			date_texto = date_texto + str(date.month) + '/' + str(date.year)
		else:
			date_texto = '-- / -- / --'

		button_fecha_fin = Label(precio_parent, text=date_texto, width='11', height='2', relief=GROOVE, borderwidth=0)
		button_fecha_fin.config(font=('tahoma', 13), bg='#F9F9F9', anchor=W)
		button_fecha_fin.place(relx=0.73, rely=0.5)

		#view ok
		ok_button = Button(precio_parent, text='OK', width=110, height=30, relief=GROOVE, borderwidth=0)
		ok_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		ok_button.config(image=self.imagenes['ok_icon'], compound=LEFT)
		ok_button.place(relx=0.39, rely=0.85)
		ok_button.config(command=lambda:self.widget_destroy(precio_parent))

	def view_agregar_editar_pre_venta(self):
		print('agregando/Editando pre venta...')
		self.frame_pre_venta = Toplevel(self.parent, bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		self.frame_pre_venta.title('Pre Venta')
		#frame.tittle('Pre Venta')
		self.frame_pre_venta.geometry('600x400+650+150')
		self.frame_pre_venta.resizable(width=False, height=False)

		#view precio
		label = Label(self.frame_pre_venta, text='Precio:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.05)
		#label.grid(row=0, column=1, padx=10, pady=20)

		self.price_pre_venta_content_entry = StringVar()
		self.price_pre_venta_content_entry.set('')
		self.price_pre_venta_value = None

		if self.pre_venta:
			self.price_pre_venta_value = self.pre_venta.get_precio()
			self.price_pre_venta_content_entry.set(self.pre_venta.get_precio())
			precio_texto = str(self.pre_venta.get_precio())

			texto = ''
			j = 1
			if len(precio_texto) > 3:
				for i in range(len(precio_texto) -1, -1, -1):
					texto = precio_texto[i] + texto
					if j % 3 == 0 and i != 0:
						texto = '.' + texto

					j += 1
			else:
				texto = precio_texto

			self.price_pre_venta_content_entry.set(texto)

		price_entry = Entry(self.frame_pre_venta, width='10', font=('tahoma', 13), textvariable=self.price_pre_venta_content_entry)
		price_entry.place(relx=0.25, rely=0.075)

		#view senha
		label = Label(self.frame_pre_venta, text='Seña:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.176)

		self.senha_pre_venta_content_entry = StringVar()
		self.senha_pre_venta_content_entry.set('')
		self.senha_pre_venta_value = None

		if self.pre_venta:
			self.senha_pre_venta_value = self.pre_venta.get_senha()
			self.senha_pre_venta_content_entry.set(self.pre_venta.get_senha())
			senha_texto = str(self.pre_venta.get_senha())

			texto = ''
			j = 1
			if len(senha_texto) > 3:
				for i in range(len(senha_texto) -1, -1, -1):
					texto = senha_texto[i] + texto
					if j % 3 == 0 and i != 0:
						texto = '.' + texto

					j += 1
			else:
				texto = senha_texto

			self.senha_pre_venta_content_entry.set(texto)
		#print('senha: {}'.format(self.senha_content_entry.get()))
		#print('A VER QUE ONDA...')

		senha_entry = Entry(self.frame_pre_venta, width='10', font=('tahoma', 13), textvariable=self.senha_pre_venta_content_entry)
		senha_entry.place(relx=0.25, rely=0.2)

		#view monto cuota
		label = Label(self.frame_pre_venta, text='Monto cuota:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.301)

		self.monto_cuota_content_entry = StringVar()
		self.monto_cuota_content_entry.set('')
		self.monto_cuota_value = None

		if self.pre_venta:
			self.monto_cuota_content_entry.set(self.pre_venta.get_monto_cuota())
			self.monto_cuota_value = self.pre_venta.get_monto_cuota()
			monto_cuota_texto = str(self.pre_venta.get_monto_cuota())

			texto = ''
			j = 1
			if len(monto_cuota_texto) > 3:
				for i in range(len(monto_cuota_texto) -1, -1, -1):
					texto = monto_cuota_texto[i] + texto
					if j % 3 == 0 and i != 0:
						texto = '.' + texto

					j += 1
			else:
				texto = monto_cuota_texto

			self.monto_cuota_content_entry.set(texto)

		monto_cuota_entry = Entry(self.frame_pre_venta, width='10', font=('tahoma', 13), textvariable=self.monto_cuota_content_entry)
		monto_cuota_entry.place(relx=0.25, rely=0.325)

		#view cantidad de cuotas
		label = Label(self.frame_pre_venta, text='Cant cuotas:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.425)

		cant_cuota_content_entry = StringVar()
		cant_cuota_content_entry.set('')

		if self.pre_venta:
			cant_cuota_content_entry.set(self.pre_venta.get_cantidad_cuotas())
		cant_cuota_entry = Entry(self.frame_pre_venta, width='10', font=('tahoma', 13), textvariable=cant_cuota_content_entry)
		cant_cuota_entry.place(relx=0.25, rely=0.448)

		#view fecha inicio
		label = Label(self.frame_pre_venta, text='Fecha inicio:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.5, rely=0.05)

		content_button_fecha_inicio = StringVar()

		if self.pre_venta:
			date_texto = ''
			date = self.pre_venta.get_fecha_inicio()
			if date!= None:
				if date.day < 10:
					date_texto = '0'

				date_texto = date_texto + str(date.day) + '/'

				if date.month < 10:
					date_texto = date_texto + '0'

				date_texto = date_texto + str(date.month) + '/' + str(date.year)
			else:
				date_texto = '-- / -- / --'
			content_button_fecha_inicio.set(date_texto)
		else:
			content_button_fecha_inicio.set('-- / -- / --')

		if self.pre_venta:
			self.pre_venta_fecha_inicio = self.pre_venta.get_fecha_inicio()
		button_fecha_inicio = Button(self.frame_pre_venta, textvariable=content_button_fecha_inicio, width='8', height='1', relief=GROOVE, borderwidth=0)
		button_fecha_inicio.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
		button_fecha_inicio.place(relx=0.73, rely=0.07)

		#view fecha fin
		label = Label(self.frame_pre_venta, text='Fecha fin:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.5, rely=0.174)

		content_button_fecha_fin = StringVar()
		if self.pre_venta:
			date_texto = ''
			date = self.pre_venta.get_fecha_fin()
			if date!= None:
				if date.day < 10:
					date_texto = '0'

				date_texto = date_texto + str(date.day) + '/'

				if date.month < 10:
					date_texto = date_texto + '0'

				date_texto = date_texto + str(date.month) + '/' + str(date.year)
			else:
				date_texto = '-- / -- / --'
			content_button_fecha_fin.set(date_texto)
		else:
			content_button_fecha_fin.set('-- / -- / --')

		if self.pre_venta:
			self.pre_venta_fecha_fin = self.pre_venta.get_fecha_fin()
		button_fecha_fin = Button(self.frame_pre_venta, textvariable=content_button_fecha_fin, width='8', height='1', relief=GROOVE, borderwidth=0)
		button_fecha_fin.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
		button_fecha_fin.place(relx=0.73, rely=0.195)

		#view ok and cancel
		save_button = Button(self.frame_pre_venta, text='Guardar', width=110, height=30, relief=GROOVE, borderwidth=0)
		save_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		save_button.config(image=self.imagenes['save_icon'], compound=LEFT)
		save_button.place(relx=0.52, rely=0.75)

		cancel_button = Button(self.frame_pre_venta, text='Salir', width=110, height=30, relief=GROOVE, borderwidth=0)
		cancel_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		cancel_button.config(image=self.imagenes['not_ok_icon'], compound=LEFT)
		cancel_button.place(relx=0.28, rely=0.75)

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************
		button_fecha_inicio.config(command=lambda:self.view_calendar(self.frame_pre_venta, content_button_fecha_inicio, 2, 0.55, 0.06))
		button_fecha_fin.config(command=lambda:self.view_calendar(self.frame_pre_venta, content_button_fecha_fin, 3, 0.55, 0.13))
		self.price_pre_venta_content_entry.trace("w", self.update_price_pre_venta_content_entry)
		self.senha_pre_venta_content_entry.trace("w", self.update_senha_pre_venta_content_entry)
		self.monto_cuota_content_entry.trace("w", self.update_monto_cuota_content_entry)
		save_button.config(command=lambda:self.controller.guardar_pre_venta(self.price_pre_venta_value, self.senha_pre_venta_value, self.monto_cuota_value,
				cant_cuota_content_entry.get(), self.pre_venta_fecha_inicio, self.pre_venta_fecha_fin))
		cancel_button.config(command=lambda:self.widget_destroy(self.frame_pre_venta))


	def view_editar_pre_venta(self):
		print('Editando pre venta...')
		self.frame_pre_venta = Toplevel(self.parent, bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		self.frame_pre_venta.title('Pre Venta')
		#frame.tittle('Pre Venta')
		self.frame_pre_venta.geometry('600x400+650+150')
		self.frame_pre_venta.resizable(width=False, height=False)

		#view precio
		label = Label(self.frame_pre_venta, text='Precio:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.05)
		#label.grid(row=0, column=1, padx=10, pady=20)

		self.price_pre_venta_content_entry = StringVar()
		self.price_pre_venta_value = self.pre_venta.get_precio()
		self.price_pre_venta_content_entry.set(self.pre_venta.get_precio())
		precio_texto = str(self.pre_venta.get_precio())

		price_entry = Entry(self.frame_pre_venta, width='10', font=('tahoma', 13), textvariable=self.price_pre_venta_content_entry)
		price_entry.place(relx=0.25, rely=0.075)
		#price_entry.grid(row=0, column=2, padx=-10)

		texto = ''
		j = 1
		if len(precio_texto) > 3:
			for i in range(len(precio_texto) -1, -1, -1):
				texto = precio_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = precio_texto

		self.price_pre_venta_content_entry.set(texto)

		#view senha
		label = Label(self.frame_pre_venta, text='Seña:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.176)

		self.senha_pre_venta_value = self.pre_venta.get_senha()
		self.senha_pre_venta_content_entry = StringVar()
		self.senha_pre_venta_content_entry.set(self.pre_venta.get_senha())
		senha_texto = str(self.pre_venta.get_senha())

		texto = ''
		j = 1
		if len(senha_texto) > 3:
			for i in range(len(senha_texto) -1, -1, -1):
				texto = senha_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = senha_texto

		self.senha_pre_venta_content_entry.set(texto)
		#print('senha: {}'.format(self.senha_content_entry.get()))
		#print('A VER QUE ONDA...')

		senha_entry = Entry(self.frame_pre_venta, width='10', font=('tahoma', 13), textvariable=self.senha_pre_venta_content_entry)
		senha_entry.place(relx=0.25, rely=0.2)

		#view monto cuota
		label = Label(self.frame_pre_venta, text='Monto cuota:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.301)

		self.monto_cuota_content_entry = StringVar()
		self.monto_cuota_content_entry.set(self.pre_venta.get_monto_cuota())
		self.monto_cuota_value = self.pre_venta.get_monto_cuota()
		monto_cuota_texto = str(self.pre_venta.get_monto_cuota())

		texto = ''
		j = 1
		if len(monto_cuota_texto) > 3:
			for i in range(len(monto_cuota_texto) -1, -1, -1):
				texto = monto_cuota_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = monto_cuota_texto

		self.monto_cuota_content_entry.set(texto)

		monto_cuota_entry = Entry(self.frame_pre_venta, width='10', font=('tahoma', 13), textvariable=self.monto_cuota_content_entry)
		monto_cuota_entry.place(relx=0.25, rely=0.325)

		#view cantidad de cuotas
		label = Label(self.frame_pre_venta, text='Cant cuotas:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.425)

		cant_cuota_content_entry = StringVar()
		if self.pre_venta:
			cant_cuota_content_entry.set(self.pre_venta.get_cantidad_cuotas())
		cant_cuota_entry = Entry(self.frame_pre_venta, width='10', font=('tahoma', 13), textvariable=cant_cuota_content_entry)
		cant_cuota_entry.place(relx=0.25, rely=0.448)

		#view fecha inicio
		label = Label(self.frame_pre_venta, text='Fecha inicio:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.5, rely=0.05)

		content_button_fecha_inicio = StringVar()
		if self.pre_venta:
			date_texto = ''
			date = self.pre_venta.get_fecha_inicio()
			if date!= None:
				if date.day < 10:
					date_texto = '0'

				date_texto = date_texto + str(date.day) + '/'

				if date.month < 10:
					date_texto = date_texto + '0'

				date_texto = date_texto + str(date.month) + '/' + str(date.year)
			else:
				date_texto = '-- / -- / --'
			content_button_fecha_inicio.set(date_texto)
		else:
			content_button_fecha_inicio.set('-- / -- / --')

		if self.pre_venta:
			self.pre_venta_fecha_inicio = self.pre_venta.get_fecha_inicio()
		button_fecha_inicio = Button(self.frame_pre_venta, textvariable=content_button_fecha_inicio, width='8', height='1', relief=GROOVE, borderwidth=0)
		button_fecha_inicio.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
		button_fecha_inicio.place(relx=0.73, rely=0.07)

		#view fecha fin
		label = Label(self.frame_pre_venta, text='Fecha fin:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#343535', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.5, rely=0.174)

		content_button_fecha_fin = StringVar()
		if self.pre_venta:
			date_texto = ''
			date = self.pre_venta.get_fecha_fin()
			if date!= None:
				if date.day < 10:
					date_texto = '0'

				date_texto = date_texto + str(date.day) + '/'

				if date.month < 10:
					date_texto = date_texto + '0'

				date_texto = date_texto + str(date.month) + '/' + str(date.year)
			else:
				date_texto = '-- / -- / --'
			content_button_fecha_fin.set(date_texto)
		else:
			content_button_fecha_fin.set('-- / -- / --')

		if self.pre_venta:
			self.pre_venta_fecha_fin = self.pre_venta.get_fecha_fin()
		button_fecha_fin = Button(self.frame_pre_venta, textvariable=content_button_fecha_fin, width='8', height='1', relief=GROOVE, borderwidth=0)
		button_fecha_fin.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
		button_fecha_fin.place(relx=0.73, rely=0.195)

		#view ok and cancel
		save_button = Button(self.frame_pre_venta, text='Guardar', width=110, height=30, relief=GROOVE, borderwidth=0)
		save_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		save_button.config(image=self.imagenes['save_icon'], compound=LEFT)
		save_button.place(relx=0.52, rely=0.75)

		cancel_button = Button(self.frame_pre_venta, text='Salir', width=110, height=30, relief=GROOVE, borderwidth=0)
		cancel_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		cancel_button.config(image=self.imagenes['not_ok_icon'], compound=LEFT)
		cancel_button.place(relx=0.28, rely=0.75)

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************
		button_fecha_inicio.config(command=lambda:self.view_calendar(self.frame_pre_venta, content_button_fecha_inicio, 2, 0.55, 0.06))
		button_fecha_fin.config(command=lambda:self.view_calendar(self.frame_pre_venta, content_button_fecha_fin, 3, 0.55, 0.13))
		self.price_pre_venta_content_entry.trace("w", self.update_price_pre_venta_content_entry)
		self.senha_pre_venta_content_entry.trace("w", self.update_senha_pre_venta_content_entry)
		self.monto_cuota_content_entry.trace("w", self.update_monto_cuota_content_entry)
		save_button.config(command=lambda:self.controller.guardar_pre_venta(self.price_pre_venta_value, self.senha_pre_venta_value, self.monto_cuota_value,
				cant_cuota_content_entry.get(), self.pre_venta_fecha_inicio, self.pre_venta_fecha_fin))
		cancel_button.config(command=lambda:self.widget_destroy(self.frame_pre_venta))

	def add_pila_anterior(self, clave):
		self.pila_anterior.append(clave)

		if len(self.pila_siguiente) != 0:
			self.pila_siguiente = []

	def pop_pila_anterior(self, codigo_actual):
		if len(self.pila_anterior) == 0:
			return

		#si no esta vacia
		codigo = self.pila_anterior.pop()
		self.pila_siguiente.append(codigo_actual)

		if codigo == View.VIEW_PAQUETES_COD:
			self.view_paquetes(False)
		elif codigo == View.VIEW_BUSCAR_PAQUETE:
			self.view_buscar_paquete(False)
		elif codigo == View.VIEW_CREAR_PAQUETE:
			#self.view_crear_paquete(False)
			self.controller.crear_paquete(False)
		elif codigo == View.VIEW_USUARIOS_COD:
			self.controller.registrar_cliente(False)

	def pop_pila_siguiente(self):
		if len(self.pila_siguiente) == 0:
			return

		self.next_back_starting = False

		#si no esta vacia
		codigo = self.pila_siguiente.pop()
		self.pila_anterior.append(codigo)

		if codigo == View.VIEW_BUSCAR_PAQUETE:
			self.view_buscar_paquete(False)
		elif codigo == View.VIEW_CREAR_PAQUETE:
			#self.view_crear_paquete(False)
			self.controller.crear_paquete(False)

	def view_crear_paquete(self, next_back_starting):
		self.set_button_bold('paquetes')
		self.anterior = 'paquetes'

		#DEFINIMOS EL FRAME 
		self.frame_pre_venta = None
		self.frame_crear_paquete = Frame(self.main_frame, width='900', height='700', bg='#F9F9F9', relief=GROOVE, borderwidth=0)

		#almacemamos los frame en una pila para los botones de 'anterior y siguiente'
		self.add_pila_anterior(View.VIEW_PAQUETES_COD)

		#********************************************************
		#				CREAMOS TODOS LOS BOTONES				*
		#********************************************************
		button_anterior = Button(self.frame_crear_paquete, width='33', height='30', relief=GROOVE, borderwidth=0)
		button_anterior.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)

		button_siguiente = Button(self.frame_crear_paquete, width='33', height='30', relief=GROOVE, borderwidth=0)
		button_siguiente.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)

		#********************************************************
		#			AGREGAMOS ICONOS A LOS BOTONES				*
		#********************************************************
		button_anterior.config(image=self.imagenes['back_available_icon'], compound=CENTER)
		if len(self.pila_siguiente) == 0:
			button_siguiente.config(image=self.imagenes['next_not_available_icon'], compound=CENTER)
		else:
			button_siguiente.config(image=self.imagenes['next_available_icon'], compound=CENTER)

		#********************************************************
		#  AGREGAMOS LAS ETIQUETAS CORRESPONDIENTE A LOS DATOS	*
		#********************************************************

		#view nombre paquete
		label = Label(self.frame_crear_paquete, text='Nombre:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.06)

		name_content_entry = StringVar()
		name_entry = Entry(self.frame_crear_paquete, width='25', font=('tahoma', 13), textvariable=name_content_entry)
		name_entry.place(relx=0.17, rely=0.075)

		#view tipo de paquete
		label = Label(self.frame_crear_paquete, text='Tipo:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.132)

		lista_tipos = ['Terrestre', 'Aereo']
		combobox_tipos = ttk.Combobox(self.frame_crear_paquete, values=lista_tipos)
		combobox_tipos.config(state='readonly', font=(13), width='9', height='6', background='#F9F9F9')
		combobox_tipos.place(relx=0.17, rely=0.149)

		lista_sub_tipos = ['Estandar', 'Personalizado']
		combobox_sub_tipos = ttk.Combobox(self.frame_crear_paquete, values=lista_sub_tipos)
		combobox_sub_tipos.config(state='readonly', font=(13), width='12', height='6', background='#F9F9F9')
		combobox_sub_tipos.place(relx=0.3, rely=0.149)

		#view vigente
		label = Label(self.frame_crear_paquete, text='Vigente:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.204)

		lista_vigencia = ['Si', 'No']
		combobox_vigencia = ttk.Combobox(self.frame_crear_paquete, values=lista_vigencia)
		combobox_vigencia.config(state='readonly', font=(13), width='9', height='6', background='#F9F9F9')
		combobox_vigencia.place(relx=0.17, rely=0.221)

		#view fecha
		label = Label(self.frame_crear_paquete, text='Salida/as:', width='11', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.276)

		self.lista_fecha = []
		self.lista_fecha_combobox = []
		self.combobox_add_fecha = ttk.Combobox(self.frame_crear_paquete, values=self.lista_fecha_combobox)
		self.combobox_add_fecha.config(state='readonly', font=(13), width='9', height='6', background='#F9F9F9')
		self.combobox_add_fecha.set('-- / -- / --')
		self.combobox_add_fecha.place(relx=0.17, rely=0.292)

		button_fecha_de_viaje = Button(self.frame_crear_paquete, width='25', height='25', relief=GROOVE, borderwidth=0)
		button_fecha_de_viaje.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
		button_fecha_de_viaje.config(image=self.imagenes['add_icon'])
		button_fecha_de_viaje.place(relx=0.3, rely=0.289)

		#view precio
		label = Label(self.frame_crear_paquete, text='Precio:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.347)

		self.price_content_entry = StringVar()
		self.price_value = None
		price_entry = Entry(self.frame_crear_paquete, width='25', font=('tahoma', 13), textvariable=self.price_content_entry)
		price_entry.place(relx=0.17, rely=0.36)

		#view senha
		label = Label(self.frame_crear_paquete, text='Seña:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.42)

		self.senha_content_entry = StringVar()
		self.senha_value = None
		senha_entry = Entry(self.frame_crear_paquete, width='25', font=('tahoma', 13), textvariable=self.senha_content_entry)
		senha_entry.place(relx=0.17, rely=0.43)

		#incluye view
		label = Label(self.frame_crear_paquete, text='Incluye:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		label.place(relx=0.02, rely=0.492)

		incluye_frame = Frame(self.frame_crear_paquete, width='400', height='200', bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		incluye_frame.place(relx=0.17, rely=0.492)

		scroll = Scrollbar(incluye_frame, orient=VERTICAL)
		scroll.pack(side=RIGHT, fill=Y)

		incluye_content = StringVar()
		incluye_text_widget = Text(incluye_frame, height=7, width=30, relief=GROOVE, borderwidth=0)
		incluye_text_widget.insert(END, '')
		
		incluye_text_widget.config(font=('tahoma', 12), bg='#FFFFFF', fg='#2F3030')
		incluye_text_widget.pack(side=LEFT, fill=Y)

		scroll.config(command=incluye_text_widget.yview)
		incluye_text_widget.config(wrap=WORD, yscrollcommand=scroll.set)

		#view cantidad de pasajeros
		label = Label(self.frame_crear_paquete, text='Cant pasajeros:', width='13', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		label.place(relx=0.56, rely=0.06)

		cant_pasajeros_content_entry = StringVar()
		cant_pasajeros_entry = Entry(self.frame_crear_paquete, width='15', font=('tahoma', 13), textvariable=cant_pasajeros_content_entry)
		cant_pasajeros_entry.place(relx=0.742, rely=0.075)

		#view pre venta
		self.pre_venta = None
		label = Label(self.frame_crear_paquete, text='Pre venta:', width='13', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		label.place(relx=0.56, rely=0.132)

		self.content_pre_venta_button = StringVar()
		self.content_pre_venta_button.set('Agregar')
		pre_venta_button = Button(self.frame_crear_paquete, textvariable=self.content_pre_venta_button, width=10, height=1, relief=GROOVE, borderwidth=0)
		pre_venta_button.config(font=('tahoma', 13), bg='#F9F9F9')
		pre_venta_button.place(relx=0.742, rely=0.139)

		#view ok and cancel
		save_button = Button(self.frame_crear_paquete, text='Guardar', width=110, height=30, relief=GROOVE, borderwidth=0)
		save_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		save_button.config(image=self.imagenes['save_icon'], compound=LEFT)
		save_button.place(relx=0.5, rely=0.85)

		cancel_button = Button(self.frame_crear_paquete, text='Cancelar', width=110, height=30, relief=GROOVE, borderwidth=0)
		cancel_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		cancel_button.config(image=self.imagenes['not_ok_icon'], compound=LEFT)
		cancel_button.place(relx=0.34, rely=0.85)
		#********************************************************

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************
		button_anterior.config(command=lambda:self.pop_pila_anterior(View.VIEW_CREAR_PAQUETE))
		button_siguiente.config(command=lambda:self.pop_pila_siguiente())
		self.price_content_entry.trace("w", self.update_price_content_entry)
		self.senha_content_entry.trace("w", self.update_senha_content_entry)
		button_fecha_de_viaje.config(command=lambda:self.view_calendar(self.frame_crear_paquete, None, 1, 0.17, 0.277))
		pre_venta_button.config(command=lambda:self.controller.agregar_editar_pre_venta())
		save_button.config(command=lambda:self.controller.guardar_paquete(name_content_entry.get(), combobox_tipos.get(), combobox_sub_tipos.get(),
				combobox_vigencia.get(), self.lista_fecha, self.price_value, self.senha_value, incluye_text_widget.get(1.0, END),
				cant_pasajeros_content_entry.get(), self.pre_venta))
		cancel_button.config(command=lambda:self.controller.crear_paquete(True))

		#********************************************************
		#				PACK A TODOS LOS BOTONES				*
		#********************************************************
		button_anterior.place(relx=0.025, rely=0.001)
		button_siguiente.place(relx=0.08, rely=0)
		self.frame_crear_paquete.pack(padx=20, pady=20, anchor=NE)
		self.frame_crear_paquete.pack_propagate(0)

		self.switch_frame(self.frame_crear_paquete)

	def update_price_pre_venta_content_entry(self, *args):
		texto = ''
		precio_texto = self.price_pre_venta_content_entry.get()

		#eliminamos los puntos '.'
		if len(precio_texto) > 3:
			for i in range(len(precio_texto)):
				if precio_texto[i] != '.':
					texto += precio_texto[i]

			precio_texto = texto
			self.price_pre_venta_value = texto
			texto = ''
		else:
			self.price_pre_venta_value = precio_texto

		j = 1
		if len(precio_texto) > 3:
			for i in range(len(precio_texto) -1, -1, -1):
				texto = precio_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = precio_texto

		self.price_pre_venta_content_entry.set(texto)

	def update_senha_pre_venta_content_entry(self, *args):
		texto = ''
		senha_texto = self.senha_pre_venta_content_entry.get()

		#eliminamos los puntos '.'
		if len(senha_texto) > 3:
			for i in range(len(senha_texto)):
				if senha_texto[i] != '.':
					texto += senha_texto[i]

			senha_texto = texto
			self.senha_pre_venta_value = texto
			texto = ''
		else:
			self.senha_pre_venta_value = senha_texto

		j = 1
		if len(senha_texto) > 3:
			for i in range(len(senha_texto) -1, -1, -1):
				texto = senha_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = senha_texto

		self.senha_pre_venta_content_entry.set(texto)

	def update_price_content_entry(self, *args):
		texto = ''
		precio_texto = self.price_content_entry.get()

		#eliminamos los puntos '.'
		if len(precio_texto) > 3:
			for i in range(len(precio_texto)):
				if precio_texto[i] != '.':
					texto += precio_texto[i]

			precio_texto = texto
			self.price_value = texto
			texto = ''
		else:
			self.price_value = precio_texto

		j = 1
		if len(precio_texto) > 3:
			for i in range(len(precio_texto) -1, -1, -1):
				texto = precio_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = precio_texto

		self.price_content_entry.set(texto)

	def update_senha_content_entry(self, *args):
		#self.price_value_int = self.price_content_entry.get()
		texto = ''
		senha_texto = self.senha_content_entry.get()

		#eliminamos los puntos '.'
		if len(senha_texto) > 3:
			for i in range(len(senha_texto)):
				if senha_texto[i] != '.':
					texto += senha_texto[i]

			senha_texto = texto
			self.senha_value = texto
			texto = ''
		else:
			self.senha_value = senha_texto

		j = 1
		if len(senha_texto) > 3:
			for i in range(len(senha_texto) -1, -1, -1):
				texto = senha_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = senha_texto

		self.senha_content_entry.set(texto)

	def update_monto_cuota_content_entry(self, *args):
		#self.price_value_int = self.price_content_entry.get()
		texto = ''
		monto_cuota_texto = self.monto_cuota_content_entry.get()

		#eliminamos los puntos '.'
		if len(monto_cuota_texto) > 3:
			for i in range(len(monto_cuota_texto)):
				if monto_cuota_texto[i] != '.':
					texto += monto_cuota_texto[i]

			monto_cuota_texto = texto
			self.monto_cuota_value = texto
			texto = ''
		else:
			self.monto_cuota_value = monto_cuota_texto

		j = 1
		if len(monto_cuota_texto) > 3:
			for i in range(len(monto_cuota_texto) -1, -1, -1):
				texto = monto_cuota_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = monto_cuota_texto

		self.monto_cuota_content_entry.set(texto)
	
	def set_value_pre_venta(self, pre_venta):
		self.pre_venta = pre_venta

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

		if self.frame_pre_venta is not None and success:
			self.widget_destroy(self.frame_pre_venta)
			self.frame_pre_venta = None
			self.content_pre_venta_button.set('Disponible')

		ok.config(command=lambda:self.widget_destroy(message))
		ok.pack(pady=10)

	def widget_destroy(self, widget):
		widget.destroy()

	def view_calendar(self, frame, content, cod_fecha, x, y):
		frame_calendar = Frame(frame, bg='#F9F9F9', width='260', height='270', relief=GROOVE, borderwidth=1)
		frame_calendar.place(relx=x, rely=y)
		frame_calendar.pack_propagate(0)

		frame_date = Frame(frame_calendar, bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		frame_date.pack()

		calendario = Calendar(frame_date)
		ok = Button(frame_calendar, width=5, bg='#F9F9F9', text='OK', command=lambda:self.update_button_fecha_de_viaje(frame_calendar, content, calendario, cod_fecha))
		ok.pack(pady=2)

	def update_button_fecha_de_viaje(self, frame_calendar, content, calendario, cod_fecha):
		frame_calendar.destroy()
		date = calendario.get_date_selected()

		if cod_fecha == 1:
			self.fecha_de_viaje = date
		elif cod_fecha == 2:
			self.pre_venta_fecha_inicio = date
		elif cod_fecha == 3:
			self.pre_venta_fecha_fin = date

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

		if cod_fecha == 1:
			self.combobox_add_fecha.destroy()
			self.lista_fecha.append(date)
			self.lista_fecha_combobox.append(day + '/' + month + '/' + str(date.year))
			self.combobox_add_fecha = ttk.Combobox(self.frame_crear_paquete, values=self.lista_fecha_combobox)
			self.combobox_add_fecha.config(state='readonly', font=(13), width='9', height='6', background='#F9F9F9')
			self.combobox_add_fecha.set(day + '/' + month + '/' + str(date.year))
			self.combobox_add_fecha.place(relx=0.17, rely=0.292)
		else:
			content.set(day + '/' + month + '/' + str(date.year))

	def view_usuarios(self, next_back_starting):
		self.set_button_bold('usuarios')
		self.anterior = 'usuarios'

		if next_back_starting:
			self.pila_anterior = []
			self.pila_siguiente = []

		#********************************************************
		#				CREAMOS TODOS LOS BOTONES				*
		#********************************************************
		frame = Frame(self.main_frame, width='900', height='700', bg='#F9F9F9', relief=GROOVE, borderwidth=2)

		button_anterior = Button(frame, width='33', height='30', relief=GROOVE, borderwidth=0)
		button_anterior.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)

		button_siguiente = Button(frame, width='33', height='30', relief=GROOVE, borderwidth=0)
		button_siguiente.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)

		button_create = Button(frame, text=' Registrar nuevo cliente', font=('tahoma', 15), bg='#F9F9F9', width='390', height='90', highlightthickness=0, borderwidth=2)
		button_create.config(anchor=W)  #posicionamos el texto a la izquierda
		button_create.config(fg='#48C2FA', activeforeground='#48C2FA')

		button_search = Button(frame, text=' Buscar cliente', font=('tahoma', 15), bg='#F9F9F9', width='390', height='90', highlightthickness=0, borderwidth=2)
		button_search.config(anchor=W)  #posicionamos el texto a la izquierda
		button_search.config(fg='#48C2FA', activeforeground='#48C2FA')

		#********************************************************
		#			AGREGAMOS ICONOS A LOS BOTONES				*
		#********************************************************
		button_anterior.config(image=self.imagenes['back_not_available_icon'], compound=CENTER)
		if len(self.pila_siguiente) == 0:
			button_siguiente.config(image=self.imagenes['next_not_available_icon'], compound=CENTER)
		else:
			button_siguiente.config(image=self.imagenes['next_available_icon'], compound=CENTER)

		button_search.config(image=self.imagenes['lupa_icon'], compound=LEFT)
		button_create.config(image=self.imagenes['lupa_icon'], compound=LEFT)

		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************
		#button_search.config(command=lambda:self.view_buscar_paquete(True))
		button_siguiente.config(command=lambda:self.pop_pila_siguiente())
		#button_create.config(command=lambda:self.view_crear_paquete(True))
		button_create.config(command=lambda:self.controller.registrar_cliente(True))

		#********************************************************
		#				PACK A TODOS LOS BOTONES				*
		#********************************************************
		#button_search.pack(side='left', padx=20, pady=20, anchor=NW)
		#button_create.pack(side='right', padx=100, pady=20, anchor=NE)
		button_anterior.place(relx=0.025, rely=0.00155)
		button_siguiente.place(relx=0.08, rely=0)
		button_create.place(relx=0.028, rely=0.06, anchor=NW)
		button_search.place(relx=0.978,rely=0.06, anchor=NE)
		frame.pack(padx=20, pady=50, anchor=NE)
		frame.pack_propagate(0)

		self.switch_frame(frame)

	def view_registrar_cliente(self, next_back_starting):
		self.set_button_bold('usuarios')
		self.anterior = 'usuarios'
		#print('wtf')

		#DEFINIMOS EL FRAME 
		frame = Frame(self.main_frame, width='900', height='700', bg='#F9F9F9', relief=GROOVE, borderwidth=2)

		#almacemamos los frame en una pila para los botones de 'anterior y siguiente'
		self.add_pila_anterior(View.VIEW_USUARIOS_COD)

		#********************************************************
		#				CREAMOS TODOS LOS BOTONES				*
		#********************************************************
		button_anterior = Button(frame, width='33', height='30', relief=GROOVE, borderwidth=0)
		button_anterior.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)

		button_siguiente = Button(frame, width='33', height='30', relief=GROOVE, borderwidth=0)
		button_siguiente.config(bg='#F9F9F9', activebackground='#F9F9F9', highlightthickness=0)

		#********************************************************
		#			AGREGAMOS ICONOS A LOS BOTONES				*
		#********************************************************
		button_anterior.config(image=self.imagenes['back_available_icon'], compound=CENTER)
		if len(self.pila_siguiente) == 0:
			button_siguiente.config(image=self.imagenes['next_not_available_icon'], compound=CENTER)
		else:
			button_siguiente.config(image=self.imagenes['next_available_icon'], compound=CENTER)

		#********************************************************
		#  AGREGAMOS LAS ETIQUETAS CORRESPONDIENTE A LOS DATOS	*
		#********************************************************

		#view nombre cliente
		label = Label(frame, text='Nombre:', width='10', height='2', relief=GROOVE, borderwidth=2)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.06)

		name_content_entry = StringVar()
		name_entry = Entry(frame, width='25', font=('tahoma', 13), textvariable=name_content_entry)
		name_entry.place(relx=0.17, rely=0.075)

		#view apellido cliente
		label = Label(frame, text='Apellido:', width='10', height='2', relief=GROOVE, borderwidth=2)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.134)

		apellido_content_entry = StringVar()
		apellido_entry = Entry(frame, width='25', font=('tahoma', 13), textvariable=apellido_content_entry)
		apellido_entry.place(relx=0.17, rely=0.149)

		#view apellido cliente
		label = Label(frame, text='Cedula:', width='10', height='2', relief=GROOVE, borderwidth=2)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.207)

		self.cedula_content_entry = StringVar()
		self.cedula_value = None
		apellido_entry = Entry(frame, width='25', font=('tahoma', 13), textvariable=self.cedula_content_entry)
		apellido_entry.place(relx=0.17, rely=0.223)

		#view fecha de nacimiento cliente
		label = Label(frame, text='Nacimiento:', width='10', height='2', relief=GROOVE, borderwidth=2)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.280)

		content_button_edad = StringVar()
		content_button_edad.set('-- / -- / --')
		self.edad_de_viaje = None
		button_edad_de_viaje = Button(frame, textvariable=content_button_edad, width='8', height='1', relief=GROOVE, borderwidth=0)
		button_edad_de_viaje.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
		button_edad_de_viaje.place(relx=0.17, rely=0.288)

		#view edad cliente
		label = Label(frame, text='Edad:', width='10', height='2', relief=GROOVE, borderwidth=2)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.353)

		'''
		#view vigente
		label = Label(frame, text='Vigente:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.204)

		lista_vigencia = ['Si', 'No']
		combobox_vigencia = ttk.Combobox(frame, values=lista_vigencia)
		combobox_vigencia.config(state='readonly', font=(13), width='9', height='6', background='#F9F9F9')
		combobox_vigencia.place(relx=0.17, rely=0.221)

		#view fecha
		label = Label(frame, text='Fecha:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.276)

		content_button_fecha = StringVar()
		content_button_fecha.set('-- / -- / --')
		self.fecha_de_viaje = None
		button_fecha_de_viaje = Button(frame, textvariable=content_button_fecha, width='8', height='1', relief=GROOVE, borderwidth=0)
		button_fecha_de_viaje.config(font=('tahoma', 13), bg='#F9F9F9', fg='#2F3030', activeforeground='#2F3030', highlightthickness=0, anchor=W)
		button_fecha_de_viaje.place(relx=0.17, rely=0.288)

		#view precio
		label = Label(frame, text='Precio:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.347)

		price_content_entry = StringVar()
		price_entry = Entry(frame, width='25', font=('tahoma', 13), textvariable=price_content_entry)
		price_entry.place(relx=0.17, rely=0.36)

		#view senha
		label = Label(frame, text='Seña:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W) #posicionamos el texto a la izquierda
		label.place(relx=0.02, rely=0.42)

		senha_content_entry = StringVar()
		senha_entry = Entry(frame, width='25', font=('tahoma', 13), textvariable=senha_content_entry)
		senha_entry.place(relx=0.17, rely=0.43)

		#incluye view
		label = Label(frame, text='Incluye:', width='10', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		label.place(relx=0.02, rely=0.492)

		incluye_frame = Frame(frame, width='400', height='200', bg='#F9F9F9', relief=GROOVE, borderwidth=0)
		incluye_frame.place(relx=0.17, rely=0.492)

		scroll = Scrollbar(incluye_frame, orient=VERTICAL)
		scroll.pack(side=RIGHT, fill=Y)

		incluye_content = StringVar()
		incluye_text_widget = Text(incluye_frame, height=7, width=30, relief=GROOVE, borderwidth=0)
		incluye_text_widget.insert(END, '')
		
		incluye_text_widget.config(font=('tahoma', 12), bg='#FFFFFF', fg='#2F3030')
		incluye_text_widget.pack(side=LEFT, fill=Y)

		scroll.config(command=incluye_text_widget.yview)
		incluye_text_widget.config(wrap=WORD, yscrollcommand=scroll.set)

		#view cantidad de pasajeros
		label = Label(frame, text='Cant pasajeros:', width='13', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		label.place(relx=0.56, rely=0.06)

		cant_pasajeros_content_entry = StringVar()
		cant_pasajeros_entry = Entry(frame, width='15', font=('tahoma', 13), textvariable=cant_pasajeros_content_entry)
		cant_pasajeros_entry.place(relx=0.742, rely=0.075)

		#view pre venta
		self.pre_venta = None
		label = Label(frame, text='Pre venta:', width='13', height='2', relief=GROOVE, borderwidth=0)
		label.config(font=('tahoma', 13, 'bold'), bg='#F9F9F9', fg='#48C2FA', anchor=W)
		label.place(relx=0.56, rely=0.132)

		self.content_pre_venta_button = StringVar()
		self.content_pre_venta_button.set('Agregar')
		pre_venta_button = Button(frame, textvariable=self.content_pre_venta_button, width=10, height=1, relief=GROOVE, borderwidth=0)
		pre_venta_button.config(font=('tahoma', 13), bg='#F9F9F9')
		pre_venta_button.place(relx=0.742, rely=0.139)

		#view ok and cancel
		save_button = Button(frame, text='Guardar', width=110, height=30, relief=GROOVE, borderwidth=0)
		save_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		save_button.config(image=self.imagenes['save_icon'], compound=LEFT)
		save_button.place(relx=0.5, rely=0.85)

		cancel_button = Button(frame, text='Cancelar', width=110, height=30, relief=GROOVE, borderwidth=0)
		cancel_button.config(font=('tahoma', 13), bg='#F9F9F9', fg='#343535')
		cancel_button.config(image=self.imagenes['not_ok_icon'], compound=LEFT)
		cancel_button.place(relx=0.34, rely=0.85)
		#********************************************************

		'''
		#********************************************************
		#				CONFIGURAMOS LOS EVENTOS				*
		#********************************************************
		button_anterior.config(command=lambda:self.pop_pila_anterior(View.VIEW_CREAR_PAQUETE))
		button_siguiente.config(command=lambda:self.pop_pila_siguiente())
		self.cedula_content_entry.trace("w", self.update_cedula_content_entry)
		button_edad_de_viaje.config(command=lambda:self.view_calendar(frame, content_button_edad, 4, 0.17, 0.277))
		#pre_venta_button.config(command=lambda:self.controller.agregar_pre_venta())
		#save_button.config(command=lambda:self.controller.guardar_paquete(name_content_entry.get(), combobox_tipos.get(), combobox_sub_tipos.get(),
		#		combobox_vigencia.get(), self.fecha_de_viaje, price_content_entry.get(), senha_content_entry.get(), incluye_text_widget.get(1.0, END),
		#		cant_pasajeros_content_entry.get(), self.pre_venta))
		#cancel_button.config(command=lambda:self.controller.crear_paquete(True))

		#********************************************************
		#				PACK A TODOS LOS BOTONES				*
		#********************************************************
		button_anterior.place(relx=0.025, rely=0.001)
		button_siguiente.place(relx=0.08, rely=0)

		frame.pack(padx=20, pady=20, anchor=NE)
		frame.pack_propagate(0)

		self.switch_frame(frame)

	def update_cedula_content_entry(self, *args):
		texto = ''
		cedula_texto = self.cedula_content_entry.get()

		#eliminamos los puntos '.'
		if len(cedula_texto) > 3:
			for i in range(len(cedula_texto)):
				if cedula_texto[i] != '.':
					texto += cedula_texto[i]

			cedula_texto = texto
			self.cedula_value = texto
			texto = ''
		else:
			self.cedula_value = cedula_texto

		j = 1
		if len(cedula_texto) > 3:
			for i in range(len(cedula_texto) -1, -1, -1):
				texto = cedula_texto[i] + texto
				if j % 3 == 0 and i != 0:
					texto = '.' + texto

				j += 1
		else:
			texto = cedula_texto

		self.cedula_content_entry.set(texto)

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
