# Copyright - see copyright.txt

class Predicate:
    def __init__(self, con, result):
        self.concolic = con
        self.result = result

    def negate(self):
        """Negates the current predicate"""
        assert (self.result is not None)
        self.result = not self.result

    def __eq__(self, other):
        if isinstance(other, Predicate):
            res = self.result == other.result and self.concolic.symbolic_eq(other.concolic)
            return res
        else:
            return False

    def get_formula(self):
        expr = self.concolic.expr
        formula =  self._get_formula(expr)
        if self.result is True:
            return "(assert " + formula + ")"
        else:
            return "(assert (not " + formula + "))\n"

    def _get_formula(self, expr):
        if isinstance(expr, list):
            operand = self._get_formula(expr[1])
            comparand = self._get_formula(expr[2])
            return "(" + expr[0] + " " + operand + " " + comparand + ")"
        else:
            return str(expr)

    def __str__(self):
        return "Result: %s\nExpr: %s" % (self.result, self.concolic.expr)
