""" Top level nodes
"""

from libvmf.datatype.base import ValveDict
from libvmf.datatype.base import ValveClass

from libvmf.datatype.solid import ValveSolid
from libvmf.datatype.entity import ValveEntity

from libvmf.datatype.camera import ValveCameras

from libvmf.datatype.cordon import ValveCordon

from libvmf.datatype.viewsettings import ValveViewSettings

from libvmf.datatype.visgroup import ValveVisibilityGroups

from libvmf.datatype.versioninfo import ValveVersionInformation


class ValveWorld(ValveClass):
    """ The World Geometry Node
    """
    vmf_skyname = str
    vmf_maxpropscreenwidth = int
    vmf_detailvbsp = str
    vmf_detailmaterial = str
    vmf_comment = str
    vmf_mapversion = int
    vmf_classname = str
    vmf_solid = ValveSolid
    vmf_targetname = str
    vmf_coldworld = int
    vmf_message = str
    vmf_light = str
    vmf_spawnflags = int
    vmf_MaxRange = int  #8096
    vmf_startdark = int
    vmf_gametitle = int


class ValveMap(ValveDict):
    """ The file's outer most node
    """
    vmf_world = ValveWorld
    vmf_entity = ValveEntity
    vmf_cameras = ValveCameras
    vmf_cordon = ValveCordon
    vmf_viewsettings = ValveViewSettings
    vmf_visgroups = ValveVisibilityGroups
    vmf_versioninfo = ValveVersionInformation

