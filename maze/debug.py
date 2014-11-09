__author__ = 'gavin'

VERBOSE = 1
DEBUG = False


def report(msg, verb=1):
    if verb <= VERBOSE or DEBUG:
        print msg
