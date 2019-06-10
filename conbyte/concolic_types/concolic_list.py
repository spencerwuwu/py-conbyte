from .concolic_type import *

log = logging.getLogger("ct.con.list")

class ConcolicList(ConcolicType):
    def __init__(self, size = 0):
        self.expr = "LIST"
        self.value = []
        self.size = size
        log.debug("  List Init")

    def append(self, element):
        self.value.append(element)
        self.size += 1
        log.debug("List append: %s", element)

    def get(self, index=0):
        return self.value[index]

    def __str__(self):
        return "List[%s]" % self.size
        
