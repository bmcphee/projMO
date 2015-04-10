#!/usr/bin/env python3

import sys
from optparse import OptionParser

# Local module
import constants

def cli_parser():
    parser = OptionParser()
    parser.add_option('-f', '--fuzziness', default=constants.DEFAULT_FUZZINESS, help='fuzziness')
    parser.add_option('-d', '--dict', default=constants.DEFAULT_DICT_FILE, help='default dict')

    args, options = parser.parse_args()

    return args, options
