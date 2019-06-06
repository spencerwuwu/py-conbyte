# Copyright: copyright.txt
from .concolic_type import *

class ConcolicInteger(ConcolicType):
    def __init__(self, expr, value=None):
        self.expr = expr
        if value is None:
            if isinstance(expr, int):
                self.value = expr
            else:
                self.value = int(expr)
        else:
            self.value = value
        print("  Int  expr:", expr)

    def __int__(self):
        return self.value

    def __str__(self):
        return str(self.value)

ops = [("add", "+", "+"),
       ("sub", "-", "-"),
       ("mul", "*", "*"),
       ("mod", "%", "mod"),
       ("div", "/", "div"),
       ("floordiv", "//", "div"),
       ("and", "&", "&"),
       ("or", "|", "|"),
       ("xor", "^", "^"),
       ("lshift", "<<", "<<"),
       ("rshift", ">>", ">>")]

def make_method(method, op, op_smt):
    code = "def %s(self, other):\n" % method
    code += "   value = self.value %s other.value\n" % op
    code += "   expr = [\"%s\", self.expr, other.expr]\n" % op_smt
    code += "   return ConcolicInteger(expr, value)"
    locals_dict = {}
    exec(code, globals(), locals_dict)
    setattr(ConcolicInteger, method, locals_dict[method])

for (name, op, op_smt) in ops:
    method = "__%s__" % name
    make_method(method, op, op_smt)
    rmethod = "__r%s__" % name
    make_method(rmethod, op, op_smt)
