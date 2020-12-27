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

import json
import os
import signal
import logging

import pkg_resources

from gi.repository import Gtk, Gdl

import crowbar
from crowbar import dictview
from crowbar import linkedpanes



LOGGER = logging.getLogger('crowbar.crowbar')

SETTINGS_PATH = [pkg_resources.resource_filename("crowbar", "package_data/settings/")]


class Crowbar:
    """docstring for crowbar lol"""

    extensions = {}

    def __init__(self):
        super(Crowbar, self).__init__()
        self.LOGGER = logging.getLogger('crowbar.crowbar.Crowbar')

        self.register_icons()
        self.build()
        self.load_extensions(
            os.path.join(SETTINGS_PATH[0], "default.crowbar-mountpoints")
        )

        self._demo()
        self.window.show_all()


    def _demo(self):
        geometry = list()
        geometry.append(dict(x=(-33, 33), y=(-33, 33), z=(-33, 33)))

        default_scroll_lock = True

        # linked panes
        pane_data = {
            'geometry': geometry,
            'scroll_lock': {
                'enabled': default_scroll_lock,
                'x': Gtk.Adjustment(),
                'y': Gtk.Adjustment(),
                'z': Gtk.Adjustment(),
            },
        }
        _linkedpanes = linkedpanes.LinkedPanes(
            Gtk.Label('Viewport'),
            dictview.DictView(('y', 'x'), **pane_data),
            dictview.DictView(('x', 'z'), **pane_data),
            dictview.DictView(('y', 'z'), **pane_data),
        )
        linkedpanes_container = self.builder.get_object('linkedpanes_container')
        linkedpanes_container.add(_linkedpanes)


    @staticmethod
    def register_icons():
        """
            install package_data path for gtk use
        """
        basepath = pkg_resources.resource_filename('crowbar', 'package_data/share/crowbar/icons/')
        # register icon path
        # note: actions described in the following document were attempted
        #    without success.
        #    https://wiki.gnome.org/draftspecs/themableappspecificicons

        Gtk.IconTheme.get_default().append_search_path(
            os.path.join(basepath, 'hicolor/24/mimetypes')
        )
        Gtk.IconTheme.get_default().append_search_path(
            os.path.join(basepath, 'hicolor/24/actions')
        )

    @staticmethod
    def main():
        """
            init gtk app and pass control to GTK
            (noreturn unless clean gtk main loop exit)
        """
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        Gtk.main()

    def build(self):
        """ Use GTK Glade files
        """
        builder = Gtk.Builder()
        self.builder = builder
        builder.add_from_file(
            pkg_resources.resource_filename(
                "crowbar", "package_data/crowbar.glade"
            )
        )

        builder.connect_signals(
            {
                "onDeleteWindow": Gtk.main_quit,
            }
        )

        self.window = builder.get_object("window")

    def load_extensions(self, crowbar_mountpoints):
        """ Load ui extensions
            todo: document how to integrate (based on setuptools entry_points)
        """

        # make a single dock for the entire application.
        self.extension_dock = Gdl.Dock()

        # read our settings file (this functionality may already be offered by gdl)
        with open(crowbar_mountpoints) as mountpoints:
            mountpoints = json.loads(mountpoints.read())

        for mountpoint, extensions in mountpoints.items():

            # block variables
            orientation = self.builder.get_object(mountpoint).get_orientation()
            is_horizontal = orientation.value_name == "GTK_ORIENTATION_HORIZONTAL"

            # create dock inside glade mountpoint box
            dock = Gdl.Dock.new_from(self.extension_dock, False)
            self.builder.get_object(mountpoint).add(dock)

            dock.set_hexpand(is_horizontal)
            dock.set_vexpand(not is_horizontal)

            # reverse the order in which toolbars are spawned, it makes the
            # resizing the smallest bit more sane.
            extensions.reverse()
            for extension in extensions:

                # block variables
                extension_name = extension["extension"]
                extension = crowbar.Extensions(
                    extension_name
                )
                extension.instance.icons_append_search_path()
                extension_gui = extension.gui

                # create dock item
                dock_item = Gdl.DockItem.new(
                    extension_name, extension_name, Gdl.DockItemBehavior.NORMAL
                )

                # add flags, this can probably be condensed into the
                # instantiation call if i lookup python bitwise or.
                dock_item.set_behavior_flags(Gdl.DockItemBehavior.CANT_ICONIFY, False)
                dock_item.set_behavior_flags(Gdl.DockItemBehavior.CANT_CLOSE, False)
                dock_item.set_behavior_flags(
                    Gdl.DockItemBehavior.NEVER_VERTICAL
                    if is_horizontal
                    else Gdl.DockItemBehavior.NEVER_HORIZONTAL,
                    False,
                )
                dock_item.set_behavior_flags(
                    Gdl.DockItemBehavior.CANT_DOCK_TOP
                    if is_horizontal
                    else Gdl.DockItemBehavior.CANT_DOCK_LEFT,
                    False,
                )
                dock_item.set_behavior_flags(
                    Gdl.DockItemBehavior.CANT_DOCK_BOTTOM
                    if is_horizontal
                    else Gdl.DockItemBehavior.CANT_DOCK_RIGHT,
                    False,
                )
                dock_item.set_orientation(orientation)

                # Orient things properly; Hide Toolbar buttons for horizontal elements.
                if getattr(extension_gui, "set_orientation", None):
                    extension_gui.set_orientation(orientation)
                if isinstance(extension_gui, Gtk.Toolbar) or is_horizontal:
                    dock_item.set_behavior_flags(Gdl.DockItemBehavior.NO_GRIP, False)

                dock_item.add(extension_gui)
                dock_item.set_hexpand(False if is_horizontal else True)
                dock_item.set_vexpand(False if is_horizontal else True)

                # Dock things where the settings file told us to. :D
                dock.add_item(
                    dock_item,
                    Gdl.DockPlacement.LEFT if is_horizontal else Gdl.DockPlacement.TOP,
                )
