class Point(object):
    dtol = 1e-7

    def __init__(self, x, y):
        self.coords = [0, 0]
        self.coords[0] = x
        self.coords[1] = y

    def __repr__(self):
        return "[" + str(self.coords[0]) + "," + str(self.coords[1]) + "]"

    def __getitem__(self, item):
        if item >= 2:
            raise Exception("Point index out of bounds")
        return self.coords[item]

    def __setitem__(self, key, value):
        self.coords[key] = value
        return self

    def x(self, value=None):
        if value is not None:
            self.coords[0] = value
        return self.coords[0]

    def y(self, value=None):
        if value is not None:
            self.coords[1] = value
        return self.coords[1]

    def __eq__(self, other):
        if abs(self.coords[0] - other.coords[0]) < Point.dtol and \
                abs(self.coords[1] - other.coords[1]) < Point.dtol:
            return True
        return False

    def __lt__(self, other):
        if self.coords[0] < other.coords[0]:
            return True
        elif abs(self.coords[0] - other.coords[0]) < Point.dtol:
            if self.coords[1] < other.coords[1]:
                return True
        return False

    def __gt__(self, other):
        #print "gt:",  self.coords[0], self.coords[1], " other:", other.coords[0], other.coords[1]
        if self.coords[0] > other.coords[0]:
            return True
        elif abs(self.coords[0] - other.coords[0]) < Point.dtol:
            if self.coords[1] > other.coords[1]:
                return True
        return False


    def __len__(self):
        return 2

    def dist(self, other):
        xd = self[0] - other[0]
        yd = self[1] - other[1]
        return ((xd * xd) + (yd * yd)) ** 0.5

    def __add__(self, other):
        sx = self[0] + other[0]
        sy = self[1] + other[1]
        return Point(sx, sy)

    def __sub__(self, other):
        sx = self[0] - other[0]
        sy = self[1] - other[1]
        return Point(sx, sy)

    def __neg__(self):
        return Point(-self[0], -self[1])

    def norm(self):
        return ((self[0]*self[0]) + (self[1]*self[1]))**0.5

    def normalize(self):
        n = self.norm()
        if n < 1e-7:
            raise Exception("Point is zero")
        return Point(self[0]/n, self[1]/n)


class Vertex(object):
    dtol = 1e-7

    def __init__(self, point, eid):
        self.point = point
        self.vid = eid

    def __repr__(self):
        return "Vertex id:" + str(self.vid) + \
               ",[" + str(self.point[0]) + "," + str(self.point[1]) + "]"

    def x(self, value=None):
        if value is not None:
            self.point[0] = value
        return self.point[0]

    def y(self, value=None):
        if value is not None:
            self.point[1] = value
        return self.point[1]

    def id(self, value=None):
        if value is not None:
            self.vid = value
        return self.vid

    def __getitem__(self, item):
        return self.point[item]

    def __eq__(self, other):
        if self.point == other and self.id() == other.id():
            return True
        return False

    def __lt__(self, other):
        return self.point < other

    def __gt__(self, other):
        return self.point > other

    def __len__(self):
        return len(self.point)

    def norm(self):
        return ((self[0]*self[0]) + (self[1]*self[1]))**0.5

    def dist(self, other):
        return self.point.dist(other)

    def __add__(self, other):
        return self.point + other

    def __sub__(self, other):
        return self.point - other

    def __neg__(self):
        return -self.point
