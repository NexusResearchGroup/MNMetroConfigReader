#!/usr/bin/env python
from __future__ import division
from collections import namedtuple
import xml.etree.cElementTree as ET

Corridor = namedtuple('Corridor', ["route",
                                   "dir"]
                      )

R_Node = namedtuple('R_Node', ["name",
                               "n_type",
                               "label",
                               "lat",
                               "lon",
                               "lanes",
                               "shift",
                               "station_id",
                               "speed_limit",
                               "attach_side",
                               "transition",
                               "above",
                               "pickable",
                               "active",
                               "forks"]
                    )

class MNMetroConfigReader:
    def __init__(self, filename=None):
        if filename == None:
            self.filename = None
        else:
            self.load_file(filename)

    def load_file(self, filename):
        self.root = ET.parse(filename).getroot()

    def list_corridors(self):
        '''
        Returns a list of Corridors in the metro_config file

        Each element in the list is a namedtuple of type "Corridor" with the properties:

            route   = the route idenfier, e.g. "I-35W"
            dir     = the directrion identifier, e.g. "SB"

        A route and dir pair uniquely idenfies a corridor in the metro_config.xml file.
        '''
        return list(Corridor(route=corridor.get('route'), dir=corridor.get('dir')) for corridor in self.root.findall('corridor'))

    def list_rnodes_in_corridor(self, corridor):
        '''
        Returns a list containing an R_Node for each r_node in the specified Corridor

        Each element in the list is a namedtuple of type "R_Node" with the properties:

            name        = the name of the r_node, e.g. "rnd_95039"
            n_type      = the type of node, e.g. 'Entrance', 'Station', etc
            label
            lat         = the latitude of the r_node's location in decimal degrees
            lon         = the longitude of the r_node's location in decimal degrees
            lanes
            shift
            station_id  = for an n_node of type "Station", the station id; for other
                            types, None
            speed_limit
            attach_side
            transition
            above
            pickable
            forks
            active

        The r_nodes are listed in the order of their appearance in the
        metro_config.xml file, which MnDOT states corresponds to their physical
        locations witihn the corridor.
        '''
        corridor_node = self.root.findall("corridor[@route='%s'][@dir='%s']" % (corridor.route, corridor.dir))[0]
        r_nodes = []
        for r_node in corridor_node.findall("r_node"):
            r_nodes.append(R_Node(name = r_node.get("name"),
                                  n_type = r_node.get("n_type"),
                                  label = r_node.get("label"),
                                  lat = float(r_node.get("lat")),
                                  lon = float(r_node.get("lon")),
                                  lanes = r_node.get("lanes"),
                                  shift = r_node.get("shift"),
                                  station_id = r_node.get("station_id"),
                                  speed_limit = r_node.get("s_limit"),
                                  attach_side = r_node.get("attach_side"),
                                  transition = r_node.get("transition"),
                                  above = r_node.get("above"),
                                  pickable = r_node.get("pickable"),
                                  forks = r_node.get("forks"),
                                  active = r_node.get("active")
                                  )
                           )
        return r_nodes

    def find_rnodes_in_corridor(self, corridor, attributes):
        '''
        Returns a list of r_nodes in the specified corridor with the specified
        attributes

        corridor should be a Corridor objects identifying one of the corridors
        in the metro_config.xml file

        attributes should be a list of (attribute, value) pairs that the
        r_nodes will be compared against. For example,
            attributes = (("n_type", "Station"), ("speed_limit", "70"))
        will return a list of all Station nodes where the speed limit is 70.
        Inequalities are not supported.
        '''
        corridor_node = self.root.findall("corridor[@route='%s'][@dir='%s']" % (corridor.route, corridor.dir))[0]
        r_nodes = []

        query = "r_node"
        for attribute in attributes:
            query += "[@%s='%s']" % (attribute[0], attribute[1])

        for r_node in corridor_node.findall(query):
            r_nodes.append(R_Node(name = r_node.get("name"),
                                  n_type = r_node.get("n_type"),
                                  label = r_node.get("label"),
                                  lat = r_node.get("lat"),
                                  lon = r_node.get("lon"),
                                  lanes = r_node.get("lanes"),
                                  shift = r_node.get("shift"),
                                  station_id = r_node.get("station_id"),
                                  speed_limit = r_node.get("s_limit"),
                                  attach_side = r_node.get("attach_side"),
                                  transition = r_node.get("transition"),
                                  above = r_node.get("above"),
                                  pickable = r_node.get("pickable"),
                                  forks = r_node.get("forks"),
                                  active = r_node.get("active")
                                  )
                           )
        return r_nodes

if __name__ == '__main__':
    testfile = "test/metro_config.xml"

    mcreader = MNMetroConfigReader(testfile)
    corridors = mcreader.list_corridors()
    rnodes = mcreader.list_rnodes_in_corridor(corridors[0])
    stations = mcreader.find_rnodes_in_corridor(corridors[0], (("n_type", "Station"),))
    print corridors
    print rnodes
    print stations
