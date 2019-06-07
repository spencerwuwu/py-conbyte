from .utils import * 
from .concolic_types.concolic_type import * 
from .concolic_types.concolic_int import * 
from .concolic_types.concolic_str import * 
from .concolic_types.concolic_object import * 

class Frame:
    def __init__(self, frame, mem_stack):
        # print("New Frame")
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
        self.variables = dict()
        self.mem_stack = mem_stack
        self.enter_object = None
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
    def init_locals(self):
        symbolic_inputs = dict()
        for local in self.locals:
            if local != "self":
                local_value = self.locals[local]
                # print(" local:", local, local_value)
                if isinstance(local_value, int):
                    concolic_var = ConcolicInteger(local, local_value)
                    symbolic_inputs[local] = "Int"
                elif isinstance(local_value, str):
                    concolic_var = ConcolicStr(local, local_value)
                    symbolic_inputs[local] = "String"
                self.variables[local] = concolic_var
        return symbolic_inputs

    def set_locals(self, mem_stack, is_init_object):
        for local in self.locals:
            print("   local:", local)
            if local != "self":
                var = mem_stack.pop()
                self.variables[local] = var
            else:
                if is_init_object:
                    self.variables[local] = ConcolicObject()
                else:
                    var = mem_stack.pop()
                    self.variables[local] = var

