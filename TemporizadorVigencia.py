#!/usr/bin/env python
# -*- coding: latin-1 -*-

import pickle
from datetime import datetime, timedelta
from threading import Thread
from time import sleep
import os

class TemporizadorVigencia(Thread):
    PAUSE = 1
    TOTAL_PAUSE = 3

    def __init__(self, hora, delay):
        # El constructor recibe como parámetros:
        ## hora = en un string con formato hh:mm:ss y es la hora a la que queremos que se ejecute la función.
        ## delay = tiempo de espera entre comprobaciones en segundos.
        ## funcion = función a ejecutar.

        super(TemporizadorVigencia, self).__init__()
        self._estado = True
        self.hora = hora
        self.delay = delay
        #self.funcion = funcion

    def stop(self):
        self._estado = False

    def run(self):
        realizamos_comprobacion = False
        # Pasamos el string a dato tipo datetime
        aux = datetime.strptime(self.hora, '%H:%M:%S')
        # Obtenemos la fecha y hora actuales.
        hora = datetime.now()
        # Sustituimos la hora por la hora a ejecutar la función.
        hora = hora.replace(hour = aux.hour, minute=aux.minute, second=aux.second, microsecond = 0)

        # Comprobamos si la hora ya a pasado o no, si ha pasado sumamos un dia (hoy ya no se ejecutará)
        if self.si_hice_la_comprobacion():
            print('modificando fecha de comprobacion...')
            hora += timedelta(days=1)


        #Iniciamos el ciclo:
        si_cambio_vigencia = None
        paquetes = []

        while self._estado:
            if datetime.now() > hora and self.si_hice_la_comprobacion() == False:
                print('Hilo 2: procesando...')
                paquetes = self.get_paquetes()
                si_cambio_vigencia = self.revisar_vigencia(paquetes)
                if si_cambio_vigencia:
                    self.guardar_paquetes(paquetes)

                #print('Ejecucion programada ejecutada el {0} a las {1}'.format(hora.date(), hora.time()))
                hora += timedelta(days=1)
                #print('Proxima ejecucion programada el {0} a las {1}'.format(hora.date(), hora.time()))
                self.generar_achivo_de_comprobacion(datetime.now().day)

            #Esperamos x segundos para volver a ejecutar la comprobación.
            sleep(self.delay)

    def si_hice_la_comprobacion(self):
        #si el archivo existe entonces ya se realizo una comprobacion anterior
        result_return = None
        try:
            archivo = open('data_base_files/comprobacion_realizada.pickle', 'rb')
            result = pickle.load(archivo)
            if int(result) != 0:
                #la fecha del dia es valida
                result_returnt = True
            else:
                result_return = False
            archivo.close()
        except IOError:
            print('IOError...')
            result_return = False
        except EOFError:
            print('*********************')
            print('*  ERROR: EOFError  *')
            print('*********************')
            result_return = False

        return result_return

    def generar_achivo_de_comprobacion(self, dia_de_comprobacion):
        try:
            archivo_nuevo = open('data_base_files/comprobacion_realizada.pickle', 'wb')
            pickle.dump(dia_de_comprobacion, archivo_nuevo)
            archivo_nuevo.close()
        except IOError:
            try:
                archivo_nuevo = open('data_base_files/comprobacion_realizada.pickle', 'wb')
                archivo_nuevo.dump(dia_de_comprobacion, archivo_nuevo)
                archivo_nuevo.close()
            except Exception:
                print('*warnning: thread error  *')
        except Exception:
            print('*Error: something happened*')
            #raise
        return

    def guardar_paquetes(self, paquetes):
        print('guardando paquetes desde el Temporizador')

        try:
            archivo_nuevo = open('data_base_files/paquete.pickle', 'wb')
            pickle.dump(paquetes, archivo_nuevo)
            archivo_nuevo.close()
        except IOError:
            archivo_nuevo = open('data_base_files/paquete.pickle', 'wb')
            pickle.dump(paquetes, archivo_nuevo)
            archivo_nuevo.close()
        return

    def get_paquetes(self):
        result = []
        try:
	        archivo = open('data_base_files/paquete.pickle', 'rb')
	        result = pickle.load(archivo)
	        archivo.close()
	        return result
        except IOError:
	        return result
        return

    def revisar_vigencia(self, paquetes):
        si_cambio_vigencia = False
        print('estoy revisando la vigencia')
        for paquete in paquetes:
            if paquete.get_esta_vigente():
                fecha_de_viaje = str(paquete.get_fecha_de_viaje().year) + '-' + str(paquete.get_fecha_de_viaje().month) + '-' + str(paquete.get_fecha_de_viaje().day)
                hoy = str(datetime.today().year) + '-' + str(datetime.today().month) + '-' + str(datetime.today().day)
                if hoy > fecha_de_viaje:
                    si_cambio_vigencia = True
                    print('Cambiando vigencia....')
                    paquete.set_esta_vigente(False)

        return si_cambio_vigencia

