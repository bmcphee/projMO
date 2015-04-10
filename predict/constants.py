#!/usr/bin/env python3

import os

RESOURCES_DIR       = 'resources'
SENTINEL            = '$'
DEFAULT_DICT        = 'wordlist.txt'
DEFAULT_FUZZINESS   = 60.0
EXIT_CHAR           = '!'

DEFAULT_DICT_FILE   = os.path.join(RESOURCES_DIR, DEFAULT_DICT)
