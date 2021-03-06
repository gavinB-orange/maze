__author__ = 'gavin'

'''
Covers the display of the maze
'''

from debug import report
from Tkinter import *
import pygame


class Display(object):
    """
    handle all display aspects
    """

    def __init__(self, bd):
        """
        :param bd : board to use for the display
        """
        self.board = bd
        report("Display ready", 2)

    def set_cell_dimensions(self, cw, ch):
        """
        set the cell width and height, and also re-calculate the
        overall display dimensions.
        Not actually used by the basic version, but used by the descendants
        :param cw : width
        :param ch : height
        """
        self.cell_width = cw
        self.cell_height = ch
        self.display_width = self.board.get_width() * self.cell_width
        self.display_height = self.board.get_height() * self.cell_height

    def set_colours(self, background="white", cell_colour="blue", endpoint_colour="red"):
        """
        sets the colours. Sensible defaults.
        Not used by the basic version, but used by descendants
        :param : background for background colour
        :param : cell_colour for the colour to draw the cells
        :param : endpoint_colour for the colour to draw the endpoints
        """
        self.background_colour = background
        self.cell_colour = cell_colour
        self.endpoint_colour = endpoint_colour

    def show(self, test):
        """
        The main action of a Display object. This is a basic
        text version intended to be over-ridden by a more
        sophisticated version.
        :param test : signals that in test mode. Interpretation is left to each implementation.
        """
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
    _BLOCK_WIDTH = 10   # defaults which can / will be over-written
    _BLOCK_HEIGHT = 10

    def __init__(self, bd):
        """
        Cover the necessary initialisation of the display
        :param bd: board to display
        """
        Display.__init__(self, bd)
        self.cell_height = TkDisplay._BLOCK_HEIGHT
        self.cell_width = TkDisplay._BLOCK_WIDTH
        self.display_width = self.board.get_width() * self.cell_width
        self.display_height = self.board.get_height() * self.cell_height
        self.endpoint_colour = None
        self.cell_colour = None
        self.background_colour = None
        self.set_colours()



    def show(self, test):
        """
        draw the maze using Tk
        :param : test to signal test mode.
        """
        master = Tk()
        w = Canvas(master, width=self.display_width, height=self.display_height)
        w.pack()
        boxes = self.board.get_board()
        for x in xrange(self.board.get_width()):
            for y in xrange(self.board.get_height()):
                colour = self.background_colour  # default value
                if boxes[x][y] == self.board.get_empty_val():
                    colour = self.cell_colour
                else:
                    if boxes[x][y] in self.board.get_endpoint_values():
                        colour = self.endpoint_colour
                w.create_rectangle(x * self.cell_width,
                                   y * self.cell_height,
                                   (x+1) * self.cell_width,
                                   (y+1) * self.cell_height,
                                   fill=colour)
        if not test:
            mainloop()


class PygameDisplay(Display):
    """
    Uses pygame to display the maze
    """
    def __init__(self, bd):
        """
        sets things up.
        :param - bd : the board to display
        """
        Display.__init__(self, bd)
        self.cell_height = None
        self.cell_width = None
        self.display_width = None
        self.display_height = None
        self.endpoint_colour = None
        self.cell_colour = None
        self.background_colour = None
        self.set_colours()
        pygame.init()
        self.screen = None

    def name_to_color(self, col):
        """
        A bit of a horrible hack, but I need a mapping from name to color
        :param col : text reference to a known RGBA setting
        :return the pygame.Color corresponding to the value passed.
        """
        if col == "red":
            return pygame.Color(255, 0, 0, 255)
        if col == "green":
            return pygame.Color(0, 255, 0, 255)
        if col == "blue":
            return pygame.Color(0, 0, 255, 255)
        if col == "yellow":
            return pygame.Color(255, 255, 0, 255)
        if col == "white":
            return pygame.Color(255, 255, 255, 255)
        if col == "black":
            return pygame.Color(0, 0, 0, 255)
        if col == "silver":
            return pygame.Color(200, 200, 200, 255)
        if col == "grey":
            return  pygame.Color(128, 128, 128, 255)
        if col == "orange":
            return pygame.Color(255, 265, 0, 255)
        assert False, "unknown colour"

    def set_cell_dimensions(self, cw, ch):
        """
        :param cw : width
        :param ch : height
        """
        Display.set_cell_dimensions(self, cw, ch)
        self.screen = pygame.display.set_mode((self.display_width, self.display_height))

    def set_colours(self, background="white", cell_colour="blue", endpoint_colour="red"):
        self.background_colour = self.name_to_color(background)
        self.cell_colour = self.name_to_color(cell_colour)
        self.endpoint_colour = self.name_to_color(endpoint_colour)

    def show(self, test):
        """
        draw the maze using pygame
        :param test : if true, in test mode, so don't wait for user input
        """
        while 1:
            self.screen.fill(self.background_colour)
            boxes = self.board.get_board()
            for x in xrange(self.board.get_width()):
                for y in xrange(self.board.get_height()):
                    colour = self.background_colour  # default value
                    if boxes[x][y] == self.board.get_empty_val():
                        colour = self.cell_colour
                    else:
                        if boxes[x][y] in self.board.get_endpoint_values():
                            colour = self.endpoint_colour
                    rect = pygame.Rect(x * self.cell_width,
                                       y * self.cell_height,
                                       self.cell_width,
                                       self.cell_height)
                    pygame.draw.rect(self.screen,
                                     colour,
                                     rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        sys.exit()
            if test:
                break



