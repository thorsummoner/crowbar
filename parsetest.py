




from time import time
import sys
from collections import namedtuple
from pprint import pprint, pformat

class ValveDict(dict):
    def __str__(self):
        out = ''
        for key, value in self.items():
            out += '\t"%s" "%s"\n' % (key, value)
        return out

    def __repr__(self):
        return self.__str__()

class ValveMap(dict):
    lines = 0
    i = 0
    indent = -1

    """docstring for ValveMap"""
    def __init__(self, filehandle, stdout=sys.stdout):
        entry_time = time()
        super(ValveMap, self).__init__()
        self.filehandle = filehandle
        self.stdout = stdout

        self.bufcount()
        self.minupdate = self.lines // 400 or 10


        self.iterator = iter(self.filehandle.readline, '')
        parsed_file = self._parse(dict())
        self.elpsed_time = time() - entry_time
        print('\n' + str(self.elpsed_time))

        pprint(parsed_file)

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

    def _parse(self, datavar):
        datasum = dict()
        try:
            while True:
                line = next(self.iterator)
                self.i += 1

                if line.lstrip().startswith('}'):
                    self.indent -= 1
                    assert self.indent >= -1, "indent math is wrong"
                    if self.indent > -1:
                        return datavar
                    datasum[datatype] = datavar
                    continue

                assert line.lstrip() == line[(self.indent + 1):], "indent is wrong"
                line = line[(self.indent + 1):]
                # linevalue = line.strip()
                if 0 == self.i % self.minupdate:
                    self.report()

                if line.startswith('{'):
                    current_id = None
                    self.indent += 1
                    sub_datavar = self._parse(datavar)

                    if 'id' in sub_datavar:
                        datavar[sub_datavar['id']] = sub_datavar
                    else:
                        datavar[datatype] = sub_datavar

                    continue

                if line.startswith('"'):
                    key, value = line.split('" "')
                    datavar[key.lstrip('"')] = value.rstrip('"\n')
                    continue

                datatype = line
                pprint('entering datatype %s' % datatype)
                dataid = None
                datavar = dict()

        except StopIteration:
            self.report()
            return datasum
        except (AssertionError, UnboundLocalError) as err:
            # pprint((self.i, line, self.indent))
            raise NotImplementedError(
                'Unable to parse file with error `%s`, %s' % (
                    err,
                    str((self.i, line, self.indent))
                )
            )
            # # Potentially, if the error is being used to indicate an empty
            # # definition, the following line could be used to silence a
            # # potential parsing error
            return (None, dict())




with open('ttt_67thway/src/ttt_67thway.vmf', 'r') as maphandle:
    ValveMap(maphandle)



# newstrat
# turn enter and exit block into methods that can be called one BOF and EOF
