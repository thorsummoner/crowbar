#!/usr/bin/env python

"""
    Main Window Class
"""

import os
import signal

from gi.repository import Gtk

class Window(Gtk.Window):
    """
        Gui application interface.
    """
    # pylint: disable=no-member

    ROOT_WINDOW = 'window1'

    def __init__(self, *args):
        super(Window, self).__init__(*args)

        builder = Gtk.Builder()
        builder.add_from_file(
            os.path.join(
                os.path.dirname(__file__),
                self.GLADE_FILE
            )
        )
        builder.connect_signals(self.Handler(self))
        self.builder = builder

        window = builder.get_object(self.ROOT_WINDOW)
        window.show_all()

    @staticmethod
    def main():
        """
            Gtk.main wrapper.
        """
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        Gtk.main()

    class BaseHandler(object):
        """
            Main Window Event Handler
        """

        def __init__(self, parent):
            super(Window.BaseHandler, self).__init__()
            self.parent = parent
            parent.connect("delete-event", self.on_delete_window)

        @staticmethod
        def on_delete_window(*args):
            """
                Window Close Action
            """
            Gtk.main_quit(*args)

    # pylint: enable=no-member
