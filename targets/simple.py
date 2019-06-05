import sub_import
from d_import import *

class TheClassB:
    def __init__(self, value:str):
        self.value = value

    def __str__(self):
        return self.value

    def get(self):
        return self.value

class TheClass:
    def __init__(self, value:str):
        self.value = value
        self.b = TheClassB(value)

    def __str__(self):
        return self.value

    def get(self):
        return self.value

def add(a, b):
    c = a + b
    return c


def simple(a, b):
    a = a - 2
    if a > 5:
        c = add(a, b)
        if c > 100:
            return 0
        else:
            return 1
    else:
        c = 3
    d = "abc"
    """

    global glo
    glo = 2

    d = sub_import.sub_func(a, b) + sub_import.sub_func(a, b)
    e = sub_import.TheSubClass("abc")
    f = TheDClass("def")
    f = TheClass("def")
    f.get()
    """
    return c

