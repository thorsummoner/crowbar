
import signal
import json
from gi.repository import Gtk, Gdk, Gdl
from lib.Extensions import Extensions
from importlib import import_module
from os import path

class crowbar(object):
	"""docstring for crowbar"""

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
		# Note: I gave this documnet one hell of a try https://wiki.gnome.org/DraftSpecs/ThemableAppSpecificIcons
		#       What it documents didn't work, but for some reason in desparation I added the full endpoint and it worked.
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
		with open(crowbar_mountpoints) as mountpoints:
			self.mountpoints = json.loads(mountpoints.read())

		from pprint import pprint
		for mountpoint, extensions in self.mountpoints.items():
			for extension in extensions:
				self.extensions[extension['extension']] = mount_box = Extensions(extension['extension'])

				# Correct Orientations.
				if type(mount_box.gui.get_children()[0]) is Gtk.Toolbar:

					if 'GTK_ORIENTATION_VERTICAL' == self.builder.get_object(mountpoint).get_orientation().value_name:
						# Mount point is vertical, orient content vertically.
						mount_box.gui.get_children()[0].set_orientation(Gtk.Orientation.VERTICAL)
						mount_box.gui.get_children()[0].set_vexpand(True)
						mount_box.gui.get_children()[0].set_hexpand(False)
					else:
						mount_box.gui.get_children()[0].set_orientation(Gtk.Orientation.HORIZONTAL)
						mount_box.gui.get_children()[0].set_vexpand(False)
						mount_box.gui.get_children()[0].set_hexpand(True)

				# Distiguish between toolbars and frames
				# # ???

				self.builder.get_object(mountpoint).add(mount_box.gui)

