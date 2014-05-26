
from gi.repository import Gtk

class Handler:
	def deleteEvent(self, *args):
		Gtk.main_quit(*args)

	def open(self, path):
		print('Open: ' + path)
