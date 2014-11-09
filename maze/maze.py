#!/usr/bin/python

__author__ = 'gavin'


'''
top level file that starts the entire maze creator
'''

import walker
import display
import board


class Maze(object):
    """
    Covers the top level integration of the various components
    """
    def __init__(self):
        self.board = board.Board()
        self.walk = walker.Walker(self, self.board)
        self.disp = display.Display(self.board)
        self.board.set_start(0, 4)
        self.board.set_end(0, 3)
        print "Maze ready"

    def create(self):
        return self.walk.create()

    def fill_in(self):
        return self.walk.fill_in()

    def display(self):
        return self.disp.show()


if __name__ == '__main__':
    mz = Maze()
    mz.create()
    mz.display()
    mz.fill_in()
    mz.display()
