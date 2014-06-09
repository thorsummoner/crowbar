
import json

from os import path
from gi.repository import Gtk, Gdk, Gdl
from importlib import import_module


class Extensions(object):
	"""docstring for Extensions"""

	mountpoints_file = path.join(
		path.dirname(__file__),
		'..', 'settings',
		'default.crowbar-mountpoints'
	)

	extensions = {}

	def __init__(this, desktop):
		super(Extensions, this).__init__()
		this.desktop = desktop

		# Make A single dock for the entire application.
		this.dock = Gdl.Dock()

		# Read our settings file (this functionality may already be offered by Gdl)
		with open(this.mountpoints_file) as mountpoints:
			mountpoints = json.loads(mountpoints.read())

		for mountpoint, extensions in mountpoints.items():

			# Block Variables
			orientation = this.desktop.get_object(mountpoint).get_orientation()
			is_horizontal = 'GTK_ORIENTATION_HORIZONTAL' == orientation.value_name

			# Create Dock inside glade mountpoint box
			dock = Gdl.Dock.new_from(this.dock, False)
			this.desktop.get_object(mountpoint).add(dock)

			dock.set_hexpand(is_horizontal)
			dock.set_vexpand(not is_horizontal)

			# Reverse the order in which toolbars are spawned, it makes the resizing the smallest bit more sane.
			extensions.reverse()
			for extension in extensions:

				# Block Variables
				extension_name = extension['extension']
				extension_gui  = Extension(extension_name).gui

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

class Extension(object):
        """docstring for Extension"""

        extension_root = path.join(
        	path.dirname(__file__),
        	'..', 'extensions'
        )

        def __init__(self, extension_name):
                # print(extension_name)
                super(Extension, self).__init__()
                self.extension_name = extension_name

                self.extension_path = path.join(self.extension_root, self.extension_name)

                self.build()

        def build(self):
                builder = Gtk.Builder()
                self.builder = builder
                builder.add_from_file(
                        path.join(self.extension_path, self.extension_name) + '.glade'
                )
                # builder.connect_signals(Handler())
                self.gui = builder.get_object(self.extension_name)

                if self.gui == None:
                        import pprint
                        pprint.pprint(self.extension_name)
