#!/usr/bin/env python
# -*- coding: latin-1 -*-

import pickle
from datetime import datetime, timedelta
from threading import Thread
from time import sleep
from os import remove
import os

#from Model import Model

class TemporizadorDeleteFile(Thread):
    def __init__(self, hora, delay):
        # El constructor recibe como parámetros:
        ## hora = en un string con formato hh:mm:ss y es la hora a la que queremos que se ejecute la función.
        ## delay = tiempo de espera entre comprobaciones en segundos.
        ## funcion = función a ejecutar.

        super(TemporizadorDeleteFile, self).__init__()
        self._estado = True
        self.hora = hora
        self.delay = delay
        #self.funcion = funcion

    def stop(self):
        self._estado = False

    def run(self):
        # Pasamos el string a dato tipo datetime
        aux = datetime.strptime(self.hora, '%H:%M:%S')
        # Obtenemos la fecha y hora actuales.
        hora = datetime.now()
        # Sustituimos la hora por la hora a ejecutar la función.
        hora = hora.replace(hour = aux.hour, minute=aux.minute, second=aux.second, microsecond = 0)

        #print('\nPRIMERO')

        #Iniciamos el ciclo:
        while self._estado:
            # Comparamos la hora actual con la de ejecución y ejecutamos o no la función.
            # Si se ejecuta sumamos un dia a la fecha objetivo.
            dia_comprobacion = self.get_dia_comprobacion()

            #print('Hilo 1, dia comparado:', dia_comprobacion)
            if dia_comprobacion < datetime.now().day and hora <= datetime.now():
                self.actualizar_archivo_comprobacion()
                #print('Hilo 1: procesando...\n')
                hora += timedelta(days=1)

            #Esperamos x segundos para volver a ejecutar la comprobación.
            sleep(self.delay)

    def get_dia_comprobacion(self):
        dia = None
        try:
            archivo = open('data_base_files/comprobacion_realizada.pickle', 'rb')
            dia = pickle.load(archivo)
            dia = int(dia)
            archivo.close()
        except (IOError, EOFError):
	        dia = 0
        return dia

    def actualizar_archivo_comprobacion(self):
        result = 0
        try:
            archivo = open('data_base_files/comprobacion_realizada.pickle', 'wb')
            pickle.dump(result, archivo)
            archivo.close()
        except (IOError, EOFError):
            archivo = open('data_base_files/comprobacion_realizada.pickle', 'wb')
            pickle.dump(result, archivo)
            archivo.close()

        return

#t = TemporizadorDeleteFile('12:42:00', 1)
#t.start()
