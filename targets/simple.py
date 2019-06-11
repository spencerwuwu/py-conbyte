"""
import sub_import
from d_import import *


class TheClassB:
    def __init__(self, value:str):
        self.value = value

    def __str__(self):
        return self.value

    def get(self):
        return self.value
"""
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

def add(a, b):
    if a > b:
        c = a + b
    else:
        c = a - b
    return c


def simple(a, b):
    #f = TheClass(a, b)
    #c = f.add(3)
    return add(a, b)
    """
    fir = {}
    fir['a'] = 1

    sec = dict()
    sec['b'] = 1

    thi = {'a': 1, 'b': 2}
    if a > 5:
        c = a + b
    else:
        c = a - b
    if c > 100:
        if a > b:
            return 0
        else:
            return 2
    else:
        return 1
    a = a * 2
    """
    """
    d = sub_import.sub_func(a, b) + sub_import.sub_func(a, b)
    e = sub_import.TheSubClass("abc")
    f = TheClass("def")
    f.get()
    """
    return 
