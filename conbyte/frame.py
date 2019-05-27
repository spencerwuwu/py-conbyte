
class Frame:
    def __init__(self, frame):
        self.frame = frame
        self.globals = frame.f_globals
        self.locals = frame.f_locals
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
        print("locals")
        for g_name in frame.f_locals:
            if "__doc__" in g_name:
                continue
            if "__builtins__" in g_name:
                continue
            print(g_name,":",frame.f_locals[g_name])
        print()
        print()
        """
