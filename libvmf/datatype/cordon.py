""" Cordon - Compilation directive
Only objects that are at least partially within these
    boundaries will be compiled, and a box using the assigned
    cordon texture will be placed along these boundaries to
    seal leaks.
"""

from libvmf.datatype.base import ValveClass


class ValveCordon(ValveClass):
    vmf_mins = str    # "(-1024 -1024 -1024)"
    vmf_maxs = str    # "(1024 1024 1024)"
    vmf_active = int  # "0"
