""" The Solid world geometry
"""

from libvmf.datatype.base import ValveClass
from libvmf.datatype.displacement import ValveDisplacement


class ValveSolid(ValveClass):
    """ A node representing a solid volume.
    """
    allow_multiple = True

    class Side(ValveClass):
        """ The geometry for a single face of a solid
        """
        allow_multiple = True

        vmf_plane = str
        vmf_smoothing_groups = int
        vmf_material = str
        vmf_uaxis = str  # "[0.0 0.0 -1.0 288] 0.25"
        vmf_vaxis = str  # "[0.0 1.0 0.0 0] 0.25"
        vmf_lightmapscale = int
        vmf_dispinfo = ValveDisplacement

    vmf_side = Side
