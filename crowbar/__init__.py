
import signal

from os import path
from gi.repository import Gtk

class desktop(Gtk.Builder):
	"""docstring for desktop"""

	top_level_glade = path.join(
		path.dirname(__file__), 'desktop.glade'
	)

	def __init__(this):
		super(desktop, this).__init__()

		this.add_from_file(this.top_level_glade)


	def main(this):

		# Bind Glade-events to desktop_handlers methods
		this.connect_signals(dektop_handles())

		# Get the glade root object as the main window.
		this.window = this.get_object('window')
		this.window.show_all()

		# Die on Ctrl+C
		signal.signal(signal.SIGINT, signal.SIG_DFL)

		Gtk.main()

class dektop_handles(object):
	"""docstring for dektop_handles"""
	def __init__(this):
		super(dektop_handles, this).__init__()


	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def onButtonPressed(self, button):
		print("Hello World!")