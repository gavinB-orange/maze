__author__ = 'gavin'

'''
Covers the display of the maze
'''

from Tkinter import *
#import pygame


class Display(object):
    """
    handle all display aspects
    """

    def __init__(self, bd):
        self.board = bd
        print "Display ready"

    def show(self, test):
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


class TkDisplay(Display):
    """
    This uses Tk to display the maze
    """
    _BLOCK_WIDTH = 10
    _BLOCK_HEIGHT = 10

    def __init__(self, bd):
        Display.__init__(self, bd)
        self.display_width = self.board.get_width() * TkDisplay._BLOCK_WIDTH
        self.display_height = self.board.get_height() * TkDisplay._BLOCK_HEIGHT


    def show(self, test):
        """
        draw the maze using Tk
        """
        master = Tk()
        w = Canvas(master, width=self.display_width, height=self.display_height)
        w.pack()
        boxes = self.board.get_board()
        for x in xrange(self.board.get_width()):
            for y in xrange(self.board.get_height()):
                if boxes[x][y] == self.board.get_empty_val():
                    colour = "blue"
                else:
                    if boxes[x][y] in self.board.get_endpoint_values():
                        colour = "red"
                    else:
                        colour = "white"
                w.create_rectangle(x * TkDisplay._BLOCK_WIDTH,
                                   y * TkDisplay._BLOCK_HEIGHT,
                                   (x+1) * TkDisplay._BLOCK_WIDTH,
                                   (y+1) * TkDisplay._BLOCK_HEIGHT,
                                   fill=colour)
        if not test:
            mainloop()

