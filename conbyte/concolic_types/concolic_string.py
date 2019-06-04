from .concolic_type import *

class ConcolicString(ConcolicType):
    def __init__(self, expr=None, value=None):
        self.expr = expr
        self.value = value
        print("  expr:", expr)


    def __add__(self, addend):
        value = self.value + addend.value
        expr = ["+", self.expr, addend.expr]
        return ConcolicInteger(expr, value)


