#!/usr/bin/env python

"""
    Gui application interface.
"""

from gi.repository import Gtk
import signal
import os
from profile_selector import ProfileSelector
import loader

# Todo debug
from pprint import pprint

class Profiler(object):
    """
        Gui application interface.
    """
    # pylint: disable=no-member

    UI_PATH = os.path.join(
        os.path.dirname(__file__),
        'configuration-profiles.ui'
    )

    profiles = dict()

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file(self.UI_PATH)
        builder.connect_signals(self.Handler(self))
        self.builder = builder

        window = builder.get_object('window-main')
        window.show_all()

        self._init_profile_selector()

        # raise SystemExit

    def _init_profile_selector(self):
        """
            Load models into profile selector
        """
        self.profiles = loader.reload_profiles()
        combobox = self.builder.get_object('profile-combo')

        combobox.set_model(self.profiles['asListStore'])
        combobox.set_entry_text_column(0)
        combobox.set_active(0)

    @staticmethod
    def main():
        """
            Gtk.main wrapper.
        """
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        Gtk.main()

    def set_profile(self, profile_dict):
        treeview = self.builder.get_object('edit-pretty-treeview')
        treeview.set_model(profile_dict['ListStore'])

    class Handler(object):
        """Gui Event Handler"""

        def __init__(self, profiler):
            super(Profiler.Handler, self).__init__()
            self.profiler = profiler

        @staticmethod
        def on_delete_window(*args):
            """
                Window Close Action
            """
            Gtk.main_quit(*args)

        def on_profile_changed(self, widget):
            current_text = widget.get_child().get_text()
            model = widget.get_model()
            profile_names = [str(i[0]) for i in model]

            active_index = widget.get_active_iter()
            if active_index is None:
                if current_text in profile_names:
                    # Set Option as Selected, and let routine re-run
                    item_index = profile_names.index(current_text)
                    widget.set_active(item_index)
                    return None

                print('User Entered Text: `%s`' % current_text)

            else:
                # Load Current Item by name
                # print(str(model[active_index][0]))
                profile = self.profiler.profiles['byName'][current_text]
                self.profiler.set_profile(profile)

    # pylint: enable=no-member
