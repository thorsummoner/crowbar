#!/usr/bin/env python3

import loader

from pprint import pprint

from gi.repository import Gtk

class ConfigProfilesWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="Configuration Profiles")

		self.set_default_size(200, 200)
		self.connect("delete-event", Gtk.main_quit)

		self.set_border_width(10)

		name_store = Gtk.ListStore(str, str, Gtk.ListStore, str)


		configs = loader.read_configs()

		for name, body in configs.items():
			proper_name = body.splitlines()[0].lstrip('# ').rstrip()

			liststore = Gtk.ListStore(str)
			for line in body.splitlines():
				liststore.append([line])

			name_store.append([name, proper_name, liststore, body])


		name_combo = Gtk.ComboBox.new_with_model_and_entry(name_store)
		name_combo.connect("changed", self.on_name_combo_changed)
		name_combo.set_entry_text_column(1)


		self.text_area = Gtk.TextView()

		self.textbuffer = self.text_area.get_buffer()
		self.textbuffer.set_text("This is some text inside of a Gtk.TextView. "
			+ "Select text and click one of the buttons 'bold', 'italic', "
			+ "or 'underline' to modify the text accordingly.")



		self.treeview = Gtk.TreeView(model=None)

		renderer_text = Gtk.CellRendererText()
		renderer_text.set_property("editable", True)
		column_text = Gtk.TreeViewColumn("Command", renderer_text, text=0)
		self.treeview.append_column(column_text)

		renderer_text.connect("edited", self.text_edited)



		box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
		box.pack_start(name_combo, True, True, 0)
		box.pack_start(self.text_area, True, True, 0)
		box.pack_start(self.treeview, True, True, 0)
		self.add(box)



	def text_edited(self, widget, path, text):
		self.liststore[path][1] = text

	def on_name_combo_changed(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter != None:
			model = combo.get_model()
			name, proper_name, model, body = model[tree_iter][:4]
			print("Selected: name=%s, proper_name=%s" % (name, proper_name))
			self.textbuffer.set_text(body)
			self.treeview.set_model(model)
		else:
			entry = combo.get_child()
			print("Entered: %s" % entry.get_text())

if __name__ == '__main__':
	win = ConfigProfilesWindow()
	win.show_all()
	Gtk.main()
