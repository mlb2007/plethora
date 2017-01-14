from vertex import Vertex


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


class LineSegment(Edge):
    def __init__(self, start_vertex, end_vertex, id):
        super(LineSegment, self).__init__(start_vertex, end_vertex, id=id)
        super(LineSegment, self).type(EdgeType.eLineSegment)

    def __repr__(self):
        repr = "Edge," + " type:" + "LineSegment, id:" + str(self.id) + "\n"
        for v in self.vertices:
            repr += "\t" + v.__repr__() + "\n"
        return repr

    def type(self):
        super(LineSegment, self).type()


class CircularArc(Edge):
    def __init__(self, start_vertex, end_vertex, center, id, clockwise_from=None):
        super(CircularArc, self).__init__(start_vertex, end_vertex, id=id)
        super(CircularArc, self).type(EdgeType.eCircularArc)
        if clockwise_from is None:
            self.c_clockwise_from = start_vertex.id()
        else:
            self.c_clockwise_from = clockwise_from
        self.c_center = center

    def __repr__(self):
        repr = "Edge," + " type:" + "CircularArc, id:" + str(self.id) + "\n"
        for v in self.vertices:
            repr += "\t" + v.__repr__() + "\n"
        repr += "\tcenter:[" + str(self.c_center[0]) + "," + str(self.c_center[1]) + "]\n"
        repr += "\tClockwiseFrom (id):" + str(self.c_clockwise_from) + "\n"
        #        ",[" + str(self.vertices[self.c_clockwise_from][0]) + "," + str(self.vertices[self.c_clockwise_from][1]) + "]\n"
        return repr

    def type(self):
        return super(CircularArc, self).type()

    def center(self, circle_center=None):
        if circle_center is not None:
            self.c_center = circle_center
        return self.c_center

    def clockwisefrom(self, vertex_id=None):
        if vertex_id is None:
            self.c_clockwise_from = vertex_id
        return self.c_clockwise_from
