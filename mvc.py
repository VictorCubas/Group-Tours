# -*- coding: UTF-8 -*-

"""Show MVC pattern with Python and Tkinter."""

from random import choice

from tkinter import *

class View:
	"""Implement the app View."""

	def __init__(self, parent, controller):
		"""Class initializer."""
		# Get a reference to the Controller
		self.controller = controller
		# Build the GUI
		self.greetings_label = Label(parent, text='')
		self.greetings_label.pack()
		self.greetings_button = Button(parent, text='Say Hello')
		self.greetings_button.pack()
		# Connect with the Controller
		self.greetings_button.configure(command=self.controller.on_greetings_button_clicked)

	def show_greeting(self, greeting):
	    """Show greeting to the user."""
	    self.greetings_label['text'] = greeting

class Controller:
	"""Implement the app Controller."""

	def __init__(self, parent):
	    """Class initializer."""
	    # Create the View and Model inside the Controller (Composition)
	    self.view = View(parent, self) # Pass a Controller's reference to View
	    self.model = Model()

	def get_greeting(self):
	    """Get greeting from the Model."""
	    # Ask the Model for a greeting
	    greeting = self.model.get_greeting()
	    return greeting

	def on_greetings_button_clicked(self):
	    """Callback for View.greetings_button."""
	    # Ask Controller for a greeting
	    greeting = self.get_greeting()
	    # Ask the view to show greeting to user
	    self.view.show_greeting(greeting)

class Model:
	"""Implement the app Model."""

	def __init__(self):
	    """Class initializer."""
	    # Model data
	    self.greetings = ('Hello Python Devs!',
	                      'Hello World!',
	                      'Hello Python Scouts Readers!',
	                      'Hello Python MVC Design Pattern!')

	def get_greeting(self):
	    """Return a random greeting."""
	    return choice(self.greetings)

if __name__ == '__main__':

	# Client Code

	root = Tk()  # Create the root window

	ctrl = Controller(parent=root)  # Initialize the Controller

	root.mainloop()
