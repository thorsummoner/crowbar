
import signal
import json
from gi.repository import Gtk, Gdk, Gdl
from lib.Extensions import Extensions
from importlib import import_module
from os import path

class crowbar(object):
	"""docstring for crowbar lol"""

	extensions = {}

	def __init__(self):
		super(crowbar, self).__init__()

		self.register_icons()
		self.build()
		self.load_extensions('settings/default.crowbar-mountpoints')
		self.window.show_all()

	def register_icons(self):
		basepath = path.realpath(path.dirname(path.realpath(__file__)) + '/../share/crowbar/icons')
		# register icon path
		# Note: I gave this document one hell of a try https://wiki.gnome.org/DraftSpecs/ThemableAppSpecificIcons
		#       What it documents didn't work, but for some reason in desperation I added the full endpoint and it worked.
		# TODO: Unfuck this to load like a sane environment... If that is even possible.

		Gtk.IconTheme.get_default().append_search_path(basepath + '/hicolor/24/mimetypes')
		Gtk.IconTheme.get_default().append_search_path(basepath + '/hicolor/24/actions')

	def main(self):
		signal.signal(signal.SIGINT, signal.SIG_DFL)
		Gtk.main()

	def build(self):
		builder = Gtk.Builder()
		self.builder = builder
		builder.add_from_file('crowbar/crowbar.glade')
		builder.connect_signals({
			"onDeleteWindow": Gtk.main_quit,
		})

		self.window = builder.get_object('window')


	def load_extensions(self, crowbar_mountpoints):

		# Make A single dock for the entire application.
		self.extension_dock = Gdl.Dock()

		# Read our settings file (this functionality may already be offered by Gdl)
		with open(crowbar_mountpoints) as mountpoints:
			mountpoints = json.loads(mountpoints.read())

		for mountpoint, extensions in mountpoints.items():

			# Block Variables
			orientation = self.builder.get_object(mountpoint).get_orientation()
			is_horizontal = 'GTK_ORIENTATION_HORIZONTAL' == orientation.value_name

			# Create Dock inside glade mountpoint box
			dock = Gdl.Dock.new_from(self.extension_dock, False)
			self.builder.get_object(mountpoint).add(dock)

			dock.set_hexpand(is_horizontal)
			dock.set_vexpand(not is_horizontal)

			# Reverse the order in which toolbars are spawned, it makes the resizing the smallest bit more sane.
			extensions.reverse()
			for extension in extensions:

				# Block Variables
				extension_name = extension['extension']
				extension_gui  = Extensions(extension_name).gui

				# Create Dock Item
				dock_item = Gdl.DockItem.new(
					extension_name,
					extension_name,
					Gdl.DockItemBehavior.NORMAL
				)

				# Add flags, this can probably be condensed into the instantiation call if I lookup Python Bitwise Or.
				dock_item.set_behavior_flags( Gdl.DockItemBehavior.CANT_ICONIFY                                                                , False)
				dock_item.set_behavior_flags( Gdl.DockItemBehavior.CANT_CLOSE                                                                  , False)
				dock_item.set_behavior_flags( Gdl.DockItemBehavior.NEVER_VERTICAL if is_horizontal else Gdl.DockItemBehavior.NEVER_HORIZONTAL  , False)
				dock_item.set_behavior_flags( Gdl.DockItemBehavior.CANT_DOCK_TOP if is_horizontal else Gdl.DockItemBehavior.CANT_DOCK_LEFT     , False)
				dock_item.set_behavior_flags( Gdl.DockItemBehavior.CANT_DOCK_BOTTOM if is_horizontal else Gdl.DockItemBehavior.CANT_DOCK_RIGHT , False)
				dock_item.set_orientation(orientation)

				# Orient things properly; Hide Toolbar buttons for horizontal elements.
				if getattr(extension_gui, 'set_orientation', None):
					extension_gui.set_orientation(orientation)
				if type(extension_gui) is Gtk.Toolbar or is_horizontal:
					dock_item.set_behavior_flags( Gdl.DockItemBehavior.NO_GRIP, False)

				dock_item.add(extension_gui)
				dock_item.set_hexpand( False if is_horizontal else True )
				dock_item.set_vexpand( False if is_horizontal else True )

				# Dock things where the settings file told us to. :D
				dock.add_item(
					dock_item,
					Gdl.DockPlacement.LEFT if is_horizontal else Gdl.DockPlacement.TOP
				)
