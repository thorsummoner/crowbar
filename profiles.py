#!/usr/bin/env python3

from gi.repository import Gtk

import loader

from pprint import pprint

PROFILE_DEFAULT = 'default'

class ConfigProfilesWindow(Gtk.Window):

	profile = Gtk.ComboBox.new_with_entry()
	configs = loader.read_configs()
	configs_store = Gtk.ListStore(str, str, Gtk.ListStore, str)

	modes = Gtk.Notebook()
	mode = type('mode', (object,), dict(
		raw=Gtk.TextView(),
		table=Gtk.TreeView()
	))

	def __init__(self):
		Gtk.Window.__init__(self, title="Configuration Profiles")

		self.set_default_size(400, 300)
		self.connect("delete-event", Gtk.main_quit)
		self.connect("focus-out-event", Gtk.main_quit) # DEBUG

		self.set_border_width(10)

		box = Gtk.Box(spacing=10, orientation=Gtk.Orientation.VERTICAL)
		self.add(box)

		# Profile
		box.pack_start(self.profile, False, False, 0)
		self.profile.set_model(self.configs_store)
		self.profile.set_entry_text_column(1)
		self.profile.connect("changed", self.on_profile_changed)

		# Config Files
		for name, body in self.configs.items():
			config_store = self.new_config_store(body=body)
			if name == PROFILE_DEFAULT:
				self.configs_store.prepend(config_store)
				self.profile.set_active(0)
			else:
				self.configs_store.append(config_store)

		# Notebook
		box.pack_start(self.modes, True, True, 0)
		self.mode.raw.set_border_width(10)
		self.modes.append_page(self.mode.table, Gtk.Label('Operations'))
		self.modes.append_page(self.mode.raw, Gtk.Label('Raw'))

		# Operations Table of Commands

		# self.text_area = Gtk.TextView()

		# self.textbuffer = self.text_area.get_buffer()
		# self.textbuffer.set_text("This is some text inside of a Gtk.TextView. "
		# 	+ "Select text and click one of the buttons 'bold', 'italic', "
		# 	+ "or 'underline' to modify the text accordingly.")

		# self.treeview = Gtk.TreeView(model=None)

		# renderer_text = Gtk.CellRendererText()
		# renderer_text.set_property("editable", True)
		# column_text = Gtk.TreeViewColumn("Command", renderer_text, text=0)
		# self.treeview.append_column(column_text)

		# renderer_text.connect("edited", self.text_edited)

		# box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
		# box.pack_start(self._spawn_selector(), True, True, 0)
		# box.pack_start(self.text_area, True, True, 0)
		# box.pack_start(self.treeview, True, True, 0)
		# self.add(box)
	# def _spawn_selector(self):
	# 	name_combo = Gtk.ComboBox.new_with_model_and_entry(self.name_store)
	# 	name_combo.connect("changed", self.on_name_combo_changed)
	# 	name_combo.set_entry_text_column(1)

	# 	self.selector = name_combo
	# 	return self.selector

	# def text_edited(self, widget, path, text):
	# 	self.liststore[path][1] = text

	def on_profile_changed(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter != None:
			model = combo.get_model()
			name, proper_name, model, body = model[tree_iter][:4]
			print("Selected: name=%s, proper_name=%s" % (name, proper_name))
			self.mode.raw.get_buffer().set_text(body)
			self.mode.table.set_model(model)
		else:
			entry = combo.get_child()
			print("Entered: %s" % entry.get_text())

	def new_config_store(self, name=None, body=None):
		if name:
			assert self.configs[name], 'No config by name `%s`' % name;
			body = self.configs[name]

		proper_name = body.splitlines()[0].lstrip('# ').rstrip()
		body_lines = Gtk.ListStore(str)
		for line in body.splitlines():
			body_lines.append([line])

		return [name, proper_name, body_lines, body]


if __name__ == '__main__':
	win = ConfigProfilesWindow()
	win.show_all()
	Gtk.main()
