from vertex import *
from edge import *
from jsonparse import *


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


def test_circular_arc():
    v1 = Vertex(Point(0, 0), 0)
    v2 = Vertex(Point(1, 1), 1)
    center = Point(-1, 1)
    e = CircularArc(v1, v2, center, id=0)
    print e


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

# ===
if __name__ == '__main__':
    test_arc_json_parser()
    test_simple_arc_json_parser()
    test_simple_json_parser()
    test_rect_json_parser()
    test_vertex()
    test_edge()
    test_linesegment()
    test_circular_arc()
