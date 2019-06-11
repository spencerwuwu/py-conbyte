import sub_import
from d_import import *

glo = 2

class InnerClass:
    def __init__(self, a):
        self.ia = a

    def __str__(self):
        return str(self.ia)
    
    def compare_add(self, t):
        if -self.ia < 2:
            self.ia += t
        else:
            self.ia = t
        return self.ia

class TheClass:
    def __init__(self, a, b):
        self.sa = a
        self.sb = b
        self.inner = InnerClass(a)

    def __str__(self):
        return "%s %s" % (self.sa, self.sb)

    def add(self, i):
        a = self.sa 
        b = self.inner.compare_add(self.sb)
        if b > 30:
            return b
        else:
            return a

def call_obj(a, b):
    d = sub_import.sub_func(a, b) + sub_import.sub_func(a, b)
    e = sub_import.TheSubClass("abc")
    c = TheClass(a, b)
    return c.add(glo)
