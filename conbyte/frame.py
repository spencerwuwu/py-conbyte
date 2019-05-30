from conbyte.utils import * 

class Frame:
    def __init__(self, frame):
        print("New Frame")
        """
        print("locals")
        for g_name in frame.f_locals:
            #print(g_name,":",frame.f_locals[g_name])
            print(" ", g_name)
        """
        self.frame = frame
        self.globals = frame.f_globals
        self.locals = frame.f_locals
        self.instructions = Queue()
        self.data_stack = Stack()
        """
        print("global")
        for g_name in frame.f_globals:
            if "__doc__" in g_name:
                continue
            if "__builtins__" in g_name:
                continue
            print(g_name,":",frame.f_globals[g_name])
        print()
        print()
        """
    def set_local(self):
        for local in self.locals:
            if local != "self":
                print(local)


    def execute_instructs(self):
        instructs = self.instructions
        while not instructs.is_empty():
            instruct = instructs.pop()
            print("instr",instruct)
            if instruct.opname == "CALL_FUNCTION":
                return
            else:
                continue

