__author__ = 'gavin'

import debug
import random

from debug import report


class Walker(object):
    """
    The mad miner
    """

    def __init__(self, mz, bd):
        self.maze = mz
        self.board = bd
        self.x = None
        self.y = None
        self.orig_x = None
        self.orig_y = None
        report("Walker ready")

    def get_legal_moves(self, fill_in=False):
        possibles = self.board.get_legal(self.x, self.y, fill_in=fill_in)
        return possibles

    def take_a_walk(self, fill_in=False):
        """
        Do a single walk action. This may well result in a dead end
        :return:True if you find the endpoint, False if no more moves.
        """
        report("Mad miner takes a walk from (%d, %d)" % (self.x, self.y), 2)
        self.board.inc_path_count()
        while True:
            legal_moves = self.get_legal_moves(fill_in=fill_in)
            report("%d legal moves" % len(legal_moves), 2)
            if len(legal_moves) < 1:
                report("No legal moves left", 2)
                return False
            if fill_in:
                # take a neighbouring corridor if not mine
                for move in legal_moves:
                    if self.board.is_another_corridor(move):
                        report("found another corridor - moving there", 2)
                        (self.x, self.y) = move
                        self.board.take_move(move)
                        return True
            else:
                # take endpoint if nearby
                for move in legal_moves:
                    if self.board.is_end_endpoint(move):
                        report("found the endpoint - moving there", 2)
                        (self.x, self.y) = move
                        self.board.take_move(move)
                        return True
            # ok - choose a random one
            choice = random.randint(0, len(legal_moves) - 1)
            move = legal_moves[choice]
            self.x, self.y = move
            self.board.take_move(move)

    def take_a_fill_in_walk(self):
        """
        Take a walk from an unused space to any corridor
        """
        report("Mad miner takes a fill in walk from (%d, %d)" % (self.x, self.y), 2)
        return self.take_a_walk(fill_in=True)

    def did_not_move(self):
        return (self.x == self.orig_x) and (self.y == self.orig_y)

    def forced_step(self):
        """
        Ignore normal rules and take a step closer
        :return:
        """
        report("Taking a forced step", 2)
        move = self.board.get_forced_step((self.x, self.y))
        self.x, self.y = move
        self.board.take_move(move)

    def create(self):
        """
        create a path from beginning to end.
        It works by a number of successive random walks, each starting at the closest
        point the previous walk got to (or the starting point for the first time).
        :return:True if successful, else False
        """
        sanity_count_max = self.board.get_max_walks()
        (self.x, self.y) = self.board.get_start()
        finished = self.take_a_walk()
        if finished:
            print "Finished maze"
        while not finished:
            if debug.DEBUG:
                self.maze.display()
            report("more to go.", 2)
            report("closest position is %s" % self.board.closest_as_str(), 2)
            sanity_count_max -= 1
            report("attempts left = %d" % sanity_count_max, 2)
            if sanity_count_max < 0:
                print "too many iterations - bug"
                return False
            self.orig_x, self.orig_y = self.x, self.y
            self.x, self.y = self.board.closest
            self.board.reset_closest_dist_2()  # redundant, but safe.
            finished = self.take_a_walk()
            if finished:
                print "Finished maze"
            if self.did_not_move():
                self.forced_step()
        return True

    def fill_in(self):
        """
        Do something about all that filled in space.
        :return:
        """
        ok = True
        print "Starting to fill in the non-used space"
        p = self.board.get_start_pos()
        while p is not None:
            self.board.take_move(p)
            report("Start pos is %s" % str(p), 2)
            (self.x, self.y) = p
            ok = ok and self.take_a_fill_in_walk()
            p = self.board.get_start_pos()
        return ok
