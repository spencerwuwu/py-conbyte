import sys
import os
import logging
import dis
import inspect
from queue import PriorityQueue

from conbyte.utils import * 
from conbyte.module import * 
from conbyte.function import *
from conbyte.frame import *


def print_inst(obj):
    lines = dis.get_instructions(obj)
    for line in lines:
        print(line)

class ExplorationEngine:

    def __init__(self, path, filename, module):
        # Set up import environment
        sys.path.append(path)
        target_module = __import__(module)

        self.functions = dict()
        ped = " "
        # self.get_members(target_module, ped)

        self.root_module = Module(target_module, ped)

        self.trace_into = self.root_module.get_func_names()

        dis.dis(target_module)

        self.call_stack = Stack()

        """
        # Append builtin in trace_into
        self.trace_into.append("__init__")
        self.trace_into.append("__str__")
        """


    # TODO: Complete all types
    def get_members(self, target_module, ped):
        ped = ped + " "
        for name, obj in inspect.getmembers(target_module):
            if inspect.ismodule(obj):
                print(ped + "module", name)
                self.get_members(obj, ped)

            if inspect.isclass(obj):
                print(ped + "class", name)
                for name_o, obj_o in inspect.getmembers(obj):
                    if inspect.isfunction(obj_o):
                        print(ped + "function ", name_o)
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
                self.trace_into.append(name)
                self.functions[name] = Function(obj)

    def trace_return(self, frame, event, arg):
        self.call_stack.pop()
        return


    def trace_lines(self, frame, event, arg):
        if event == 'return':
            return self.trace_return

        if event != 'line':
            return

        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        filename = co.co_filename
        print('%s line %s' % (func_name, line_no))

        """
        for line in self.functions[func_name].get_instruct_by_line(line_no):
            print("\t", line)

        #self.call_stack.pop()
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


    def trace_calls(self, frame, event, arg):
        if event != 'call':
            return
        co = frame.f_code
        func_name = co.co_name
        if func_name in self.trace_into:
            # Trace into this function
            current_frame = Frame(frame)
            self.call_stack.push(current_frame)
            return self.trace_lines

    def one_execution(self, entry):
        execute = self.root_module.functions[entry].obj
        sys.settrace(self.trace_calls)
        print(execute(1,2))
        sys.settrace(None)
