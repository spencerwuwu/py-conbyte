from .concolic_type import *

class ConcolicObject(ConcolicType):
    def __init__(self):
        self.attrs = dict()

    def store_attr(self, name, value):
        self.attrs[name] = value

    def __str__(self):
        res = "Obj ["
        for name, value in self.attrs.items():
            res += "<%s: %s>" % (name, value)
        res += "]"
        return res
            
