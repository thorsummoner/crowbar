""" Visibility groups, used to filter rendered objects
"""

from libvmf.datatype.base import ValveClass


class ValveVisibilityGroup(ValveClass):
    """
    visgroup
    {
        "name" "Rebuild areaportals"
        "visgroupid" "0"
    }
    """
    allow_multiple = True
    vmf_visgroupid = int
    vmf_name = str

class ValveVisibilityGroups(ValveClass):
    """visgroups node
    """
    pass

ValveVisibilityGroups.vmf_visgroup = ValveVisibilityGroup

