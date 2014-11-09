#!/usr/bin/python

__author__ = 'gavin'


'''
top level file that starts the entire maze creator
'''

import random
import walker
import display
import board
import user_input


class Maze(object):
    """
    Covers the top level integration of the various components
    """
    def __init__(self, test=False):
        self.test = test
        self.board = board.Board(user_input.BOARD_WIDTH, user_input.BOARD_HEIGHT)
        self.walk = walker.Walker(self, self.board)
        assert user_input.DISPLAY_TYPE in user_input.ALLOWED_DISPLAY_TYPES, "unknown display type chosen"
        if user_input.DISPLAY_TYPE == "text":
            self.disp = display.Display(self.board)
        if user_input.DISPLAY_TYPE == "tk":
            self.disp = display.TkDisplay(self.board)
        self.endpoint_start_pos = (0, random.randint(0, self.board.get_height() - 1))
        self.endpoint_end_pos = (0, random.randint(0, self.board.get_height() - 1))
        self.board.set_start(self.endpoint_start_pos)
        self.board.set_end(self.endpoint_end_pos)
        print "Maze ready"

    def create(self):
        return self.walk.create()

    def fill_in(self):
        self.walk.fill_in()

    def redraw_endpoints(self):
        self.board.set_start(self.endpoint_start_pos)
        self.board.set_end(self.endpoint_end_pos)

    def display(self):
        return self.disp.show(self.test)

if __name__ == '__main__':
    mz = Maze()
    mz.create()
    if user_input.SHOW_INTERMEDIATE_MAZE:
        mz.display()
    mz.fill_in()
    mz.redraw_endpoints()
    mz.display()
