#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
GoLismero 2.0 - The web knife - Copyright (C) 2011-2013

Authors:
  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com
  Mario Vilas | mvilas<@>gmail.com

Golismero project site: http://code.google.com/p/golismero/
Golismero project mail: golismero.project@gmail.com

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

#----------------------------------------------------------------------
# Fix the module load path when running as a portable script and during installation.

import os
import sys
from os import path

if __name__ == "__main__" or __name__ == "golismero_launcher":
    try:
        _FIXED_PATH_
    except NameError:
        here = path.split(path.abspath(__file__))[0]
        if not here:  # if it fails use cwd instead
            here = path.abspath(os.getcwd())
        thirdparty_libs = path.join(here, "thirdparty_libs")
        if path.exists(thirdparty_libs):
            if __name__ == "__main__":
                # As a portable script: use our versions always
                sys.path.insert(0, thirdparty_libs)
                sys.path.insert(0, here)
            else:
                # When installing: prefer system version to ours
                sys.path.insert(0, here)
                sys.path.append(thirdparty_libs)
        _FIXED_PATH_ = True


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
