from .concolic_type import *

log = logging.getLogger("ct.con.list")

class ConcolicList(ConcolicType):
    def __init__(self, value=None):
        self.expr = "LIST"
        if value is None:
            self.value = []
            self.size = 0
            log.debug("  List: empty")
            return
        elif isinstance(value, ConcolicList):
            self.value = value.value
            self.size = value.size
        else:
            self.value = value
            self.size = len(value)
        log.debug("  List: %s" % ",".join(val.__str__() for val in self.value))


    def append(self, element):
        self.value.append(element)
        self.size += 1
        log.debug("List append: %s", element)

    def get(self, index=0):
        return self.value[index]

    def get_slice(self, start=None, stop=None):
        return ConcolicList(self.value[start:stop])

    def contains(self, other):
        return ConcolicType('nil', None)

    def __str__(self):
        return "  List: %s" % ",".join(val.__str__() for val in self.value)
        
    def __add__(self, other):
        self.value += other.value
        self.size += other .size
        log.debug(self)
        return self

    def __radd__(self, other):
        self.value += other.value
        self.size += other .size
        return self

    def __len__(self):
        return self.size
