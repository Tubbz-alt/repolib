#!/usr/bin/python3

"""
Copyright (c) 2019-2020, Ian Santopietro
All rights reserved.

This file is part of RepoLib.

RepoLib is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

RepoLib is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with RepoLib.  If not, see <https://www.gnu.org/licenses/>.
"""

from enum import Enum
from pathlib import Path

SOURCES_DIR = '/etc/apt/sources.list.d'
TESTING = False

class RepoError(Exception):
    """ Exception from this module."""

    def __init__(self, *args, code=1, **kwargs):
        """Exception with a source object

        Arguments:
            code (:obj:`int`, optional, default=1): Exception error code.
    """
        super().__init__(*args, **kwargs)
        self.code = code

try:
    import lsb_release
    DISTRO_CODENAME = lsb_release.get_distro_information()['CODENAME']
except ImportError:
    DISTRO_CODENAME = 'linux'

class AptSourceType(Enum):
    """ Helper Enum to simplify saving data. """
    BINARY = "deb"
    SOURCE = "deb-src"

class AptSourceEnabled(Enum):
    """ Helper Enum to translate between bool data and the Deb822 format. """
    TRUE = 'yes'
    FALSE = 'no'

    def get_bool(self):
        """ Return a bool based on the value. """
        # pylint: disable=comparison-with-callable
        # This doesnt seem to actually be a callable in this case.
        if self.value == "yes":
            return True

        return False

CLEAN_CHARS = {
    33: None,
    64: 45,
    35: 45,
    36: 45,
    37: 45,
    94: 45,
    38: 45,
    42: 45,
    41: None,
    40: None,
    43: 45,
    61: 45,
    91: None,
    92: None,
    93: None,
    123: None,
    125: None,
    124: 95,
    63: None,
    47: 95,
    46: 45,
    60: 95,
    62: 95,
    44: 95,
    96: None,
    126: None,
    32: 95,
    58: None,
    59: None,
}

def get_sources_dir(testing=False):
    """ Get the path to the sources dir.

    Returns:
        pathlib.Path: The Sources dir.
    """
    # pylint: disable=global-statement
    # We want to stop using the old dir and use the testing dir on subsequent
    # calls.
    if testing:
        global SOURCES_DIR
        SOURCES_DIR = '/tmp/repolib_testing'
    # pylint: enable=global-statement
    sources_dir = Path(SOURCES_DIR)
    sources_dir.mkdir(parents=True, exist_ok=True)
    return sources_dir

def validate_debline(valid):
    """ Basic checks to see if a given debline is valid or not.

    Arguments:
        valid (str): The line to validate.

    Returns:
        True if the line is valid, False otherwise.
    """
    valid = valid.strip()
    if valid.startswith('#'):
        valid = valid.replace('#', '')

    valid = valid.strip()

    if valid.startswith('deb'):
        return True

    return False
