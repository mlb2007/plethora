from vertex import Vertex
import math
import sys


def cross(a, b):
    c = a[0] * b[1] - a[1] * b[0]
    return c


def dot(a, b):
    c = a[0] * b[0] + a[1] * b[1]
    return c


def inner_angle(a, b):
    c = cross(a, b)
    d = dot(a, b)
    ad = a.norm()
    bd = b.norm()
    if ad == 0:
        raise Exception("zero")
    if bd == 0:
        raise Exception("zero")
    cosp = d / (ad * bd)
    return math.acos(cosp)


def angle_c(a, b):
    inner = inner_angle(a, b)
    det = cross(a, b)
    if det < 0:
        return inner
    else:
        return (2.0 * math.pi) - inner


# enum
class EdgeType(object):
    eLineSegment = 0
    eCircularArc = 1
    repr = ['LineSegment', 'CircularArc']

    def __repr__(self):
        return "EdgeType"


class Edge(object):
    def __init__(self, *args, **kwargs):
        self.etype = None
        self.vertices = list()
        for vertex in args:
            self.vertices.append(vertex)
        for k, v in kwargs.iteritems():
            if k == 'id':
                self.id = v
            elif k == 'type':
                self.etype = v
            else:
                raise Exception("Unknown value input as argument(s)")

    def __repr__(self):
        repr = "Edge," + " type:" + str(self.etype) + "\n"
        for v in self.vertices:
            repr += "\t" + v.__repr__() + "\n"
        return repr

    def __getitem__(self, item):
        return self.vertices[item]

    def vertex(self, index):
        if index >= len(self.vertices):
            raise Exception("vertex index out of bounds")
        return self.vertices[index]

    def start(self):
        return self.vertices[0]

    def end(self):
        return self.vertices[-1]

    def type(self, edge_type=None):
        if edge_type is not None:
            self.etype = edge_type
        return self.etype

    def length(self):
        return self[0].dist(self[1])

    def padded_area(self, pad_dist):
        return self.length()*pad_dist

class LineSegment(Edge):
    def __init__(self, start_vertex, end_vertex, id):
        super(LineSegment, self).__init__(start_vertex, end_vertex, id=id)
        super(LineSegment, self).type(EdgeType.eLineSegment)

    def __repr__(self):
        repr = "Edge," + " type:" + "LineSegment, id:" + str(self.id) + "\n"
        for v in self.vertices:
            repr += "\t" + v.__repr__() + "\n"
        return repr

    def radius(self):
        return float("inf")


class CircularArc(Edge):
    def __init__(self, start_vertex, end_vertex, center, id, clockwise_from=None):
        super(CircularArc, self).__init__(start_vertex, end_vertex, id=id)
        super(CircularArc, self).type(EdgeType.eCircularArc)
        if clockwise_from is None:
            self.c_clockwise_from = start_vertex.id()
        else:
            self.c_clockwise_from = clockwise_from
        self.c_center = center
        # the not clockwise vertex ..
        self.other_vtx = None
        if start_vertex.id() != self.c_clockwise_from:
            self.other_vtx = start_vertex
        else:
            self.other_vtx = end_vertex

        self.area_sign = 1.0

    def __repr__(self):
        repr = "Edge," + " type:" + "CircularArc, id:" + str(self.id) + "\n"
        for v in self.vertices:
            repr += "\t" + v.__repr__() + "\n"
        repr += "\tcenter:[" + str(self.c_center[0]) + "," + str(self.c_center[1]) + "]\n"
        repr += "\tClockwiseFrom (id):" + str(self.c_clockwise_from) + "\n"
        return repr

    def center(self, circle_center=None):
        if circle_center is not None:
            self.c_center = circle_center
        return self.c_center

    def clockwisefrom(self, vertex_id=None):
        if vertex_id is not None:
            self.c_clockwise_from = vertex_id
        return self.c_clockwise_from

    def clockwise_vertex(self):
        if self.vertices[0].id() == self.c_clockwise_from:
            return self.vertices[0]
        else:
            return self.vertices[1]

    def radius(self):
        return self.c_center.dist(self.clockwise_vertex())

    def angle(self):
        v1 = self.clockwise_vertex() - self.center()
        #v2 = self.vertices[self.other_id] - self.center()
        v2 = self.other_vtx - self.center()
        ang = angle_c(v1, v2)
        return ang

    def length(self):
        s = self.radius() * self.angle()
        return s

    def sector_area(self, rad):
        ang = self.angle()
        a = (rad ** 2.0) * ang / 2.0
        return math.fabs(a)

    def padded_area(self, rad):
        a = self.sector_area(rad)
        return a

    def sign(self, sgn=None):
        if sgn is not None:
            self.area_sign = sgn
        return self.area_sign

