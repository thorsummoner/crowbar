import sys
import time

from pprint import pprint, pformat


class ValveDict(dict):
    pass

class ValveMap(dict):
    lines = 0
    i = 0
    indent = 0
    mapdata = ValveDict()
    _parsenode = []
    datatypes = {
        'entity': ValveDict,
        'world': ValveDict,
        'cameras': ValveDict,
        'camera': ValveDict,
        'solid': ValveDict,
        'side': ValveDict,
        'dispinfo': ValveDict,
        'normals': ValveDict,
        'distances': ValveDict,
        'alphas': ValveDict,
        'triangle_tags': ValveDict,
        'allowed_verts': ValveDict,
        'connections': list,
    }

    """docstring for ValveMap"""
    def __init__(self, filehandle, stdout=sys.stdout):
        entry_time = time.time()
        super(ValveMap, self).__init__()
        self.filehandle = filehandle
        self.stdout = stdout

        self.lines = self.bufcount()
        self.minupdate = self.lines // 400 or 10


        self.iterator = iter(self.filehandle.readline, '')
        self.mapdata = self._parse(ValveDict())
        self.elpsed_time = time.time() - entry_time
        self.stdout.write('\n%s\n' % self.elpsed_time)

        with open('dumps.vmfstuff', 'w') as fh:
            fh.write(pformat(self.mapdata))

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
            while True:
                line = next(self.iterator).rstrip('\n\r')
                self.i += 1
                if line.endswith('}'):
                    return output
                line = line[self.indent:]
                if 0 == self.i % self.minupdate:
                    self.report()

                if line.startswith('{'):
                    assert datatype in self.datatypes, "Unknown datatype [ %s ]" % datatype
                    self.indent += 1
                    value = self._parse(self.datatypes[datatype]())
                    if isinstance(output, dict):
                        if 'id' in value:
                            output[value['id']] = value
                        elif not datatype in output:
                            output['datatype'] = value
                        else:
                            if isinstance(list, output['datatype']):
                                output['datatype'].append(value)
                            else:
                                output['datatype'] = [output['datatype']].append(value)
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
                            self.stdout.write('Line %i: Duplicate key <%s> dropped\n' % (self.i, key))
                        output[key] = value
                    elif isinstance(output, list):
                        output.append((key, value))
                    continue


                datatype = line

        except StopIteration:
            assert 0 == len(self._parsenode)
            self.report()
            return output
        # except (TypeError) as err:
            # pprint(locals())
            # print(err)
        #     pprint((self.i, line, self.indent))
        #     pprint(locals())
        #     raise err
        #     # raise NotImplementedError(
            #     'Unable to parse file with error `%s`, %s' % (
            #         err,
            #         str((self.i, line, self.indent))
            #     )
            # )
            # # Potentially, if the error is being used to indicate an empty
            # # definition, the following line could be used to silence a
            # # potential parsing error
            # return (None, dict())

if '__main__' == __name__:
    with open('ttt_67thway/src/ttt_67thway.vmf', 'r') as maphandle:
        ValveMap(maphandle)
