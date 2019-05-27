#import sub_import
#from d_import import *

glo = 0

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
    c = add(a, b)
    """
    a = a + b
    d = sub_import.sub_func(a, b) + sub_import.sub_func(a, b)
    e = sub_import.TheSubClass("abc")

    global glo
    glo = 2
    """

    #f = TheDClass("def")
    f = TheClass("def")
    print(f.get())
    print(f)
    return 0

