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

import logging
import os

import pkg_resources

from gi.repository import Gtk

class BaseExtension:
    builder = None
    pkg_resources_module = None
    pkg_resources_prefix = None
    main_glade_object_name = None

    def __init__(self):
        self.LOGGER = logging.getLogger(self.__class__.__name__)

    @property
    def glade_filename(self):
        raise NotImplementedError

    @property
    def main_gtk_widget(self):
        if self.builder is None:
            self.LOGGER.info('Gtk.Builder()')
            self.builder = Gtk.Builder()

            self.LOGGER.info('Gtk.Builder.add_from_file(%s)', self.glade_filename)
            self.builder.add_from_file(self.glade_filename)
            # builder.connect_signals(Handler())
            self.LOGGER.info('Gtk.Builder.get_object(%s)', self.main_glade_object_name)

        widget = self.builder.get_object(self.main_glade_object_name)
        if widget == None:
            raise AssertionError('Gtk.Builder returned None')

        return widget

    def icons_append_search_path(self):
        pass


class CoreExtension(BaseExtension):
    pkg_resources_module = 'crowbar'

    @property
    def main_glade_object_name(self):
        return self.__class__.__name__
    @property
    def glade_filename(self):
        return pkg_resources.resource_filename(
            self.pkg_resources_module,
            os.path.join(
                self.pkg_resources_prefix,
                '{}.glade'.format(self.__class__.__name__)
            )
        )

