from .concolic_type import *

log = logging.getLogger("ct.con.map")

class ConcolicMap(ConcolicType):
    def __init__(self, value=None):
        self.expr = "MAP"
        if value is None:
            self.value = dict()
            self.size = 0
            log.debug("  MAP: empty")
            return
        elif isinstance(value, ConcolicMap):
            self.value = value.value
            self.size = value.size
        else:
            self.value = value
            self.size = len(value)
        log.debug("  Map: %s" % ",".join("<%s: %s>" % (name.__str__(), val.__str__()) for name, val in self.value.items()))

    def __str__(self):
        if self.size == 0:
            return "  Map: nil"
        return "  Map: %s" % ",".join("<%s: %s>" % (name.__str__(), val.__str__()) for name, val in self.value.items())

    def get(self, name):
        return self.value[name]

    def store(self, name, val):
        if name not in self.value:
            self.size += 1
        self.value[name] = val
        log.debug("  Map store: <%s: %s>" % (name, val))
