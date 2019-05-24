import sub_import

class TheClass:
    def __init__(self, value:str):
        self.value = value

    def __str__(self):
        return self.value

def add(a, b):
    c = a + b
    return c


def simple(a, b):
    a = a + b
    c = add(a, b)
    d = sub_import.sub_func(a, b)
    e = sub_import.TheSubClass("abc")
    return c

