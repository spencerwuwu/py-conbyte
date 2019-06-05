
class Stack:
    def __init__(self):
        self.stack = []

    def pop(self):
        return self.stack.pop(0)
    
    def push(self, item):
        self.stack.insert(0, item)

    def top(self):
        return self.stack[0]

    def s_size(self):
        return len(self.queue)

    def is_empty(self):
        if len(self.stack) != 0:
            return False
        else:
            return True

class Queue:
    def __init__(self):
        self.queue = []

    def head(self):
        return self.queue[0]

    def pop(self):
        return self.queue.pop(0)

    def push(self, item):
        self.queue.append(item)

    def q_size(self):
        return len(self.queue)

    def is_empty(self):
        if len(self.queue) != 0:
            return False
        else:
            return True
