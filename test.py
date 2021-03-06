from vertex import *
from edge import *
from jsonparse import *
from stock import *


def test_vertex():
    v1 = Vertex(Point(0, 0), "556")
    v2 = Vertex(Point(1, 1), "4456665767")
    print v1, v2


def test_edge():
    v1 = Vertex(Point(0, 0), 0)
    v2 = Vertex(Point(1, 1), 1)
    e = Edge(v1, v2)
    print e


def test_linesegment():
    v1 = Vertex(Point(1, 1), 0)
    v2 = Vertex(Point(2, 2), 1)
    e = LineSegment(v1, v2, id=0)
    print e
    print e.length()
    print e.radius()


def test_circular_arc():
    v1 = Vertex(Point(0, 1), 0)
    v2 = Vertex(Point(1, 0), 1)
    center = Point(0, 0)
    e = CircularArc(v1, v2, center, id=0)
    print e
    print e.clockwise_vertex()
    print e.length()
    print e.radius()
    print e.angle()
    print e.sector_area(e.radius())


def test_simple_json_parser():
    filename = "simple.json"
    jp = JsonParser(filename)
    vertices, edges = jp.extract()
    print vertices
    print edges


def test_rect_json_parser():
    filename = "rectangle.json"
    jp = JsonParser(filename)
    vertices, edges = jp.extract()
    print vertices
    print edges


def test_simple_arc_json_parser():
    filename = "simple_circulararc.json"
    jp = JsonParser(filename)
    vertices, edges = jp.extract()
    print vertices
    print edges


def test_arc_json_parser():
    filename = "circulararc.json"
    jp = JsonParser(filename)
    vertices, edges = jp.extract()
    print vertices
    print edges


def test_rect_cost():
    filename = "rectangle.json"
    cost = Stock.process(filename)
    assert (abs(cost - 14.10) < 1e-2)


def test_cut_circular_cost():
    filename = "circulararc.json"
    cost = Stock.process(filename)
    assert (abs(cost - 4.06) < 1e-2)


def test_ext_circular_cost():
    filename = "extrude_arc.json"
    cost = Stock.process(filename)
    assert (abs(cost - 4.47) < 1e-2)


# ===
if __name__ == '__main__':
    test_cut_circular_cost()
    test_ext_circular_cost()
    test_rect_cost()
    # test_arc_json_parser()
    # test_simple_arc_json_parser()
    # test_simple_json_parser()
    # test_rect_json_parser()
    # test_vertex()
    # test_edge()
    # test_linesegment()
    # test_circular_arc()
