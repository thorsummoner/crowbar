
def bufcount(filehandle):
    filehandle.seek(0)
    lines = 0
    buf_size = 1024 * 1024
    read_f = filehandle.read # loop optimization

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)

    filehandle.seek(0)
    return lines

from time import time
import sys
from collections import namedtuple



def report(i, lines):
    sys.stdout.write(
        "{0:.0f}% ".format(float(i)/lines * 100)
        + '%i/%i\r' % (i, lines)
    )

entry_time = time()
with open('ttt_67thway/src/ttt_67thway.vmf', 'r') as maptext:
    lines = bufcount(maptext)
    minupdate = lines // 400 or 10
    i = 0
    for line in iter(maptext.readline, ''):
        i += 1
        if 0 == i % minupdate:
            report(i, lines)

report(i, lines)
elpsed_time = time() - entry_time
print('\n' + str(elpsed_time))

