
from libvmf import parse

if '__main__' == __name__:
    with open('ttt_67thway/src/ttt_67thway.vmf', 'r') as maphandle:
        parse.VmfParser(maphandle)
