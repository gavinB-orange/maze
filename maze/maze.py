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

from debug import report


class Maze(object):
    """
    Covers the top level integration of the various components
    """
    def __init__(self, test=False):
        """
        Setup - instantiate the board, set the start / end points
        and get the appropriate display object based upon the value from
        user_input.
        :param test: if True it signals e.g. not to wait for the user to
                     quit the display,
        :return:
        """
        self.test = test
        self.board = board.Board(user_input.BOARD_WIDTH, user_input.BOARD_HEIGHT)
        self.walk = walker.Walker(self, self.board)
        self.endpoint_start_pos = (0, random.randint(0, self.board.get_height() - 1))
        self.endpoint_end_pos = (0, random.randint(0, self.board.get_height() - 1))
        self.board.set_start(self.endpoint_start_pos)
        self.board.set_end(self.endpoint_end_pos)
        # choose the appropriate display type and initialize
        assert user_input.DISPLAY_TYPE in user_input.ALLOWED_DISPLAY_TYPES, "unknown display type chosen"
        if user_input.DISPLAY_TYPE == "text":
            self.disp = display.Display(self.board)
        if user_input.DISPLAY_TYPE == "tk":
            self.disp = display.TkDisplay(self.board)
            self.disp.set_cell_dimensions(user_input.CELL_WIDTH, user_input.CELL_HEIGHT)
            self.disp.set_colours(background=user_input.BACKGROUND_COLOUR,
                                  cell_colour=user_input.CELL_COLOUR,
                                  endpoint_colour=user_input.ENDPOINT_COLOUR)
        if user_input.DISPLAY_TYPE == "pygame":
            self.disp = display.PygameDisplay(self.board)
            self.disp.set_cell_dimensions(user_input.CELL_WIDTH, user_input.CELL_HEIGHT)
            self.disp.set_colours(background=user_input.BACKGROUND_COLOUR,
                                  cell_colour=user_input.CELL_COLOUR,
                                  endpoint_colour=user_input.ENDPOINT_COLOUR)
        report("Maze ready", 2)

    def create(self):
        return self.walk.create()

    def fill_in(self):
        self.walk.fill_in()

    def redraw_endpoints(self):
        self.board.set_start(self.endpoint_start_pos)
        self.board.set_end(self.endpoint_end_pos)

    def display(self):
        return self.disp.show(self.test)

def run_maze():
    mz = Maze()
    mz.create()
    if user_input.SHOW_INTERMEDIATE_MAZE:
        mz.display()
    mz.fill_in()
    mz.redraw_endpoints()
    mz.display()

if __name__ == '__main__':
    run_maze()
