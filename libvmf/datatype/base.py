
class ValveDict(dict):
    vmf_id = int
    allow_multiple = False

    def __init__(self, *args, **kw):
        super(ValveDict, self).__init__(*args, **kw)

    def __setitem__(self, key, value):
        if key == 'datatype':
            dict.__setitem__(self, key, value)
            return

        vmf_key = 'vmf_%s' % key
        if not hasattr(self, vmf_key):
            raise ValveKeyError(
                'Key `%s` not allowed in %s'
                % (key, self._type())
            )


        if isinstance(value, list):
            if not value[0].allow_multiple:
                raise ValveTypeError(
                    "Type %s does not allow allow multiple values"
                    % (type(value[0]))
                )
            # TODO, enforce datatype of list elements
            dict.__setitem__(self, key, value)
            return

        allowedcontainer = getattr(self, vmf_key)

        if not type(value) is allowedcontainer:
            # Lunacy!
            # Check if casting to the expected type and back vields
            # the same value
            if any([
                value is None,
                not type(value)(allowedcontainer(value)) == value
            ]):
                # We do not get the same value, we cannont cast
                raise ValveTypeError(
                    ("Illigal Type %s for key `%s`, "
                    + "expected Type %s for value `%s`") % (
                        type(value), key, allowedcontainer, value
                    )
                )

            # We can cast it, we have te technology!
            value = allowedcontainer(value)

        dict.__setitem__(self, key, value)

    def __str__(self):
        out = ''
        for key, value in self.items():
            out += '\t"%s" "%s"\n' % (key, value)
        return out

    def __repr__(self):
        return self.__str__()

    def _type(self):
        return self.__class__.__name__

ValveDict.vmf_datatype = ValveDict

class ValveClass(ValveDict):
    def __str__(self):
        out = ''
        for key, value in self.items():
            out += '\t%s {%s}\n' % (key, value)
        return out

    def __repr__(self):
        return self.__str__()

