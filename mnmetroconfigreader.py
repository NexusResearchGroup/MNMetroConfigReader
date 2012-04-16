#!/usr/bin/env python
from __future__ import division
from collections import namedtuple
import xml.etree.cElementTree as ET

Corridor = namedtuple('Corridor',
                      ["route",
                       "dir"]
                      )
R_Node = namedtuple('R_Node',
                    ["name",
                     "n_type",
                     "label",
                     "lat",
                     "lon",
                     "lanes",
                     "shift",
                     "station_id",
                     "speed_limit",
                     "attach_side"]
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
        '''
        return list(Corridor(route=corridor.get('route'), dir=corridor.get('dir')) for corridor in self.root.findall('corridor'))

    def list_rnodes_in_corridor(self, corridor):
        '''
        Returns a list containing an R_Node for each r_node in the specified Corridor
        '''
        corridor_node = self.root.findall("corridor[@route='%s'][@dir='%s']" % (corridor.route, corridor.dir))[0]
        r_nodes = []
        for r_node in corridor_node.findall("r_node"):
            r_nodes.append(R_Node(name = r_node.get("name"),
                                  n_type = r_node.get("n_type"),
                                  label = r_node.get("label"),
                                  lat = r_node.get("lat"),
                                  lon = r_node.get("lon"),
                                  lanes = r_node.get("lanes"),
                                  shift = r_node.get("shift"),
                                  station_id = r_node.get("station_id"),
                                  speed_limit = r_node.get("s_limit"),
                                  attach_side = r_node.get("attach_side")
                                  )
                           )
        return r_nodes

if __name__ == '__main__':
    testfile = "test/metro_config.xml"

    mcreader = MNMetroConfigReader(testfile)
    corridors = mcreader.list_corridors()
    rnodes = mcreader.list_rnodes_in_corridor(corridors[0])
    print corridors
    print rnodes
