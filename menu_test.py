from gi.repository import Gtk, Gdk
import signal

from pprint import pprint

class MenuTest(Gtk.Window):
	"""docstring for MenuTest"""
	def __init__(self):
		super(MenuTest, self).__init__(title="Menu Test")
		self.connect("delete-event", Gtk.main_quit)

		self.spawn_menubar()

		self.set_default_size(200, 0)
		self.show_all()

	def spawn_menubar(self):
		menubar = Gtk.MenuBar()

		file_menu = self.spawn_menu(
			caption='File',
			widget=menubar,
			mnemonic='f'
		)

		self.spawn_action(
			caption='Exit',
			widget=file_menu,
			mnemonic='x',
			action=Gtk.main_quit
		)

		self.add(menubar)
		return menubar

	def spawn_menu(self, caption, widget, mnemonic):
		menu = Gtk.Menu()
		item = Gtk.MenuItem(caption)
		item.set_submenu(menu)
		if mnemonic:
			item.set_use_underline(True)
			item.set_label(self.menu_mnemonic(caption, mnemonic))
		widget.append(item)
		return menu

	def spawn_action(self, caption, widget, mnemonic, action):
		item = Gtk.MenuItem(caption)
		item.connect("activate", action)
		if mnemonic:
			item.set_use_underline(True)
			item.set_label(self.menu_mnemonic(caption, mnemonic))
		widget.append(item)
		return action

	def menu_mnemonic(self, caption, mnemonic):
		index = caption.lower().find(mnemonic)
		return caption[0:index] + '_' + caption[index:]

	def main(self):
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		Gtk.main()

if __name__ == "__main__":
	window = MenuTest()
	window.main()

