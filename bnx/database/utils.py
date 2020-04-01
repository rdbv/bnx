
class SelfFillClass:

    fields = []
    types = []

    def __init__(self, *args, **kwargs):
        self._init_fields()

        if len(args):
            if type(args[0]) == type(()) and len(args[0]) > 0:
                for i in range(len(args[0])):
                    if type(self.types[i]) == type(None):
                        self.__dict__[self.fields[i]] = args[0][i]
                    else:
                        self.__dict__[self.fields[i]] = self.types[i](args[0][i])
        else:
            for (k, v) in kwargs.items():
                if k in self.fields:
                    self.__dict__[k] = v

    def _init_fields(self):
        for field in self.fields:
            self.__dict__[field] = None

    def __repr__(self):
        out = ""

        for v in self.fields:
            out += "%s:%s " % (v, str(self.__dict__[v]))

        return out
