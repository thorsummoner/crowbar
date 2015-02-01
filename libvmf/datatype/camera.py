""" Camera related classes
"""

from libvmf.datatype.base import ValveClass


class ValveCamera(ValveClass):
    """ Like an entity, but specifcally a camera
    """
    allow_multiple = True
    vmf_position = str  # "[-2712.7458 6088.62 149.23857]"
    vmf_look = str      # "[-2460.03 6088.62 65.0]"


class ValveCameras(ValveClass):
    """ Group of cameras
    """
    vmf_activecamera = int

ValveCameras.vmf_camera = ValveCamera
