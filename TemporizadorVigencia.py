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

        #print('\nSEGUNDO')

        while self._estado:
            #pause_counter = 1
            #while pause_counter <= TemporizadorVigencia.TOTAL_PAUSE:
            #    print(' .'.strip())
            #    sleep(TemporizadorVigencia.PAUSE)
            #    pause_counter += 1


            # Comparamos la hora actual con la de ejecución y ejecutamos o no la función.
            ## Si se ejecuta sumamos un dia a la fecha objetivo.
            #print('Actualizando vigencia...')
            #print('Hilo 2')
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
                #self.stop()

            #Esperamos x segundos para volver a ejecutar la comprobación.
            sleep(self.delay)

        #Si usamos el método stop() salimos del ciclo y el hilo terminará.
        #else:
        #     print('Ejecución automática finalizada')

    def si_hice_la_comprobacion(self):
        #si el archivo existe entonces ya se realizo una comprobacion anterior
        result_return = None
        try:
            archivo = open('data_base_files/comprobacion_realizada.pickle', 'rb')
            #print('a...')
            result = pickle.load(archivo)
            #print('b...')
            if int(result) is not 0:
                #la fecha del dia es valida
                result_returnt = True
            else:
                result_return = False
            archivo.close()
        except IOError:
            result_return = False
        except EOFError:
            print('*********************')
            print('*  ERROR: EOFError  *')
            print('* result:{}'.format(result_return))
            print('*********************')
            result_return = False

        return result_return

    def generar_achivo_de_comprobacion(self, dia_de_comprobacion):
        try:
            archivo_nuevo = open('data_base_files/comprobacion_realizada.pickle', 'wb')
            pickle.dump(dia_de_comprobacion, archivo_nuevo)
            archivo_nuevo.close()
        except IOError:
            archivo_nuevo = open('data_base_files/comprobacion_realizada.pickle', 'wb')
            archivo_nuevo.dump(dia_de_comprobacion, archivo_nuevo)
            archivo_nuevo.close()
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
                fecha = paquete.get_fecha_de_viaje()
                if fecha is None:
                    continue

                fecha_de_viaje = fecha.year*100 + fecha.month
                fecha_de_viaje = fecha_de_viaje * 100 + fecha.day
                #print('fecha de viaje: {}'.format(fecha_de_viaje))
                hoy = (datetime.today().year * 100 + datetime.today().month) * 100 + datetime.today().day
                #print('fecha de hoy: {}'.format(hoy))

                if hoy > fecha_de_viaje:
                    si_cambio_vigencia = True
                    print('Cambiando vigencia....')
                    paquete.set_esta_vigente(False)

        return si_cambio_vigencia

#t = Temporizador('12:42:00', 1)
#t.start()
#=========================================================================================
#Ejemplo de uso:

#t = Temporizador('22:10:00',1,ejecutar)# Instanciamos nuestra clase Temporizador
#t.start() #Iniciamos el hilo

#Mientras el programa principal puede seguir funcinando:
#sleep(2)
#for _ in range(10):
#    print('Imprimiendo desde hilo principal')
#    sleep(2)

# Si en cualquier momento queremos detener el hilo desde la aplicacion simplemete usamos el método stop()
#sleep(120) # Simulamos un tiempo de espera durante el cual el programa principal puede seguir funcionando.
#t.stop()   # Detenemos el hilo.
