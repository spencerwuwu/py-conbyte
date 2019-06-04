from .concolic_type import *

class ConcolicInteger(ConcolicType):
    def __init__(self, expr, value=None):
        self.expr = expr
        if value is None:
            self.value = 0
        else:
            self.value = value
        print("  expr:", expr)


    def __add__(self, addend):
        value = self.value + addend.value
        expr = ["+", self.expr, addend.expr]
        return ConcolicInteger(expr, value)

