"""Governing classes used for parsing vmf files
"""

from libvmf.datatype.base import ValveDict
from libvmf.datatype.base import ValveClass

from libvmf.datatype.camera import ValveCamera
from libvmf.datatype.camera import ValveCameras

from libvmf.datatype.displacement import ValveDisplacement
from libvmf.datatype.entity import ValveEntity

from libvmf.datatype.world import ValveMap
from libvmf.datatype.world import ValveWorld

from libvmf.datatype.solid import ValveSolid

from libvmf.datatype.viewsettings import ValveViewSettings

from libvmf.datatype.cordon import ValveCordon

from libvmf.datatype.versioninfo import ValveVersionInformation

DATATYPES = {
    'entity': ValveEntity,
    'world': ValveWorld,
    'visgroups': ValveDict,
    'viewsettings': ValveViewSettings,
    'cordon': ValveCordon,
    'cameras': ValveCameras,
    'camera': ValveCamera,
    'solid': ValveSolid,
    'side': ValveSolid.Side,
    'editor': ValveSolid.Editor,
    'dispinfo': ValveDisplacement,
    'connections': list,
    # Todo: Refactor datatypes to be children of datatype
    # ValveDisplacement:
    'allowed_verts': ValveDisplacement.AllowedVerts,
    'alphas': ValveDisplacement.Alphas,
    'distances': ValveDisplacement.Distances,
    'normals': ValveDisplacement.Normals,
    'triangle_tags': ValveDisplacement.TriangleTags,
    'versioninfo': ValveVersionInformation,
}
