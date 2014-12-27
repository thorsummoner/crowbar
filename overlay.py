#!/usr/bin/env python

from gi.repository import Gtk

class OverlayExample(Gtk.Window):
	"""docstring for OverlayExample"""
	def __init__(self):
		super(OverlayExample, self).__init__()

		self.set_default_size(200, 200)
		self.connect("destroy", lambda q: Gtk.main_quit())

		overlay = Gtk.Overlay()
		self.add(overlay)

		textview = Gtk.TextView()
		textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
		textbuffer = textview.get_buffer()
		textbuffer.set_text("Welcome to the PyGObject Tutorial\n\nThis guide aims to provide an introduction to using Python and GTK+.\n\nIt includes many sample code files and exercises for building your knowledge of the language.", -1)
		overlay.add(textview)

		button = Gtk.Label("X/Y")
		button.set_valign(Gtk.Align.START)
		button.set_halign(Gtk.Align.START)
		overlay.add_overlay(button)

		overlay.show_all()

		self.show_all()

		Gtk.main()

if __name__ == '__main__':
	OverlayExample()
