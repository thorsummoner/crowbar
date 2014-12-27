#!/usr/bin/env python3

from gi.repository import Gtk
from viewport import Viewport
import signal

from pprint import pprint

class AppWindow(Gtk.Window):
    """docstring for AppWindow"""
    def __init__(self):
        super(AppWindow, self).__init__()

    def main(self):
        window = self
        window.set_title("Hello World")
        self.set_size_request(200, 200)

        viewport = Viewport(Viewport.SQUARESET)
        window.add(viewport)

        window.connect('destroy', self.on_destroy)

        window.show_all()
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        Gtk.main()

    def on_destroy(self, window):
        Gtk.main_quit()

if __name__ == "__main__":
    AppWindow().main()

