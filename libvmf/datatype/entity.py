""" Classes for handling entities
"""

from libvmf.datatype.base import ValveClass

class ValveEntity(ValveClass):
    """ Entity node
    """
    allow_multiple = True
    vmf_classname = str
    vmf_origin = str # "776.0 259.0 -96.0"

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
