#!/usr/bin/env python3

import subprocess
import os

class VpkShell(object):

    FMT_TF2_BIN = '{home}/.local/share/Steam/steamapps/common/Team Fortress 2/bin'.format(
        home=os.path.expanduser('~')
    )

    SUBPROCESS_ENV = {
        'LD_LIBRARY_PATH': FMT_TF2_BIN,
        'PATH': FMT_TF2_BIN,
    }

    _index = None

    def __init__(self, parent, file_path):
        super(VpkShell, self).__init__()
        self.parent = parent
        self.file_path = file_path

        # import pdb; pdb.set_trace()
        for item in self.index:
            self.parent.liststore_directory.append([str(item), ''])

    @property
    def index(self):
        if self._index is None:
            self._index = subprocess.check_output(
                ['vpk_linux32', 'l', self.file_path],
                env=self.SUBPROCESS_ENV
            ).decode('ascii', 'ignore').strip().splitlines()

        return self._index


