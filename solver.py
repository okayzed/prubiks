# solve a rubik's cube

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

TRANSFORMS = {
    LEFT: [(2, LEFT), (3, LEFT), (4, LEFT), (6, RIGHT) ],
    UP: [(1, UP), (3, UP), (5, UP), (6, UP) ],
    FRONT: [(4, UP), (5, LEFT), (2, DOWN), (1, RIGHT)],
    DOWN: [(1, DOWN), (3, DOWN), (5, DOWN), (6, DOWN) ],
    RIGHT: [(6, LEFT), (4, RIGHT), (3, RIGHT), (2, RIGHT)], # reverse order of LEFT
    BACK: [(1, LEFT), (2, UP), (5, RIGHT), (4, DOWN)], # reverse order of FRONT
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

# This isn't an exact mapping to colors since we
# can't print the exact colors. orange is replaced by cyan
COLOR_NAMES = [
    "green",
    "white",
    "red",
    "yellow",
    "blue",
    "cyan" ]

INVERT=True


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
        self.sides = [self.make_side(n, -1)] + [ self.make_side(n, COLORS[i]) for i in xrange(SIDES) ]
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

        prev = None
        last = self.get_values(*transform[-1])
        for side, col_row in transform:
            next = self.get_values(side, col_row)
            if prev:
                self.set_values(side, col_row, prev)
            prev = next

        self.set_values(transform[0][0], transform[0][1], last)

    @classmethod
    def make_side(self, n, color):
        return [ [color] * n for _ in xrange(n) ]

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


    def scramble(self, k):
        available = TRANSFORMS.keys()

        import random
        moves = []
        for _ in xrange(k):
            moves.append((random.choice(available), random.choice([True, False])))

        return moves

    def execute(self, moves, printout=True):
        for move in moves:
            c.rotate(*move)
            if printout:
                print '---'
                type = move[0]
                reverse = False
                if len(move) > 1:
                    reverse = move[1]

                print "TRANSFORM", TYPES[type] + ("'" if reverse else "")
                print '---'
                print ''

                c.print_cube()

    def distance_from_solved(self):
        if self.n != 3:
            print "DONT KNOW MID"
            return

        mid = 1
        errors = 0
        for side in self.sides:
            side_color = side[mid][mid]
            for i in xrange(self.n):
                for j in xrange(self.n):
                    if side[i][j] != side_color:
                        errors += 1

        return errors / 8.0

    def find_next(self):
        available = TRANSFORMS.keys()
        moves = []
        for move in available:
            self.rotate(move)
            s = self.serialize()
            moves.append((s, move, False, self.distance_from_solved()))
            self.rotate(move, INVERT)

        for move in available:
            self.rotate(move, INVERT)
            s = self.serialize()
            moves.append((s, move, INVERT, self.distance_from_solved()))
            self.rotate(move)

        return moves

    def serialize(self):
        lines = [""] * self.n
        for i in xrange(self.n):
            lines[i] = "".join([ "".join(map(str, self.sides[j][i])) for j in xrange(1, SIDES+1) ])

        return "\n".join(lines)

    @classmethod
    def deserialize(self, s):
        lines = s.split("\n")
        n = len(lines[0]) / 6
        sides = [self.make_side(n, -1)] + [ self.make_side(n, COLORS[i]) for i in xrange(SIDES) ]
        for i in xrange(SIDES):
            for j in xrange(n):
                sides[i+1][j] = map(int, lines[j][i*n:(i+1)*n])

        cube = Cube(n)
        cube.sides = sides
        return cube

import heapq
def solve(cube):
    d = cube.distance_from_solved()
    h = [(d, cube.serialize(), None, None, 0)]
    seen = {}
    iter = 0

    best = h[0][0]
    while h:
        distance, s, move, invert, iter = heapq.heappop(h)
        best = min(best, distance)

        if move:
            it = TYPES[move]
            if invert:
                it+= "'"

            print it, "DISTANCE:", distance, "ITER", iter, "BEST", best
        print ""
        c = Cube.deserialize(s)
        c.print_cube()
        if s in seen and seen[s] == 2:
            continue


        if iter > 100:
            continue

        if distance == 0:
            break

        moves = c.find_next()
        for s, move, invert, distance in moves:
            if s in seen:
                continue
            seen[s] = 1


            heapq.heappush(h, (distance, s, move, invert, iter+1))
        seen[s] = 2


import random
random.seed(5)
if __name__ == "__main__":
    c = Cube()
    moves = c.scramble(2)
    c.execute(moves, printout=False)

    solve(c)

    # for each move, we say it's an inverse by specifying True
    # solution = map(lambda w: (w[0], not w[1]), reversed(moves))
    # c.execute(solution, printout=False)
    # c.print_cube()

