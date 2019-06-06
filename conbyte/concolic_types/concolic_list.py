from .concolic_type import *

class ConcolicList(ConcolicType):
    def __init__(self, expr, value=None):
        """
        self.expr = expr
        if value is None:
            self.value = "\'expr\'"
        else:
            self.value = value
        print("  Int  expr:", expr)
        """

