__author__ = 'gavin'

import user_input

VERBOSE = user_input.VERBOSE
DEBUG = False


def report(msg, verb=1):
    if verb <= VERBOSE or DEBUG:
        print msg
