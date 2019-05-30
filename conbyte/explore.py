import sys
import os
import logging
import dis
import inspect

from conbyte.utils import * 
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
        self.trace_into = []
        self.get_members(target_module)
        self.trace_into.append("__init__")
        self.trace_into.append("__str__")

        #dis.dis(target_module)

        self.call_stack = Stack()
        self.namespace_stack = Stack()


        """
        # Append builtin in trace_into
        """


    # TODO: Complete all types
    def get_members(self, target_module):
        for name, obj in inspect.getmembers(target_module):
            """
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
            """
            if inspect.isfunction(obj):
                print("function ", name)
                #dis.dis(obj)
                # print_inst(obj)
                self.trace_into.append(name)
                self.functions[name] = Function(obj)

    def get_line_instructions(self, lineno, instructions):
        instructs = []
        start_record = False
        i = 0
        for instruct in instructions:
            if start_record:
                if instruct.starts_line == None:
                    instructs.append(instruct)
                else:
                    break
            else:
                if instruct.starts_line != None:
                    if instruct.starts_line == lineno:
                        start_record = True
                        instructs.append(instruct)
            i += 1
        return instructs

    def execute_frame(self):
        if self.call_stack.is_empty():
            return
        self.call_stack.top().execute_instructs()
        return


    def trace_lines(self, frame, event, arg):

        if event != 'line' and event != 'return':
            return

        c_frame = self.call_stack.top()
        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        filename = co.co_filename
        print('%s line %s' % (func_name, line_no))
        instructions = self.get_line_instructions(line_no, dis.get_instructions(co))

        for line in instructions:
            c_frame.instructions.push(line)
            print("push", line)

        self.execute_frame()

        if event == 'return':
            print("Return")
            self.call_stack.pop()
            self.execute_frame()

    def trace_calls(self, frame, event, arg):
        if event != 'call':
            return
        co = frame.f_code
        func_name = co.co_name
        if func_name in self.trace_into:
            # Trace into this function
            current_frame = Frame(frame)
            # current_frame.set_local()
            self.call_stack.push(current_frame)
            return self.trace_lines

    def one_execution(self, entry):
        execute = self.functions[entry].obj
        sys.settrace(self.trace_calls)
        print(execute(1,2))
        sys.settrace(None)
