__author__ = 'gavin'

import maze


def test1():
    for n in xrange(1000):
        print "+++++++++++++++++++++++++++++++++++++++++++++"
        print "+++++++++++++++++++++++++++++++++++++++++++++"
        print "Iteration %d" % n
        mz = maze.Maze(True)
        assert mz.create()
        print "passed"
        print "+++++++++++++++++++++++++++++++++++++++++++++"
        print "+++++++++++++++++++++++++++++++++++++++++++++"


def test2():
    for n in xrange(1000):
        print "+++++++++++++++++++++++++++++++++++++++++++++"
        print "+++++++++++++++++++++++++++++++++++++++++++++"
        print "Iteration %d" % n
        mz = maze.Maze(True)
        assert mz.create()
        mz.fill_in()
        print "passed"
        print "+++++++++++++++++++++++++++++++++++++++++++++"
        print "+++++++++++++++++++++++++++++++++++++++++++++"

if __name__ == '__main__':
    test1()
    test2()
    print "All tests passed"
