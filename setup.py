#!/usr/bin/env python3
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

import setuptools

setuptools.setup(
    name='crowbar',
    description=__doc__,
    license='AGPL',
    packages=[
        'crowbar',

        'crowbar.ext.filter_control',
        'crowbar.ext.map_operations',
        'crowbar.ext.map_tools',
        'crowbar.ext.map_view',
        'crowbar.ext.new_objects',
        'crowbar.ext.select_mode',
        'crowbar.ext.status_bar',
        'crowbar.ext.textures',
        'crowbar.ext.undo',
    ],
    install_requires=[
        'importlib-metadata',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'crowbar=crowbar.__main__:main',
        ],
        'gui_scripts': [
            'xcrowbar=crowbar.__main__:main',
        ],
        'crowbar_ext': [
            'filter_control=crowbar.ext.filter_control',
            'map_operations=crowbar.ext.map_operations',
            'map_tools=crowbar.ext.map_tools',
            'map_view=crowbar.ext.map_view',
            'new_objects=crowbar.ext.new_objects',
            'select_mode=crowbar.ext.select_mode',
            'status_bar=crowbar.ext.status_bar',
            'textures=crowbar.ext.textures',
            'undo=crowbar.ext.undo',
        ]
    },
)
