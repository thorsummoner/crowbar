from base import ValveDict
from base import ValveClass

from solid import ValveSolid
from entity import ValveEntity

from camera import ValveCamera
from camera import ValveCameras

class ValveWorld(ValveClass):
    vmf_skyname = str
    vmf_maxpropscreenwidth = int
    vmf_detailvbsp = str
    vmf_detailmaterial = str
    vmf_comment = str
    vmf_mapversion = int
    vmf_classname = str
    vmf_solid = ValveSolid

class ValveMap(ValveDict):
    vmf_world = ValveWorld
    vmf_entity = ValveEntity
    vmf_cameras = ValveCameras
