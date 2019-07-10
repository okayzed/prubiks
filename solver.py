# solve a rubik's cube

# how it works?
# cube is represented as six sides
#   2
# 1 3 5 6
#   4

# 1 is LEFT
# 2 is UP
# 3 is FRONT (FACING US)
# 4 is DOWN
# 5 is RIGHT
# 6 is BACK (away from us)

# to rotate a side we: rotate that side by 90 degrees (transpose), then
# we rotate the 4 connected faces
# if we rotate 1, we are rotating 2346 left column
# if we rotate 2, we rotate the top row of 1356
# if we rotate 3, we rotate 1245 top
# if we rotate 4: we are rotating 1356 bottom
# if we rotate 5: we rotate 2346 right
# if we rotate 6: we rotate rotate 1245 bottom

# if we rotate 1:
# 2L -> 3L -> 4L -> 6L
# if we rotate 2:
# 1T -> 3T -> 5T -> 6T
# if we rotate 3, then:
# 1R -> 2B -> 5L -> 4T
# if we rotate 4:
# 1B -> 3B -> 5B -> 6B
# if we rotate 5:
# 2R -> 3R -> 4R -> 6R
# if we rotate 6:
# 1L -> 2T -> 5R -> 4B

# 1 green
# 2 white
# 3 red
# 4 yellow
# 5 blue
# 6 orange

LEFT=1
UP=2
FRONT=3
DOWN=4
RIGHT=5
BACK=6

GREEN  = 1
WHITE  = 2
RED    = 3
YELLOW = 4
BLUE   = 5
ORANGE = 6
SIDES  = 6

import colorama
import termcolor
colorama.init()

# NEED TO PROPERLY TRANSPOSE MATRIX DEPENDING ON WHICH SIDE IS BEING ROTATED
TRANSFORMS = {
    LEFT: [(2, LEFT), (3, LEFT), (4, LEFT), (6, RIGHT) ],
    UP: [(1, UP), (3, UP), (5, UP), (6, UP) ],
    FRONT: list(reversed([(1, RIGHT), (2, DOWN), (5, LEFT), (4, UP)])),
    DOWN: [(1, DOWN), (3, DOWN), (5, DOWN), (6, DOWN) ],
    RIGHT: list(reversed([(2, RIGHT), (3, RIGHT), (4, RIGHT), (6, LEFT) ])),
    BACK: [(1, LEFT), (2, UP), (5, RIGHT), (4, DOWN)],
}

TYPES = {
    LEFT: "left",
    RIGHT: "right",
    UP: "up",
    DOWN: "down",
    FRONT: "front",
    BACK: "back"
}

COLORS = [
    GREEN,
    WHITE,
    RED,
    YELLOW,
    BLUE,
    ORANGE ]

COLOR_NAMES = [
    "green",
    "white",
    "red",
    "yellow",
    "blue",
    "cyan" ]


def rotate_matrix_ccw(m):
    n = len(m) - 1

    for k in xrange(len(m) / 2):
        for i in xrange(n - k*2):
            a = m[k][i+k]
            b = m[i+k][n-k]
            c = m[n-k][n-i-k]
            d = m[n-i-k][k]

            m[i+k][n-k] = c
            m[n-k][n-i-k] = d
            m[n-i-k][k] = a
            m[k][i+k] = b

    return m


def rotate_matrix_cw(m):
    n = len(m) - 1

    for k in xrange(len(m) / 2):
        for i in xrange(n - k*2):
            a = m[k][i+k]
            b = m[i+k][n-k]
            c = m[n-k][n-i-k]
            d = m[n-i-k][k]

            m[i+k][n-k] = a
            m[n-k][n-i-k] = b
            m[n-i-k][k] = c
            m[k][i+k] = d

    return m


class Cube:
    def __init__(self, n=3):
        self.n = n
        self.sides = [self.make_side(-1)] + [ self.make_side(COLORS[i]) for i in xrange(SIDES) ]
        self.printout = [ [' '] * n * 4 for _ in xrange(4)]

    def set_values(self, side, tr, values):
        if tr == DOWN:
            for i in xrange(self.n):
                self.sides[side][-1][i] = values[i]
        if tr == UP:
            for i in xrange(self.n):
                self.sides[side][0][i] = values[i]
        if tr == LEFT:
            for i in xrange(self.n):
                self.sides[side][i][0] = values[i]
        if tr == RIGHT:
            for i in xrange(self.n):
                self.sides[side][i][-1] = values[i]

    def get_values(self, side, tr):
        ret = []
        if tr == DOWN:
            for i in xrange(self.n):
                ret.append(self.sides[side][-1][i])
        if tr == UP:
            for i in xrange(self.n):
                ret.append(self.sides[side][0][i])
        if tr == LEFT:
            for i in xrange(self.n):
                ret.append(self.sides[side][i][0])
        if tr == RIGHT:
            for i in xrange(self.n):
                ret.append(self.sides[side][i][-1])
        return ret

    def rotate(self, type, reverse=False):
        transform = TRANSFORMS[type]
        if reverse:
            self.sides[type] = rotate_matrix_ccw(self.sides[type])
            transform = list(reversed(transform))
        else:
            self.sides[type] = rotate_matrix_cw(self.sides[type])
       
        print '---'
        print "TRANSFORM", TYPES[type] + ("'" if reverse else "")
        print '---'
        print ''

        prev = None
        last = self.get_values(*transform[-1])
        for side, col_row in transform:
            next = self.get_values(side, col_row)
            if prev:
                self.set_values(side, col_row, prev)
            prev = next

        self.set_values(transform[0][0], transform[0][1], last)



    def make_side(self, color):
        return [ [color] * self.n for _ in xrange(self.n) ]

    def print_side(self, i):
        for j in xrange(self.n):
            print ''.join(map(str, self.sides[i][j]))
        print ''

    def print_blank(self):
        for _ in xrange(self.n):
            print ''.join([' '] * self.n)
        print ''

    def print_sides(self, sides):
        n = self.n+1
        buf = [ [' '] * len(sides) * n for _ in xrange(self.n)]

        for i, side in enumerate(sides):
            if side > 0:
                face = self.sides[side]

                # if we are on side six, we reverse the entries horizontally
                # because side 6 is on the back
                if side == 6:
                    face = [ list(reversed(r)) for r in face ]

                for j in xrange(self.n):
                    for k in xrange(self.n):
                        v = face[j][k]
                        if v:
                            bg = "on_%s" % (COLOR_NAMES[v-1])
                            buf[j][i*n+k] = termcolor.colored(" ", "white", bg)

        print '\n'.join([ ''.join(map(str, b)) for b in buf])
        print ''
                

    def print_cube(self):
        self.print_sides([0,2,0,0])
        self.print_sides([1,3,5,6])
        self.print_sides([0,4,0,0])


available = TRANSFORMS.keys()

import random
moves = []
for _ in xrange(5):
    moves.append(random.choice(available))

c = Cube()
c.print_cube()

for move in moves:
    c.rotate(move)
    c.print_cube()

print "GOING BACKWARDS"

for move in reversed(moves):
    c.rotate(move, True)
    c.print_cube()

