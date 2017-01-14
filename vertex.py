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

    def x(self, value=None):
        if value is not None:
            self.coords[0] = value
        return self.coords[0]

    def y(self, value=None):
        if value is not None:
            self.coords[y] = value
        return self.coords[1]

    def __eq__(self, other):
        if abs(self.coords[0]-other.coords[0]) < Point.dtol and \
           abs(self.coords[1]-other.coords[1]) < Point.dtol:
            return true
        return false


class Vertex(object):
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
