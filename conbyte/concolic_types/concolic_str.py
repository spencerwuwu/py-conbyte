from .concolic_type import *
from .concolic_int import *
from .concolic_list import *

log = logging.getLogger("ct.con.str")

class ConcolicStr(ConcolicType):
    def __init__(self, expr, value=None):
        self.expr = expr

        if value is None:
            self.value = expr
        else:
            self.value = value
        log.debug("ConStr, value: \'%s\', expr: %s" % (self.value, self.expr))
        

    def __add__(self, other):
        value = self.value + other.value
        expr = ["str.++", self.expr, other.expr]
        return ConcolicStr(expr, value)

    def __contains__(self, other):
        value = self.value.contains(other.value)
        expr = ["str.contains", self.expr, other.expr]
        return ConcolicType(expr, value)

    def __len__(self):
        value = len(self.value)
        expr = ["str.len", self.expr]
        return ConcolicInteger(expr, value)

    def __str__(self):
        return "{ConStr, value: \'%s\', expr: %s)" % (self.value, self.expr)

    def contains(self, other):
        value = other.value in self.value
        expr = ["str.contains", self.expr, other.expr]
        return ConcolicType(expr, value)

    def get_slice(self, start=None, stop=None):
        return ConcolicStr(self.value[start:stop])

    
    def find(self, findstr, beg=0):
        value = self.value.find(findstr.value, beg)
        expr = ["str.indexof", self.expr, findstr.expr, beg]
        return ConcolicInteger(expr, value)

    def startswith(self, prefix):
        value = self.value.startswith(prefix.value)
        expr = ["str.prefixof", prefix.expr, self.expr]
        return ConcolicType(expr, value)

    def split(self, sep=None, maxsplit=None):
        if isinstance(maxsplit, ConcolicInteger):
            maxsplit = maxsplit.value

        if sep is not None:
            if len(self.value) == 0:
                return ConcolicList([ConcolicStr("")])
        else:
            sep = ConcolicStr(" ")
            if len(self.value) == 0:
                return ConcolicList([ConcolicStr("")])
        if isinstance(sep, str):
            sep = ConcolicStr(sep)

        if maxsplit == 0 or sep.value not in self.value:
            return ConcolicList([self])
        else:
            sep_idx = self.find(sep).value
            if maxsplit is None:
                return ConcolicList([self.get_slice(0, sep_idx)]) + \
                   ConcolicList(self.get_slice(sep_idx + 1).split(sep))
            else:
                return ConcolicList([self.get_slice(0, sep_idx)]) + \
                   ConcolicList(self.get_slice(sep_idx + 1).split(sep, maxsplit - 1))

    # Return a new string, no continued expr
    def lower(self):
        value = self.value.lower()
        return ConcolicStr(value)

    def replace(self, old, new, maxreplace=-1):
        value = self.value
        expr = self.expr

        if isinstance(maxreplace, ConcolicInteger):
            maxreplace = maxreplace.value

        if maxreplace == 0:
            return ConcolicStr(expr, value)
        
        n_value = value.replace(old.value, new.value, 1)
        n_expr = ["str.replace", expr, old.expr, new.expr]
        if maxreplace > 0:
            maxreplace -= 1

        while n_value != value and (maxreplace == -1 or maxreplace > 0):
            value = n_value
            expr = n_expr
            n_value = value.replace(old.value, new.value, 1)
            n_expr = ["str.replace", expr, old.expr, new.expr]
            if maxreplace > 0:
                maxreplace -= 1

        return ConcolicStr(n_expr, n_value)

    
    # TODO
    """
    def __getitem__(self, key):
    """
    def count(self, sub):
        """String count is not a native function of the SMT solver. Instead, we implement count as a recursive series of
        find operations. Note that not all of the functionality of count is supported at this time, such as the start
        index."""
        if sub.value not in self.value:
            ret = ConcolicInteger(0)
        elif sub.value == "":
            ret = self.__len__() + 1
        else:
            find_idx = self.find(sub).value
            reststr = ConcolicStr(self.value[find_idx + sub.value.__len__():])
            ret = reststr.count(sub) + 1
        # assert int(ret) == str.count(str(self), str(sub))
        return ret


    # Return a new string, no continued expr
    def strip(self, chars=None):
        value = self.value.strip(chars)
        return ConcolicStr(value)

