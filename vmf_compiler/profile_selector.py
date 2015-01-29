from gi.repository import Gtk

from pprint import pprint

class ProfileSelector(object):
    """docstring for ProfileSelector"""

    PROFILE_DEFAULT = 'default'

    # combobox = Gtk.ComboBox.new_with_entry()

    config_stores = Gtk.ListStore(str, str, Gtk.ListStore, str)
    parent_profiles = None

    def __init__(self, parent_profiles):
        super(ProfileSelector, self)
        self.parent_profiles = parent_profiles
        self._reload_profiles()

        # TODO figure out how to create this combo box without segfaulting

        # Profile
        # self.combobox.set_model(self.config_stores)
        # self.set_entry_text_column(1)
        # self.connect("changed", self.on_profile_changed)

    def _reload_profiles(self):
        # pass
        for name, data in self.parent_profiles['byName'].iteritems():
            config_store = [name, data['file_name'], data['ListStore'], data['raw']]
            if name == self.PROFILE_DEFAULT:
                self.config_stores.prepend(config_store)
                self.profile.set_active(0)
            else:
                self.config_stores.append(config_store)


