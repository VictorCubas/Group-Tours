#!/usr/bin/env python

from abc import ABCMeta, abstractmethod

class Contrato(metaclass=ABCMeta):
	'''Clase abstracta contrato'''

	def __init__(self):
		pass

	@abstractmethod
	def accion(self):
		pass
