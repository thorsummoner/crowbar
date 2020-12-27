#
#    crowbar - a geometry manipulation program
#    Copyright (C) 2020  Dylan Scott Grafmyre
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""
    crowbar - a geometry manipulation program
    Copyright (C) 2020  Dylan Scott Grafmyre
"""

import os
import importlib

try:
    import importlib.metadata as importlib_metadata
except ImportError as err:
    import importlib_metadata

from gi.repository import Gtk

class Entrypoints:
    """ practically, this is a userdict that is auto-populated from
        importlib.metadata.entry_points() for the 'crowbar_ext' namespace
        mapping entrypoint name to entrypoint object
    """
    _cache = None

    @property
    def cache(self):
        if self._cache is None:
            self._cache = {
                i.name: i for i in
                importlib_metadata.entry_points().get('crowbar_ext')
            }
        return self._cache

    def get(self, ext_name):
        entry = self.cache.get(ext_name)
        if entry is None:
            raise AssertionError('no entry point {} found'.format(('crowbar_ext', ext_name,)))
        return entry

ENTRYPOINTS = Entrypoints()

class ExtensionModules:
    modules = None

    def __init__(self):
        """ this is a container for runtime-imported modules used by
            crowbar to extend the program
        """
        self.modules = {}

    def get_module(self, name):
        if name not in self.modules:
            self.modules[name] = importlib.import_module(name)
        return self.modules[name]

EXTENSION_MODULES = ExtensionModules()



class Extensions:
    """docstring for Extensions"""

    extension_root = "extensions"

    def __init__(self, extension_name):
        super(Extensions, self).__init__()
        self.extension_name = extension_name
        self.entry_point = ENTRYPOINTS.get(extension_name)

        self.module = EXTENSION_MODULES.get_module(self.entry_point.value)

        self.gui = self.module.INSTANCE.main_gtk_widget

        if self.gui is None:
            raise AssertionError('self.gui was none after initialization with glade')
