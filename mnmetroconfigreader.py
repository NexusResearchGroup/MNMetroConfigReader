#!/usr/bin/env python
from __future__ import division
import xml.etree.cElementTree as ET

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
        Returns a list of tuples (route, dir) for each corridor in the metro_config file
        '''
        return list((corridor.get('route'), corridor.get('dir')) for corridor in self.root.findall('corridor'))

    def list_rnodes_in_corridor(self, route, dir):
        pass

if __name__ == '__main__':
    testfile = "test/metro_config.xml"

    mcreader = MNMetroConfigReader(testfile)
    print mcreader.list_corridors()
