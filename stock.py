import json
from edge import *
from vertex import *
from jsonparse import *
import sys


class Stock(object):
    def __init__(self, json_file):
        self.padding = 0.1
        self.material_cost = 0.75
        self.cutter_speed = 0.5
        self.time_cost = 0.07
        jp = JsonParser(json_file)
        self.vertices, self.edges = jp.extract()
        self.ordered_edges = None

    def is_closed(self):
        if self.edges is None:
            return False
        id_list = list()
        for edge_id, edge in self.edges.iteritems():
            id_list.append(edge.start().id())
            id_list.append(edge.end().id())
        if len(id_list) % 2 != 0:
            return False
        id_list.sort()
        for i in range(0, len(id_list), 2):
            if id_list[i] != id_list[i + 1]:
                return False
        return True

    # this orders the edges so that we can traverse the given stock
    # examine the bag of edges, pick one and then keeping picking edges from
    # the bag as and when we find the connection ... a simpler edge-find algorithm
    def form_closed_polygon(self):
        if not self.is_closed():
            return None
        ed_list = list(list())
        ed_rev_list = {}
        for edge_id, edge in self.edges.iteritems():
            ed_list.append([edge.start().id(), edge.end().id()])
            ed_rev_list[str(edge.start().id()) + str(edge.end().id())] = edge
        self.ordered_edges = list()
        st_id = ed_list[0][0]
        e_id = ed_list[0][1]
        key = str(st_id) + str(e_id)
        self.ordered_edges.append(ed_rev_list[key])
        # print "first Append edge:", ed_rev_list[key]
        del ed_list[0]
        i = 0
        while len(ed_list) > 0:
            curr_edge = ed_list[i]
            # print curr_edge
            key = str(curr_edge[0]) + str(curr_edge[1])
            if st_id == curr_edge[0] or st_id == curr_edge[1]:
                self.ordered_edges.append(ed_rev_list[key])
                # print "back. Adding edge:", ed_rev_list[key]
                if st_id == curr_edge[0]:
                    e_id = curr_edge[1]
                else:
                    e_id = curr_edge[0]
                del ed_list[i]
                i = 0
            elif e_id == curr_edge[0] or e_id == curr_edge[1]:
                self.ordered_edges.append(ed_rev_list[key])
                # print "front. Adding edge:", ed_rev_list[key]
                if e_id == curr_edge[0]:
                    st_id = curr_edge[1]
                else:
                    st_id = curr_edge[0]
                del ed_list[i]
                i = 0
            else:
                i += 1
        return self.ordered_edges

    # determine which side the circular arc is turning to determine the
    # right area
    # simple logic that takes into account how the turning happens given the
    # clockwisefrom data for the circular arc by examining neighboring edges
    #
    def circular_area_sign(self):
        ord_edges = self.form_closed_polygon()
        sz = len(ord_edges)
        # print ord_edges, "."
        for i, edge in enumerate(ord_edges):
            if edge.type() != EdgeType.eCircularArc:
                continue
            else:
                ccw_vid = edge.clockwisefrom()
                j = i
                keep_looping = True
                ref_vec = edge.clockwise_vertex() - edge.center()
                other_vertex = Point(0, 0)
                while (keep_looping):
                    which_edge = ord_edges[(j - 1) % sz]
                    which_edge2 = ord_edges[(j + 1) % sz]
                    got_edge = False
                    if not got_edge and (which_edge.start().id() == ccw_vid):
                        # print ccw_vid, " ref1:", which_edge.start().id()
                        other_vertex += which_edge.end()
                        j -= 1
                        got_edge = True
                    if not got_edge and (which_edge.end().id() == ccw_vid):
                        # print ccw_vid, " ref2:", which_edge.end().id()
                        other_vertex += which_edge.start()
                        j -= 1
                        got_edge = True
                    if not got_edge and (which_edge2.start().id() == ccw_vid):
                        # print ccw_vid, " ref3:", ord_edges[(i+1)%sz].start().id()
                        other_vertex += which_edge2.end()
                        j += 1
                        got_edge = True
                    if not got_edge and (which_edge2.end().id() == ccw_vid):
                        # print ccw_vid, " ref4:", ord_edges[(i+1)%sz].end().id()
                        other_vertex += which_edge2.start()
                        j += 1
                        got_edge = True
                    if not got_edge:
                        raise Exception("cannot find other vertex")

                    p2 = other_vertex - edge.center()
                    c = cross(ref_vec, p2)
                    if abs(c) < 1.0e-7:
                        keep_looping = True
                    elif c < 0:
                        edge.sign(-1.0)
                        keep_looping = False
                    if c > 0:
                        edge.sign(1.0)
                        keep_looping = False

    # find bounding box , including the circular protrusion or cut...
    def bbox(self):
        min = Point(sys.float_info.max, sys.float_info.max)
        max = Point(-sys.float_info.max, -sys.float_info.max)
        for edge in self.ordered_edges:
            s = edge.start().point
            e = edge.end().point
            if s[0] < min[0]:
                min[0] = s[0]
            if s[1] < min[1]:
                min[1] = s[1]
            if s[0] > max[0]:
                max[0] = s[0]
            if s[1] > max[1]:
                max[1] = s[1]
            if e[0] < min[0]:
                min[0] = e[0]
            if e[1] < min[1]:
                min[1] = e[1]
            if e[0] > max[0]:
                max[0] = e[0]
            if e[1] > max[1]:
                max[1] = e[1]
        # now bounds added by circular edge
        for edge in self.ordered_edges:
            if edge.type() == EdgeType.eCircularArc:
                ref_vec = edge.center() - edge.clockwise_vertex()
                rn = Point(-ref_vec[1], ref_vec[0]).normalize()
                mod_pt = Point(rn[0] * edge.radius(), rn[1] * edge.radius())
                ref_perp_vec = edge.center() + mod_pt
                if ref_perp_vec[0] < min[0]:
                    min[0] = ref_perp_vec[0]
                if ref_perp_vec[1] < min[1]:
                    min[1] = ref_perp_vec[1]
                if ref_perp_vec[0] > max[0]:
                    max[0] = ref_perp_vec[0]
                if ref_perp_vec[1] > max[1]:
                    max[1] = ref_perp_vec[1]
        return min, max

    def perimeter(self):
        perim = 0
        for edge in self.ordered_edges:
            perim += edge.length()
        return perim

    def _bbox_len_width(self):
        min, max = self.bbox()
        # print "bbox:", min, max
        length = abs(max[0] - min[0])
        width = abs(max[1] - min[1])
        return length, width

    def _bbox_area(self):
        length, width = self._bbox_len_width()

        area = length * width
        return area

    def padding_area(self):
        length, width = self._bbox_len_width()
        pad_area = (length * self.padding) + (width * self.padding) + (self.padding ** 2.0)
        return pad_area

    def area(self):
        bbox_area = self._bbox_area()
        circ_area = 0
        for edge in self.ordered_edges:
            if edge.type() == EdgeType.eCircularArc:
                # print "Sign of the edge is:", edge.area_sign
                circ_area += (edge.area_sign * edge.sector_area(edge.radius()))
        circ_area = 0
        bbox_area += circ_area
        return bbox_area

    def cutting_time(self):
        c_time = 0
        for edge in self.ordered_edges:
            speed = self.cutter_speed
            if edge.type() == EdgeType.eCircularArc:
                speed = self.cutter_speed * math.exp(-1.0 / edge.radius())
            length = edge.length()
            c_time += length / speed
        return c_time
