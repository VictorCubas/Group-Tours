import calendar
import datetime
import time
import sys
if sys.version[0] == '2':
    import Tkinter as tk
else:
    import tkinter as tk
 
class Calendar:
    def __init__(self, parent):
        self.values = None
        self.parent = parent
        self.cal = calendar.TextCalendar(calendar.SUNDAY)
        self.year = datetime.date.today().year
        self.month = datetime.date.today().month
        self.wid = []
        self.day_selected = datetime.date.today().day
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = ''
        self.setup(self.year, self.month)

    def clear(self):
        for w in self.wid[:]:
            w.grid_forget()
            #w.destroy()
            self.wid.remove(w)
     
    def go_prev(self):
        if self.month > 1:
            self.month -= 1
        else:
            self.month = 12
            self.year -= 1
        #self.selected = (self.month, self.year)
        self.clear()
        self.setup(self.year, self.month)
 
    def go_next(self):
        if self.month < 12:
            self.month += 1
        else:
            self.month = 1
            self.year += 1
         
        #self.selected = (self.month, self.year)
        self.clear()
        self.setup(self.year, self.month)

    def selection(self, day, name, position, d):
        self.day_selected = day
        self.month_selected = self.month
        self.year_selected = self.year
        self.day_name = name
         
        #data
        self.values = datetime.date(self.year_selected, self.month_selected, self.day_selected)
        if self.position_anterior > -1:
            self.wid[self.position_anterior].config(font=('tahoma', '9'), fg='#000000', activeforeground='#000000')

        self.wid[position].config(font=('tahoma', '9', 'bold'), fg='#48C2FA', activeforeground='#48C2FA')
        self.position_anterior = position

    def setup(self, year, m):
        self.position_anterior = -1
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
                    self.wid.append(b)
                    b.grid(row=w, column=d)
         
    def kill_and_save(self):
        self.parent.destroy()

    def get_date_selected(self):
        return self.values
