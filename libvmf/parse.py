"""VMF Parser
"""

import sys
import time
import warnings
from pprint import pprint

from libvmf.exception import ValveException
from libvmf.exception import ValveKeyError

from libvmf.datatype import ValveMap

from libvmf.datatype import DATATYPES


class VmfParser(dict):
    """docstring for ValveMap"""
    # pylint: disable=too-many-instance-attributes
    lines = 0
    i = 0
    indent = 0
    mapobject = ValveMap
    mapdata = mapobject()
    _parsenode = []
    datatypes = DATATYPES
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
        """Progress Update Handler
        """
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
        # loop optimization:
        read_f = self.filehandle.read

        buf = read_f(buf_size)
        while buf:
            self.lines += buf.count('\n')
            buf = read_f(buf_size)

        self.filehandle.seek(0)

        return self.lines

    def _parse(self, output):
        """ Recursive node parser
        """
        import pdb
        try:
            datatype = 'FIRST_ITERATION_PLACEHOLDER'
            while True:
                line = next(self.iterator).rstrip('\n\r')
                self.i += 1
                if line.endswith('}'):
                    if not isinstance(output, list):
                        output.finalize()
                    return output
                line = line[self.indent:]
                if 0 == self.i % self.minupdate:
                    self.report()

                if line.startswith('{'):
                    if datatype not in self.datatypes:
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
                            elif datatype not in output:
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
