""" Settings for how to customize the interface
"""

from libvmf.datatype.base import ValveClass


class ValveViewSettings(ValveClass):
    vmf_bSnapToGrid = int       # "1"
    vmf_bShowGrid = int         # "1"
    vmf_bShowLogicalGrid = int  # "0"
    vmf_nGridSpacing = int      # "64"
    vmf_bShow3DGrid = int       # "0"
