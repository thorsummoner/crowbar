#!/c/Python34x32/python.exe

import signal
from gi.repository import Gtk, Gdk
from lib.Handler import Handler

max_int = 2**14 # 16384

builder = Gtk.Builder()
builder.add_from_file("ui/crowbar.glade")
builder.connect_signals(Handler())

window = builder.get_object("MainWindow")

style_provider = Gtk.CssProvider()
style_provider.load_from_path('ui/crowbar.css')

Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

window.show_all()

signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
