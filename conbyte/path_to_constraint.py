# Copyright: see copyright.txt

from .predicate import Predicate
from .constraint import Constraint

class PathToConstraint:
    def __init__(self, add):
        self.constraints = []
        self.root_constraint = Constraint(None, None)
        self.current_constraint = self.root_constraint
        self.expected_path = None
        self.add = add

    def reset(self, expected):
        self.current_constraint = self.root_constraint
        if expected is None:
            self.expected_path = None
        else:
            self.expected_path = []
            tmp = expected
            while tmp.predicate is not None:
                self.expected_path.append(tmp.predicate)
                tmp = tmp.parent

    def which_branch(self, concolic_type):
        p = Predicate(concolic_type, concolic_type.value)
        c = self.current_constraint.find_child(p)
        p.negate()
        cneg = self.current_constraint.find_child(p)

        if c is None:
            c = self.current_constraint.add_child(p)
            # we add the new constraint to the queue of the engine for later processing
            self.add(c)

        self.current_constraint = c

        # check for path mismatch
        # IMPORTANT: note that we don't actually check the predicate is the
        # same one, just that the direction taken is the same
        if self.expected_path is not None and self.expected_path != []:
            expected = self.expected_path.pop()
            # while not at the end of the path, we expect the same predicate result
            # at the end of the path, we expect a different predicate result
            done = self.expected_path == []
            if (not done and expected.result != c.predicate.result or
                            done and expected.result == c.predicate.result):
                print("Replay mismatch (done=", done, ")")
                print(expected)
                print(c.predicate)

        if cneg is not None:
            # We've already processed both
            cneg.processed = True
            c.processed = True

        self.current_constraint = c


    def find_constraint(self, id):
        return self._find_constraint(self.root_constraint, id)

    def _find_constraint(self, constraint, id):
        if constraint.id == id:
            return constraint
        else:
            for child in constraint.children:
                found = self._find_constraint(child, id)
                if found is not None:
                    return found
        return None


