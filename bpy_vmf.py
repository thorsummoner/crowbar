import bpy
from sys import argv
from pprint import pprint
from collections import namedtuple
import os
import sys
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))

from libvmf import parse

FILE = './test_maps/simple_brush.vmf'
# FILE = './test_maps/ttt_richland/src/ttt_richland.vmf'
# FILE = './test_maps/ttt_bank/src/ttt_bank.vmf'
# FILE = './test_maps/ttt_whitehouse/src/ttt_whitehouse.vmf'
# FILE = './test_maps/ttt_lost_temple/src/ttt_lost_temple.vmf'
FILE = './test_maps/ttt_minecraft/src/ttt_minecraft.vmf'
# FILE = './test_maps/ttt_minecraftcity/src/ttt_minecraftcity.vmf'
# FILE = './test_maps/ttt_magma/src/ttt_magma.vmf'
# FILE = './test_maps/ttt_clue_se/src/ttt_clue_se.vmf'
# FILE = './test_maps/ttt_datmap/src/ttt_datmap.vmf'
# FILE = './test_maps/ttt_hotwireslum_final/src/ttt_hotwireslum.vmf'
# FILE = './test_maps/ttt_fallout/src/ttt_fallout.vmf'
# FILE = './test_maps/ttt_community_pool_classic/src/ttt_community_pool_classic.vmf'
# FILE = './test_maps/ttt_canyon/src/ttt_canyon.vmf'
# FILE = './test_maps/ttt_camel/src/ttt_camel.vmf'
# FILE = './test_maps/ttt_community_bowling/src/ttt_community_bowling.vmf'
# FILE = './test_maps/ttt_rooftops/src/ttt_rooftops.vmf'
# FILE = './test_maps/ttt_terrortrain/src/ttt_terrortrain.vmf'
# FILE = './test_maps/ttt_hairyhouse/src/ttt_hairyhouse.vmf'
# FILE = './test_maps/ttt_67thway/src/ttt_67thway.vmf'
# FILE = './test_maps/ttt_vessel/src/ttt_vessel.vmf'
# FILE = './test_maps/ttt_bb_teenroom/src/ttt_bb_teenroom.vmf'
# FILE = './test_maps/ttt_island_2013/src/ttt_island_2013.vmf'


class PointsList(list):
    def add_unique(self, value):
        if value not in self:
            self.append(value)
        return self.index(value)


def main():
    with open(FILE, 'r') as maphandle:
        map_data = parse.VmfParser(maphandle)

    solids = map_data.mapdata['world']['solid']
    if not isinstance(solids, list):
        solids = [solids]
    for solid in solids:

        points_list = PointsList()
        Point = namedtuple('Point', ['x', 'y', 'z'])
        # print('=' * 80)
        faces = list()
        name = 'solid-%i' % solid['id']
        mesh = bpy.data.meshes.new(name)   # create a new mesh
        ob = bpy.data.objects.new(name, mesh)          # create an object with that mesh
        ob.location = bpy.context.scene.cursor_location   # position object at 3d-cursor
        bpy.context.scene.objects.link(ob)                # Link object to scene

        for side in solid['side']:
            plane = side['plane']
            # pprint(side['id'])
            face = list()
            for idx, point in enumerate(plane.split('(')[1:]):
                point = tuple(point.rstrip(') ').split())
                point = [float(i) * 0.01 for i in point]
                point_idx = points_list.add_unique(point)
                # pprint(('point', point, point_idx))
                face.append(point_idx)

            faces.append(tuple(face))
            p, a, q = [
                Point(*points_list[i])
                for i in face
            ]

            center = Point((p.x + q.x) / 2.0, (p.y + q.y) / 2.0, (p.z + q.z) / 2.0)

            forth = Point(
                center.x - (a.x - center.x), #*2,
                center.y - (a.y - center.y), #*2,
                center.z - (a.z - center.z), #*2,
            )
            forth_idx = points_list.add_unique(forth)

            faces.append(tuple([face[0], forth_idx, face[2]]))

        # Fill the mesh with verts, edges, faces
        mesh.from_pydata(list(points_list), [], faces)   # edges or faces should be [], or you ask for problems
        mesh.update(calc_edges=True)    # Update mesh with new data

main()
