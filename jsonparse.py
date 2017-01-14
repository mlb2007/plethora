import json
from edge import *
from vertex import *


class JsonParser(object):
    def __init__(self, json_file):
        if json_file is None:
            raise Exception("Provide Json file input")

        with open(json_file) as jh:
            self.jobj = json.load(jh)

        # for caching ...
        self.extracted_vertices = False
        self.extracted_edges = False
        # cached lists  ...
        self. v_list = {}
        self. e_list = {}

    def __getitem__(self, item):
        return self.jobj[item]

    def __repr__(self):
        return self.jobj.__repr__()

    def get_vertices(self):
        for id_or_key, data in self.jobj.iteritems():
            #print "VERTICES_EXTRACT: Extracted key:", id_or_key, " value:", data
            if id_or_key == 'Vertices':
                for vid, vdata in data.iteritems():
                    try:
                        pos_dict = vdata["Position"]
                        x_pos = pos_dict["X"]
                        y_pos = pos_dict["Y"]
                        pt = Point(x_pos, y_pos)
                        # create vertices now  ...
                        vtx = Vertex(pt, str(vid))
                        self.v_list[str(vid)] = vtx
                    except:
                        raise Exception("key word position expected ..")

        self.extracted_vertices = True
        return self.v_list

    def get_edges(self):
        vertex_list = self.v_list
        if not self.extracted_vertices:
            vertex_list = self.get_vertices()

        for id, data in self.jobj.iteritems():
            #print "EDGE_EXTRACT: Extracted key:", id, " value:", data
            etype = None
            v_ids = list()
            cen = None
            clk_index = None
            try:
                etype = data['Type']
            except KeyError:
                pass
            try:
                v_ids = data['Vertices']
                print v_ids
                if len(v_ids) != 2:
                    print "Number of vertices got:", len(v_ids)
                    raise Exception("Expecting start and end points only for line segment")
            except KeyError:
                pass
            try:
                ctr = data['Center']
                xc = ctr['X']
                yc = ctr['Y']
                cen = Point(xc, yc)
            except KeyError:
                pass
            try:
                clk_index = data["ClockwiseFrom"]
            except:
                pass

            # now set up the edge data
            edge = None
            if etype == 'LineSegment':
                edge = LineSegment(vertex_list[str(v_ids[0])], vertex_list[str(v_ids[1])], str(id))
            elif etype == 'CircularArc':
                edge = CircularArc(vertex_list[str(v_ids[0])], vertex_list[str(v_ids[1])], cen, str(id), str(clk_index))

            # add to list
            if edge is not None:
                self.e_list[str(id)] = edge

        self.extracted_edges = True

        return self.e_list

    def extract(self):
        vertices_list = self.get_vertices()
        edge_list = self.get_edges()
        return vertices_list, edge_list

