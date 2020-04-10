import calendar
import datetime
import time
import sys
if sys.version[0] == '2':
    import Tkinter as tk
else:
    import tkinter as tk
 
class Calendar:
    AMOUNT_WIDGET_PREVIUS = 9
    def __init__(self, parent, fecha_seleccionado):
        self.values = None
        self.parent = parent
        self.cal = calendar.TextCalendar(calendar.SUNDAY)
        self.wid = []

        self.date_init(fecha_seleccionado)
        self.day_name = ''
        self.setup(self.year, self.month)
        self.mes_anterior_selected = 0
        self.paint_day_selected(fecha_seleccionado)

    def paint_day_selected(self, fecha_seleccionado):
        #marcamos el dia selecionado en caso de que ya se haya seleccionado uno
        if fecha_seleccionado is not None:
            #calculamos el numero de widget el cual se usa como posicion el el vector wid y asi lo pintamos
            position = self.day_selected + Calendar.AMOUNT_WIDGET_PREVIUS
            #procedemos a pintarlo
            self.wid[position].config(font=('tahoma', '9', 'bold'), fg='#48C2FA', activeforeground='#48C2FA')
            #guardamos la posicion anterior del widget pintado
            self.position_anterior = position
            #guardamos mes anterior
            self.mes_anterior_selected = self.month
        else:
            self.position_anterior = -1

    def date_init(self, fecha_seleccionado):
        if fecha_seleccionado is not None:
            self.month = fecha_seleccionado.month
            self.year = fecha_seleccionado.year

            self.day_selected = fecha_seleccionado.day
            self.month_selected = self.month
            self.year_selected = self.year

        else:
            self.year = datetime.date.today().year
            self.month = datetime.date.today().month

            self.day_selected = datetime.date.today().day
            self.month_selected = self.month
            self.year_selected = self.year

    def clear(self):
        for w in self.wid[:]:
            w.grid_forget()

            self.wid.remove(w)
     
    def go_prev(self):
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1

        self.clear()
        self.setup(self.year, self.month)

        #comparamos en caso de que volvamos al mes anterior de forma que se muestre el dia ya seleccionado
        if self.month == self.mes_anterior_selected:
            self.wid[self.position_anterior].config(font=('tahoma', '9', 'bold'), fg='#48C2FA', activeforeground='#48C2FA')
 
    def go_next(self):

        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1

        self.clear()
        self.setup(self.year, self.month)

        #comparamos en caso de que volvamos al mes anterior de forma que se muestre el dia ya seleccionado
        if self.month == self.mes_anterior_selected:
            self.wid[self.position_anterior].config(font=('tahoma', '9', 'bold'), fg='#48C2FA', activeforeground='#48C2FA')

    def selection(self, day, name, position, d):
        self.day_selected = day
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = name
        self.mes_anterior_selected = self.month
         
        #data
        self.values = datetime.date(self.year_selected, self.month_selected, self.day_selected)
        if self.position_anterior > -1:
            self.wid[self.position_anterior].config(font=('tahoma', '9'), fg='#000000', activeforeground='#000000')

        self.wid[position].config(font=('tahoma', '9', 'bold'), fg='#48C2FA', activeforeground='#48C2FA')
        self.position_anterior = position

    def setup(self, year, m):
        #self.position_anterior = -1
        position = 0
        left = tk.Button(self.parent, bg='#F9F9F9', text='<', command=self.go_prev)
        self.wid.append(left)
        left.grid(row=0, column=1)
         
        header = tk.Label(self.parent, height=2, bg='#F9F9F9', text='{}   {}'.format(calendar.month_abbr[m], str(year)))
        header.config(font=('tahoma', '10', 'bold'))
        position += 1
        self.wid.append(header)
        header.grid(row=0, column=2, columnspan=3)
         
        right = tk.Button(self.parent, bg='#F9F9F9', text='>', command=self.go_next)
        position += 1
        self.wid.append(right)
        right.grid(row=0, column=5)
         
        days = ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado']
        for num, name in enumerate(days):
            t = tk.Label(self.parent, bg='#F9F9F9', text=name[:3])
            position += 1
            self.wid.append(t)
            t.grid(row=1, column=num)
         
        for w, week in enumerate(self.cal.monthdayscalendar(year, m), 2):
            for d, day in enumerate(week):
                if day:
                    position += 1
                    b = tk.Button(self.parent, width=1, bg='#F9F9F9', text=day, command=lambda day=day, position=position, d=d:self.selection(day, calendar.day_name[(d-1) % 7], position, d))
                    #b = tk.Button(self.parent, width=1, bg='#F9F9F9', text=day, command=lambda day=day, position=position,:self.selection(day, calendar.day_name[(d-1) % 7], position))

                    #if position == self.position_anterior:
                    self.wid.append(b)
                    b.grid(row=w, column=d)

    def kill_and_save(self):
        self.parent.destroy()

    def get_date_selected(self):
        return self.values
