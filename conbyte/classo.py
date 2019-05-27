import inspect
from conbyte.function import *

class Classo:
    def __init__(self, class_obj, ped):
        self.obj = class_obj
        self.name = class_obj.__name__
        self.functions = dict()

        ped = ped + " "
        for name, obj in inspect.getmembers(class_obj):
            if inspect.ismethod(obj):
                print(ped + "method", name)
                #dis.dis(obj)
                # print_inst(obj)
            if inspect.isfunction(obj):
                print(ped + "function ", name)
                #dis.dis(obj)
                # print_inst(obj)
                self.functions[name] = Function(obj)
    def get_func_names(self):
        funcs = []
        for func in self.functions:
            funcs.append(func)
        return funcs
