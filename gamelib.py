
import valvemap

class TF2(valvemap.ValveMap):
    """docstring for TF2"""

    def __init__(self, *args, **kw):
        super(TF2, self).__init__(*args, **kw)
        self.itemlist = super(TF2, self).keys()

        # TF2 Defaults

        if None == self['world']['skyname']:
            self['world']['skyname'] = 'sky_tf2_04'

        if None == self['world']['detailvbsp']:
            self['world']['detailvbsp'] = 'detail_2fort.vbsp'

        if None == self['world']['detailmaterial']:
            self['world']['detailmaterial'] = 'detail/detailsprites_2fort'


