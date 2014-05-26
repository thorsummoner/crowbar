from os import path
from gi.repository import Gtk, Gdk

class Extensions(object):
	"""docstring for Extensions"""

	extension_root = 'extensions'

	def __init__(self, extension_name):
		# print(extension_name)
		super(Extensions, self).__init__()
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

