
import signal
import json
from gi.repository import Gtk, Gdk
from lib.Extensions import Extensions
from importlib import import_module

class crowbar(object):
	"""docstring for crowbar"""

	extensions = {}

	def __init__(self):
		super(crowbar, self).__init__()

		self.build()
		self.load_extensions('settings/default.crowbar-mountpoints')
		self.window.show_all()

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




























# from gi.repository import Gtk, Gdk
# from lib.Handler import Handler

# max_int = 2**14 # 16384

# builder = Gtk.Builder()
# builder.add_from_file("ui/crowbar.glade")
# builder.connect_signals(Handler())

# window = builder.get_object("MainWindow")

# style_provider = Gtk.CssProvider()
# style_provider.load_from_path('ui/crowbar.css')

# Gtk.StyleContext.add_provider_for_screen(
#     Gdk.Screen.get_default(),
#     style_provider,
#     Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
# )

# window.show_all()

# signal.signal(signal.SIGINT, signal.SIG_DFL)
# Gtk.main()
#
