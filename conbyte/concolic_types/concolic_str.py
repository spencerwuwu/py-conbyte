from .concolic_type import *
from .concolic_int import *

log = logging.getLogger("ct.con.str")

class ConcolicStr(ConcolicType):
    def __init__(self, expr, value=None):
        self.expr = expr
        if value is None:
            self.value = "\'expr\'"
        else:
            self.value = value
        log.debug("  Str  expr: %s" % expr)

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

    # TODO
    """
    def __getitem__(self, key):
    """
    def find(self, findstr, beg=0):
        value = self.value.find(findstr.value, beg)
        expr = ["str.indexof", self.expr, findstr.expr, beg]
        return ConcolicInteger(expr, value)
    
    def startswith(self, prefix):
        value = self.value.startswith(prefix.value)
        expr = ["str.prefixof", self.expr, prefix.expr]
        return ConcolicType(expr, value)
    
    def split(self, sep=None, maxsplit=None):
        if sep is not None:
            if len(self.value) == 0:
                return ConcolicStr("")
        else:
            sep = ConcolicStr(" ")
            if len(self.value) == 0:
                return []

        if sep.value not in self.value:
            return [self]
        else:
            sep_idx = self.find(sep)
            maxsplit = None if maxsplit is None else maxsplit - 1
            return [self[0:sep_idx]] + \
               self[sep_idx + 1:].split(sep, maxsplit)

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


    # TODO: only implement max_replace = -1
    def replace(self, old, new, maxreplace=-1):
        value = self.value.reaplce(old.value, new.value)
        expr = ["str.replaceall", self.expr, old.expr, new.expr]
        return ConcolicStr(value, expr)

    # Return a new string, no continued expr
    def strip(self, chars=None):
        value = self.value.strip(chars)
        return ConcolicStr(value)

    # Return a new string, no continued expr
    def lower(self):
        value = self.value.lower()
        return ConcolicStr(value)

