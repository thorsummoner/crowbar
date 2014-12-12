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
		table_window = Gtk.ScrolledWindow()
		table_window.set_policy(
			Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.ALWAYS)
		table_window.add(self.mode.table)

		self.modes.append_page(table_window, self.notebook_tab('Edit', Gtk.STOCK_EXECUTE))
		self.modes.append_page(self.mode.raw, self.notebook_tab('Raw', Gtk.STOCK_FILE))

		# Operations Table of Commands
		cell_checkbox = Gtk.CellRendererToggle()
		cell_checkbox.connect("toggled", self.toggle_line)
		col_checkbox = Gtk.TreeViewColumn("#", cell_checkbox, active=0)
		self.mode.table.append_column(col_checkbox)

		cell_command = Gtk.CellRendererText()
		cell_command.set_property("editable", True)
		cell_command.connect("edited", self.on_cell_edited)
		col_command = Gtk.TreeViewColumn("Command", cell_command, text=1)
		self.mode.table.append_column(col_command)

	def on_cell_edited(self, widget, path, text):
		pprint((widget, path, text))
		# self.liststore[path][1] = text

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

		body_lines = body.splitlines()
		proper_name = body_lines.pop(0).lstrip('# ').rstrip()
		body_store = Gtk.ListStore(bool, str, str)
		for line in body_lines:
			body_store.append([not line.startswith('#'), line.lstrip('# '), line])

		return [name, proper_name, body_store, body]


	def notebook_tab(self, label, icon):
		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
		box_icon = Gtk.Image.new_from_stock(icon, Gtk.IconSize.MENU)
		box.pack_start(box_icon, False, False, 0)
		box.pack_start(Gtk.Label(label), True, True, 0)
		box.pack_start(Gtk.Label(''), False, False, 0)
		box.show_all()

		return box

	def toggle_line(self, widget, index):
		model = self.mode.table.get_model()
		row = model[index]
		row[0] ^= True
		if row[0]:
			row[2] = row[2].lstrip('# ')
		else:
			row[2] = '# ' + row[2]

		self.mode.raw.get_buffer().set_text(
			'\n'.join([row[2] for row in model])
		)

if __name__ == '__main__':
	win = ConfigProfilesWindow()
	win.show_all()
	Gtk.main()
