#!/usr/bin/env python

from abc import ABCMeta, abstractmethod

class Documento(metaclass=ABCMeta):
	'''Clase abstracta documento'''

	def __init__(self):
		pass

	@abstractmethod
	def accion(self):
		pass
