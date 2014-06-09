
import signal
from crowbar.extensions import Extensions

from os import path
from gi.repository import Gtk

#DEBUG
from pprint import pprint

class Desktop(Gtk.Builder):
	"""docstring for Desktop"""

	top_level_glade = path.join(
		path.dirname(__file__), 'desktop.glade'
	)

	crowbar_menu = path.join(
		path.dirname(__file__), 'main.crowbar-menu'
	)

	def __init__(this):
		super(Desktop, this).__init__()

		# Load glade file
		this.add_from_file(this.top_level_glade)

		# Bind Glade-events to Desktop_signals methods
		this.signals = DesktopSignals()
		this.connect_signals(this.signals)


		# Get the glade root object as the main window.
		this.window = this.get_object('window')
		this.window.show_all()

		# Load Extensions
		this.extensions = extensions.Extensions(this)

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

		for menuitem in list:

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

			# Allow separators to be defined
			if menuitem['caption'] == '-':
				_menuitem = Gtk.SeparatorMenuItem()

			# Allow signals to be called
			if 'command' in menuitem:
				_menuitem.connect('activate', getattr(
					this.signals,
					menuitem['command']
				))

			_menuitem.show()
			menu.append(_menuitem)

			# Fill it with children if it so desired.
			if 'children' in menuitem:
				obj_id = 'menu_' + menuitem['id']
				# DO IF CHILD MENU WITH THIS ID DOES NOT EXIST
				submenu = Gtk.Menu()
				_menuitem.set_submenu(submenu)

				this._menuitems(menuitem['children'], submenu)

	def register_icons(self):
		basepath = path.realpath(path.dirname(path.realpath(__file__)) + '/../share/crowbar/icons')
		# register icon path
		# Note: I gave this document one hell of a try https://wiki.gnome.org/DraftSpecs/ThemableAppSpecificIcons
		#       What it documents didn't work, but for some reason in desperation I added the full endpoint and it worked.
		# TODO: Unfuck this to load like a sane environment... If that is even possible.

		Gtk.IconTheme.get_default().append_search_path(basepath + '/hicolor/24/mimetypes')
		Gtk.IconTheme.get_default().append_search_path(basepath + '/hicolor/24/actions')


class DesktopSignals(object):
	"""docstring for DesktopSignals"""
	def __init__(this):
		super(DesktopSignals, this).__init__()


	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def onButtonPressed(self, button):
		print("Hello World!")