
from time import time
import sys
from collections import namedtuple

class ValveMap(dict):
    lines = 0
    i = 0

    """docstring for VmfParser"""
    def __init__(self, filehandle):
        super(VmfParser, self).__init__()
        self.filehandle = filehandle

        self.bufcount()
        self.minupdate = lines // 400 or 10


        self._parse()

    def report(self, callback=lambda: False, stdout=sys.stdout):
        percent = "{0:.0f} ".format(float(self.i)/self.lines * 100)
        output = (percent, self.i, self.lines)
        if None != stdout:
            stdout.write(
                + '%f%% %i/%i\r' % output
            )

        callback(output)
        return output

    def bufcount(self):
        """ Count lines in file as fast as possible! """
        self.filehandle.seek(0)
        buf_size = 1024 * 1024
        read_f = self.filehandle.read # loop optimization

        buf = read_f(buf_size)
        while buf:
            self.lines += buf.count('\n')
            buf = read_f(buf_size)

        self.filehandle.seek(0)

        return self.lines

    def _parse():
        pass





entry_time = time()
with open('ttt_67thway/src/ttt_67thway.vmf', 'r') as maptext:
    lines = bufcount(maptext)
    i = 0
    for line in iter(maptext.readline, ''):
        i += 1
        linevalue = line.strip()
        if 0 == i % minupdate:
            report(i, lines)

        if line.startswith('\{'):

            datavar = dict()

        if line.lstrip('\t').startswith('"id"':
            pass

        datatype = line.strip()

report(i, lines)
elpsed_time = time() - entry_time
print('\n' + str(elpsed_time))

