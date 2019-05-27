import inspect
from conbyte.classo import *
from conbyte.function import *


class Module:
    def __init__(self, target_module, ped):
        self.name = target_module.__name__
        self.sub_modules = []
        self.classoes = []
        self.methods = []
        self.functions = dict()

        # TODO: Complete all types
        ped = ped + " "
        for name, obj in inspect.getmembers(target_module):
            if inspect.ismodule(obj):
                print(ped + "module", name)
                self.sub_modules.append(Module(obj, ped))

            if inspect.isclass(obj):
                print(ped + "class", name)
                self.classoes.append(Classo(obj, ped))
                #print_inst(obj_o)
                #dis.dis(obj)
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
        for classo in self.classoes:
            funcs.extend(classo.get_func_names())
        for sub_module in self.sub_modules:
            funcs.extend(sub_module.get_func_names()) 
        return funcs


    # Return target module or class
    def load_global(self, target):
        for sub_module in self.sub_modules:
            if sub_module.name == target:
                return sub_module

        for classo in self.classoes:
            if classo.name == target:
                return classo
        return None


