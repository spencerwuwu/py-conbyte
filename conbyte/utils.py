
class Stack:
    def __init__(self):
        self.stack = []

    def pop(self):
        self.stack.pop(0)
    
    def push(self, module):
        self.stack.insert(0, module)

    def top(self):
        return self.stack[0]
