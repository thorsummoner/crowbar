import sys
import time
import warnings
from pprint import pprint

from exception import ValveException
from exception import ValveKeyError
from exception import ValveTypeError

from datatype import ValveDict
from datatype import ValveClass
from datatype import ValveEntity
from datatype import ValveCamera
from datatype import ValveCameras
from datatype import ValveDisplacement
from datatype import ValveSolid
from datatype import ValveWorld
from datatype import ValveMap

import datatype

class VmfParser(dict):
    """docstring for ValveMap"""
    # pylint: disable=too-many-instance-attributes
    lines = 0
    i = 0
    indent = 0
    mapobject = ValveMap
    mapdata = mapobject()
    _parsenode = []
    datatypes = datatype.datatypes
    _parseerrors = []

    def __init__(self, filehandle, stdout=sys.stdout):
        entry_time = time.time()
        super(VmfParser, self).__init__()
        self.filehandle = filehandle
        self.stdout = stdout

        self.lines = self.bufcount()
        self.minupdate = self.lines // 400 or 10


        self.iterator = iter(self.filehandle.readline, '')
        self.mapdata = self._parse(self.mapobject())
        self.elpsed_time = time.time() - entry_time
        self.stdout.write('\n%s\n' % self.elpsed_time)

        # pprint(self.mapdata)
        pprint(self._parseerrors)
        with open('dumps.vmfstuff', 'w') as file_handle:
            file_handle.write(str(self.mapdata))

    def report(self, callback=lambda x: False):
        percent = "{0:.0f} ".format(float(self.i)/self.lines * 100)
        output = (percent, self.i, self.lines)
        if None != self.stdout:
            self.stdout.write(
                '%s%% %i/%i\r' % output
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


    def _parse(self, output):
        try:
            datatype = 'FIRST_ITERATION_PLACEHOLDER'
            while True:
                line = next(self.iterator).rstrip('\n\r')
                self.i += 1
                if line.endswith('}'):
                    return output
                line = line[self.indent:]
                if 0 == self.i % self.minupdate:
                    self.report()

                if line.startswith('{'):
                    if not datatype in self.datatypes:
                        raise ValveKeyError(
                            "Unknown datatype [ %s ]"
                            % datatype
                        )
                    self.indent += 1
                    value = self._parse(self.datatypes[datatype]())
                    if isinstance(output, dict):
                        try:
                            if type(value) is str and 'id' in value:
                                output[value['id']] = value
                            elif not datatype in output:
                                output[datatype] = value
                            else:
                                if not isinstance(output[datatype], list):
                                    output[datatype] = [output[datatype]]

                                output[datatype].append(value)
                        except ValveException as err:
                            self._parseerrors.append(
                                'Ln %s: %s' % (self.i, err)
                            )
                    elif isinstance(output, list):
                        output.append((datatype, value))
                    self.indent -= 1
                    continue

                if line.startswith('"'):
                    key, value = line.split('" "')
                    key = key[1:]
                    value = value[:-1]
                    if isinstance(output, dict):
                        if key in output:
                            warnings.warn(
                                'Line %i: Duplicate key <%s> dropped\n'
                                % (self.i, key)
                            )
                        try:
                            output[key] = value
                        except ValveException as err:
                            self._parseerrors.append(
                                'Ln %s: %s' % (self.i, err)
                            )

                    elif isinstance(output, list):
                        output.append((key, value))
                    continue


                datatype = line

        except StopIteration:
            assert 0 == len(self._parsenode)
            self.report()
            return output


if '__main__' == __name__:
    with open('ttt_67thway/src/ttt_67thway.vmf', 'r') as maphandle:
        VmfParser(maphandle)
