
import signal

from os import path
from gi.repository import Gtk

class desktop(Gtk.Builder):
	"""docstring for desktop"""

	top_level_glade = path.join(
		path.dirname(__file__), 'desktop.glade'
	)

	crowbar_menu = path.join(
		path.dirname(__file__), 'main.crowbar-menu'
	)

	def __init__(this):
		super(desktop, this).__init__()

		# Load glade file
		this.add_from_file(this.top_level_glade)

		# Bind Glade-events to desktop_handlers methods
		this.connect_signals(dektop_handles())

		# Get the glade root object as the main window.
		this.window = this.get_object('window')
		this.window.show_all()

		this.menu_add(this.crowbar_menu)

	def main(this):
		# Die on Ctrl+C
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		Gtk.main()


	def menu_add(this, file):
		import json
		with open(file) as crowbar_menu:
			crowbar_menu = json.loads(crowbar_menu.read())

		menu = this._menuitems(
			crowbar_menu, this.get_object('menubar')
		)

	def _menuitems(this, list, menu):
		from pprint import pprint
		for menuitem in list:
			pprint(menuitem)


			menuitem_label = menuitem['caption']
			mnemonic_index = -1

			# Prefix mnemonic substring of caption with underscore
			if 'mnemonic' in menuitem:
				mnemonic_index = menuitem_label.lower().find(
					menuitem['mnemonic']
				)
			if -1 != mnemonic_index:
				menuitem_label = \
					menuitem_label[0:mnemonic_index] \
					+ '_' + \
					menuitem_label[mnemonic_index:]

			# Make a new menu item
			_menuitem = Gtk.MenuItem(
				label=menuitem_label, use_underline=True
			)

			if menuitem['caption'] == '-':
				_menuitem = Gtk.SeparatorMenuItem()

			_menuitem.show()
			menu.append(_menuitem)

			# Fill it with children if it so desired.
			if 'children' in menuitem:
				obj_id = 'menu_' + menuitem['id']
				# DO IF CHILD MENU WITH THIS ID DOES NOT EXIST
				submenu = Gtk.Menu()
				_menuitem.set_submenu(submenu)

				this._menuitems(menuitem['children'], submenu)


class dektop_handles(object):
	"""docstring for dektop_handles"""
	def __init__(this):
		super(dektop_handles, this).__init__()


	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def onButtonPressed(self, button):
		print("Hello World!")