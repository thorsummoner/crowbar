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

from crowbar.crowbar import crowbar

# statusbar = Extensions('StatusBar')

if '__main__' == __name__:
	app = crowbar()
	app.main()


