
from base import ValveClass

class ValveCamera(ValveClass):
    allow_multiple = True
    vmf_position = str # "[-2712.7458 6088.62 149.23857]"
    vmf_look = str # "[-2460.03 6088.62 65.0]"

class ValveCameras(ValveClass):
    vmf_activecamera = int

ValveCameras.vmf_camera = ValveCamera

