""" Info about the version of hammer this file was made with
"""

from libvmf.datatype.base import ValveClass


class ValveVersionInformation(ValveClass):
    """ verinfo node
    """
    vmf_editorversion = int  # "400"
    vmf_editorbuild = int    # "6550"
    vmf_mapversion = int     # "1"
    vmf_formatversion = int  # "100"
    vmf_prefab = int         # "0"

