""" File for displacement-related classes
"""

from libvmf.datatype.base import ValveClass

class ValveDisplacement(ValveClass):
    """ `dispinfo` key
    """

    class _RowData(ValveClass):
        """ Handle node attributes
        """
        def __setitem__(self, key, value):
            # Allow variable keys
            if key.startswith('row') and key[3:].isdigit():
                setattr(self, 'vmf_%s' % key, str)

            dict.__setitem__(self, key, value)

    class AllowedVerts(ValveClass):
        """ `allowed_verts` key """
        def __setitem__(self, key, value):
            # todo, restruct to numeric keys only?
            dict.__setitem__(self, key, value)

    class Alphas(_RowData):
        """ `alphas` key """
        pass

    class Distances(_RowData):
        """ `distances` key """
        pass

    class Normals(_RowData):
        """ `normals` key """
        pass

    class TriangleTags(ValveClass):
        """ `triangle_tags` key """
        pass

    vmf_power = int # "3"
    vmf_startposition = str # "[384.0 512.0 72.0]"
    vmf_elevation = int # "0"
    vmf_subdiv = int # "0"
    vmf_triangle_tags = TriangleTags
    vmf_allowed_verts = AllowedVerts
    vmf_alphas = Alphas
    vmf_distances = Distances
    vmf_normals = Normals
