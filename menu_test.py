from gi.repository import Gtk, Gdk
import signal

class MenuTest(Gtk.Window):
	"""docstring for MenuTest"""
	def __init__(self):
		super(MenuTest, self).__init__(title="Menu Test")
		self.connect("delete-event", Gtk.main_quit)
		self.show_all()

	def main(self):
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		Gtk.main()

if __name__ == "__main__":
	window = MenuTest()
	window.main()

