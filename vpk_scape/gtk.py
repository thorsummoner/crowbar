#!/usr/bin/env python3

import os
import signal

from gi.repository import Gtk
from gi.repository import Gdk

import pkg_resources

import vpk_scape.vpk_shell

class VpkScapeMainWindow(Gtk.Window):
    """
        Gui application interface.
    """

    GLADE_FILE = pkg_resources.resource_filename(__name__, 'data/.glade')
    CSS_PROVIDER_FILE = pkg_resources.resource_filename(__name__, 'data/.css')
    ROOT_WINDOW = 'window_main'

    builder = None
    cssprovider = None

    vpk_shell = None

    liststore_higherarchy = None
    treeview_higherarchy = None

    liststore_directory = None
    treeview_directory = None


    # pylint: disable=no-member

    def __init__(self):
        super(VpkScapeMainWindow, self).__init__()

        if self.builder is None:
            self.builder = Gtk.Builder()
            self.builder.add_from_file(self.GLADE_FILE)

        self.root_window = self.builder.get_object(self.ROOT_WINDOW)

        self.builder.connect_signals(self.Handler(self))

        if self.cssprovider is None:
            self.cssprovider = Gtk.CssProvider()
            self.cssprovider.load_from_path(self.CSS_PROVIDER_FILE)

            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                self.cssprovider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )

        self.root_window.show_all()

        self.liststore_higherarchy = self.builder.get_object('liststore_higherarchy')
        self.treeview_higherarchy = self.builder.get_object('treeview_higherarchy')

        self.liststore_directory = self.builder.get_object('liststore_directory')
        self.treeview_directory = self.builder.get_object('treeview_directory')


    @staticmethod
    def main():
        """
            Gtk.main wrapper with ctrl+c (Signal 2) interupt handler.
        """
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        Gtk.main()

    class Handler(object):
        """
            Main Window Event Handler
        """

        def __init__(self, parent):
            super(VpkScapeMainWindow.Handler, self).__init__()
            self.parent = parent
            parent.root_window.connect("delete-event", self.on_delete_window)

        @staticmethod
        def on_delete_window(self, *args):
            """
                Window Close Action
            """
            Gtk.main_quit(*args)

        def on_file_open(self, widget):
            filechooserdialog = Gtk.FileChooserDialog(
                'Please choose a file', self.parent,
                Gtk.FileChooserAction.OPEN,
                (
                        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK
                )
            )

            filter_text = Gtk.FileFilter()
            filter_text.set_name("VPK files")
            filter_text.add_pattern("*.vpk")
            filter_text.add_mime_type("application/x-vnd.valve.vpk")
            filechooserdialog.add_filter(filter_text)

            filter_any = Gtk.FileFilter()
            filter_any.set_name("Any files")
            filter_any.add_pattern("*")
            filechooserdialog.add_filter(filter_any)

            response = filechooserdialog.run()
            filechooserdialog.hide()
            if response == Gtk.ResponseType.OK:
                self.vpk_shell = vpk_scape.vpk_shell.VpkShell(
                    self,
                    filechooserdialog.get_filename()
                )

            filechooserdialog.destroy()



# pylint: enable=no-member

class ClassName(object):
    def __init__(self, arg):
        super(ClassName, self).__init__()
        self.arg = arg

