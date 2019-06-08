# Copyright: see copyright.txt

import inspect
import functools

class ConcolicType(object):
    def __init__(self, expr=None, value=None):
        self.expr = expr
        self.value = value
        print("  Type expr:", expr)

    def get_concrete(self):
        return self.value
    
    def compare_op(self, operator, other):
        expr = [operator, self.expr, other.expr]
        val_l = self.value
        val_r = other.value
        if operator is "==":
            value = val_l == val_r
        if operator is "!=":
            value = val_l != val_r
        elif operator is ">":
            value = val_l > val_r
        elif operator is "<":
            value = val_l < val_r
        elif operator is ">=":
            value = val_l >= val_r
        elif operator is "<=":
            value = val_l <= val_r
        else:
            return None

        return ConcolicType(expr, value)

    def symbolic_eq(self, other):
        return self._eq_worker(self.expr, other.expr)

    def _eq_worker(self, expr1, expr2):
        if isinstance(expr1, list):
            if not isinstance(expr2, list):
                return False
            else:
                return expr1[0] == expr2[0] and \
                        self._eq_worker(expr1[1], expr2[1]) and \
                        self._eq_worker(expr1[2], expr2[2])
        else:
            return expr1 == expr2

    def __eq__(self, other):
        if self.value != other.value:
            return False
        else:
            return self.eq_worker(self.expr, other.expr)

    # For bool type
    def negate(self):
        self.value = not self.value
        self.expr = ['not', self.expr]
