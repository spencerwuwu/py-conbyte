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

    def add(self):
        a = self.sa 
        b = self.inner.compare_add(self.sb)
        if b > 30:
            return b
        else:
            return a

def add(a, b):
    c = a + b
    return c


def simple(a, b):
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
    """
    f = TheClass(a, b)
    c = f.add()
    a = a * 2
    """
    """
    global glo
    glo = 2

    d = sub_import.sub_func(a, b) + sub_import.sub_func(a, b)
    e = sub_import.TheSubClass("abc")
    f = TheClass("def")
    f.get()
    """
    return c

def add_string(a, b):
    arr = [a, b, "gg"]
    c = arr[0]
    # c = a.split(",", 2)[0]
    #d = c.split(",")[0]
    return c
