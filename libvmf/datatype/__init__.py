
from base import ValveDict
from base import ValveClass

from camera import ValveCamera
from camera import ValveCameras

from displacement import ValveDisplacement
from entity import ValveEntity

from world import ValveMap
from world import ValveWorld

from solid import ValveSolid


datatypes = {
    'entity': ValveEntity,
    'world': ValveWorld,
    'cameras': ValveCameras,
    'camera': ValveCamera,
    'solid': ValveSolid,
    'side': ValveSolid.Side,
    'dispinfo': ValveDisplacement,
    'connections': list,
    # Todo: Refactor datatypes to be children of datatype
    # ValveDisplacement:
    'allowed_verts': ValveDisplacement.AllowedVerts,
    'alphas': ValveDisplacement.Alphas,
    'distances': ValveDisplacement.Distances,
    'normals': ValveDisplacement.Normals,
    'triangle_tags': ValveDisplacement.TriangleTags,
}
