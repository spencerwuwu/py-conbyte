# Copyright: copyright.txt
from .concolic_type import *

class ConcolicInteger(ConcolicType):
    def __init__(self, expr, value=None):
        self.expr = expr
        if value is None:
            self.value = 0
        else:
            self.value = value
        print("  Int  expr:", expr)

    """

    def __add__(self, addend):
        value = self.value + addend.value
        expr = ["+", self.expr, addend.expr]
        return ConcolicInteger(expr, value)

    def __sub__(self, subtrahend):
        value = self.value + subtrahend.value
        expr = ["-", self.expr, subtrahend.expr]
        return ConcolicInteger(expr, value)
    """

ops = [("add", "+"),
       ("sub", "-"),
       ("mul", "*"),
       ("mod", "%"),
       ("floordiv", "//"),
       ("and", "&"),
       ("or", "|"),
       ("xor", "^"),
       ("lshift", "<<"),
       ("rshift", ">>")]

def make_method(method, op, a):
    code = "def %s(self, other):\n" % method
    code += "   value = self.value %s other.value\n" % op
    code += "   expr = [\"%s\", self.expr, other.expr]\n" % op
    code += "   return ConcolicInteger(expr, value)"
    locals_dict = {}
    exec(code, globals(), locals_dict)
    setattr(ConcolicInteger, method, locals_dict[method])

for (name, op) in ops:
    method = "__%s__" % name
    make_method(method, op, "[self,other]")
    rmethod = "__r%s__" % name
    make_method(rmethod, op, "[other,self]")
