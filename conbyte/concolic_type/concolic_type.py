

class ConcolicObject():
    def __init__(self, name, expr=None, value=None):
        self.name = name
        self.expr = expr
        self.value = value


    def get_concrete(self):
        return self.value
