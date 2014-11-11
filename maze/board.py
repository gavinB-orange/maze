__author__ = 'gavin'

import user_input
from debug import report


class Board(object):
    """
    This class implements the board - the notion of what is legal or not re. moves
    """
    _NEIGHBOURS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    _EMPTY = 0
    _START_ENDPOINT = 1
    _END_ENDPOINT = 2
    _CLOSEST = 3
    _PATH = 4

    def __init__(self, width, height):
        """
        Initialize everything - in many cases strictly temporarily.
        :param width: width of the board
        :param height: height of the board
        :return:
        """
        self.board = []
        self.height = height
        self.width = width
        self.neighbours = Board._NEIGHBOURS
        for w in xrange(self.width):
            line = []
            for h in xrange(self.height):
                line.append(0)
            self.board.append(line)
        self.closest = (None, None)
        self.closest_dist_2 = None
        self.reset_closest_dist_2()
        self.path_count = Board._PATH
        self.max_pos_iteration = self.width * self.height
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        report("Board ready", 2)

    def inc_path_count(self):
        """
        Mark the start of a new path - needed for the filling algorithm
        :return:
        """
        self.path_count += 1

    def reset_closest_dist_2(self):
        self.closest_dist_2 = self.height * self.height + self.width * self.width

    def set_start(self, pos):
        """
        Set the start position.
        :param pos: where to start
        :return:
        """
        x, y = pos
        assert x >= 0, "ERROR = start x cannot be less than 0"
        assert y >= 0, "ERROR = start y cannot be less than 0"
        assert x < self.width, "ERROR = start x cannot be greater than %d but was %d" % (self.width, x)
        assert y < self.height, "ERROR = start y cannot be greater than %d but was %d" % (self.height, y)
        self.start_x = x
        self.start_y = y
        self.closest = (x, y)
        self.board[self.start_x][self.start_y] = Board._START_ENDPOINT
        report("Start point is at (%d, %d)" % (self.start_x, self.start_y), 2)

    def set_end(self, pos):
        """
        Set the end position
        :param pos: where to end
        :return:
        """
        x, y = pos
        assert x >= 0, "ERROR = end x cannot be less than 0"
        assert y >= 0, "ERROR = end y cannot be less than 0"
        assert x < self.width, "ERROR = end x cannot be greater than %d but was %d" % (self.width, x)
        assert y < self.height, "ERROR = end y cannot be greater than %d but was %d" % (self.height, y)
        self.end_x = self.width - x - 1
        self.end_y = self.height - y - 1
        self.board[self.end_x][self.end_y] = Board._END_ENDPOINT
        report("Endpoint is at (%d, %d)" % (self.end_x, self.end_y), 2)

    def get_max_walks(self):
        """
        Get a sensible maximum number for how many walks are allowed.
         Used to catch infinite loop cases.
        :return:
        """
        return self.width * self.height

    def get_start(self):
        return self.start_x, self.start_y

    def get_end(self):
        return self.end_x, self.end_y

    def get_board(self):
        return self.board

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_neighbours(self):
        return self.neighbours

    def is_endpoint(self, move):
        return self.board[move[0]][move[1]] in (Board._START_ENDPOINT, Board._END_ENDPOINT)

    def is_end_endpoint(self, move):
        return self.board[move[0]][move[1]] == Board._END_ENDPOINT

    def is_another_corridor(self, move):
        """
        Check whether a position is another corridor
        :param move: position to check
        :return: True if another corridor
        """
        val = self.board[move[0]][move[1]]
        rr = range(Board._PATH, self.path_count)
        #return self.board[move[0]][move[1]] in range(Board._PATH, self.path_count)
        return val in rr

    def get_endpoint_values(self):
        return Board._END_ENDPOINT, Board._START_ENDPOINT

    def get_empty_val(self):
        return Board._EMPTY

    def get_closest_val(self):
        return Board._CLOSEST

    def match_for(self, x, y, values):
        """
        Return OK iff value of [x][y] is in the tuple provided
        :param x: x position
        :param y: y position
        :param values: list of acceptable values
        :return: True if there's a match else False
        """
        try:
            val = self.board[x][y]
            return val in values
        except KeyError:
            return False

    def check_valid_neighbours(self, pos, valid, offboard_ok=True):
        """
        Check out the neighbours
        :param pos: where we are
        :param valid: who is vaid
        :param offboard_ok: how you treat a neighbour that is off the board
        :return:
        """
        count = 0
        for to_check in self.get_neighbours():
            xx = to_check[0] + pos[0]
            yy = to_check[1] + pos[1]
            if (xx < 0) or (xx >= self.width):
                if offboard_ok:
                    count += 1  # off board = ok
                continue
            if (yy < 0) or (yy >= self.height):
                if offboard_ok:
                    count += 1  # off board = ok
                continue
            if self.match_for(xx, yy, valid):
                count += 1
        return count

    def is_a_wall(self, x, y):
        """
        Return true if [x][y] is next to a previous opening
        :param x: x position
        :param y: y position
        :return: True if is a wall
        """
        #count = self.check_valid_neighbours((x, y), (Board._EMPTY, Board._END_ENDPOINT))
        count = self.check_valid_neighbours((x, y), range(self.path_count))
        return count < 3

    def get_legal(self, x, y, fill_in=False):
        """
        Get the list of legal neighbours
        :param x: x position
        :param y: y position
        :param fill_in: fill_in mode is a bit different
        :return: list
        """
        poss = []
        for to_check in self.get_neighbours():
            xx = to_check[0] + x
            yy = to_check[1] + y
            if (xx < 0) or (xx >= self.width):
                continue
            if (yy < 0) or (yy >= self.height):
                continue
            if fill_in:
                if self.match_for(xx, yy, range(self.path_count)) and not self.is_a_wall(xx, yy):
                    poss.append((xx, yy))
            else:
                if self.match_for(xx, yy, (Board._EMPTY, Board._END_ENDPOINT)) and not self.is_a_wall(xx, yy):
                    poss.append((xx, yy))
        return poss

    def dist_2(self, move):
        return (self.end_x - move[0]) * (self.end_x - move[0]) +\
               (self.end_y - move[1]) * (self.end_y - move[1])

    def take_move(self, move):
        """
        Take the move - which means updating the closest info
        :param move: where to move to
        :return:
        """
        report("moved to %s" % str(move), 2)
        self.board[move[0]][move[1]] = self.path_count
        d2 = self.dist_2(move)
        if d2 < self.closest_dist_2:  # switch closest marker
            self.board[self.closest[0]][self.closest[1]] = self.path_count
            self.closest = move
            self.board[self.closest[0]][self.closest[1]] = Board._CLOSEST
            self.closest_dist_2 = d2
            report("closest pos updated = %s as d2 now %d" % (str(self.closest), d2), 2)

    def closest_as_str(self):
        return str(self.closest)

    def get_start_pos(self):
        """
        Find a location with EMPTY in all 4 directions
        :return:(x, y) tuple of location, or None
        """
        report("looking for space to start a corridor from", 2)
        for x in xrange(len(self.board)):
            for y in xrange(len(self.board[x])):
                # an isolation cross can cause a trap without these next 2 lines as it is seen as a valid
                # start pos, but there are no legal moves. I avoid this by marking the position as taken via
                # a take_move(p) and here I explicitly check whether I've already stood here before and move
                # on if so
                if self.board[x][y] == self.path_count:
                    report("I see footsteps : %d" % self.path_count, 2)
                    continue
                pos = (x, y)
                count = self.check_valid_neighbours(pos, [Board._EMPTY], offboard_ok=False)
                if count == 4:
                    report("found valid pos %s" % str(pos), 2)
                    self.max_pos_iteration -= 1
                    if self.max_pos_iteration < 1:
                        return "DEBUG_FLAG"
                    return pos
        return None

    def get_forced_step(self, start):
        """
        walk one step closer to the destination - no matter what is in the way
        :param start : where we start
        :return:the step taken
        """
        delta_x = self.end_x - start[0]
        delta_y = self.end_y - start[1]
        if delta_x > 0:
            x = start[0] + 1
            if (x >= 0) and (x < self.width):
                return x, start[1]
        if delta_x < 0:
            x = start[0] - 1
            if (x >= 0) and (x < self.width):
                return x, start[1]
        if delta_y < 0:
            y = start[1] - 1
            if (y > 0) and (y < self.height):
                return start[0], y
        if delta_y > 0:
            y = start[1] + 1
            if (y > 0) and (y < self.height):
                return start[0], y
