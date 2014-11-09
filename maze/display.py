__author__ = 'gavin'

'''
Covers the display of the maze
'''

#import pygame


class Display(object):
    """
    handle all display aspects
    """

    def __init__(self, bd):
        self.board = bd
        print "Display ready"

    def show(self):
        print "Display of board"
        bd = self.board.get_board()
        hr = '=' * self.board.get_height()
        print hr
        for xpart in bd:
            line = ""
            for value in xpart:
                if value == self.board.get_empty_val():
                    line = "%s%s" % (line, "#")
                    continue
                if value in self.board.get_endpoint_values():
                    line = "%s%s" % (line, "@")
                    continue
                if value == self.board.get_closest_val():
                    line = "%s%s" % (line, "C")
                    continue
                line = "%s%s" % (line, ".")
            print line
        print hr
