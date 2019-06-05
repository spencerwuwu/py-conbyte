import sys
import os
import logging
import dis
import inspect

from .utils import * 
from .function import *
from .frame import *
from .executor import *
from .path_to_constraint import *

from .concolic_types import concolic_type
from .z3_wrapper import Z3Wrapper


def print_inst(obj):
    lines = dis.get_instructions(obj)
    for line in lines:
        print(line)

class ExplorationEngine:

    def __init__(self, path, filename, module, entry):
        # Set up import environment
        sys.path.append(path)
        target_module = __import__(module)
        self.entry = entry

        self.trace_into = []
        self.functions = dict()
        self.get_members(target_module)
        self.z3_wrapper = Z3Wrapper()

        self.symbolic_inputs = None 
        self.new_constraints = []
        self.constraints_to_solve = Queue()
        self.solved_constraints = Queue()
        self.finished_constraints = []
        self.num_processed_constraints = 0

        #dis.dis(target_module)

        self.call_stack = Stack()
        self.mem_stack = Stack()

        self.path = PathToConstraint(lambda c: self.add_constraint(c))
        self.executor = Executor(self.path)

        """
        # Append builtin in trace_into
        """
        self.trace_into.append("__init__")
        self.trace_into.append("__str__")

    def add_constraint(self, constraint):
        self.new_constraints.append(constraint)

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
                # print("function ", name)
                # dis.dis(obj)
                # print_inst(obj)
                self.trace_into.append(name)
                self.functions[name] = Function(obj)

    def execute_instructs(self, frame):
        instructs = frame.instructions
        while not instructs.is_empty():
            instruct = instructs.pop()
            # print(" instr", instruct.opname, instruct.argval, instruct.argrepr)
            if instruct.opname == "CALL_FUNCTION":
                return
            elif instruct.opname == "CALL_METHOD":
                return
            else:
                re = self.executor.execute_instr(self.call_stack, instruct)

    def execute_frame(self):
        if self.call_stack.is_empty():
            return
        current_frame = self.call_stack.top()
        self.execute_instructs(current_frame)
        # print("")
        return


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

    def trace_lines(self, frame, event, arg):

        if event != 'line' and event != 'return':
            return

        c_frame = self.call_stack.top()
        co = frame.f_code
        func_name = co.co_name
        line_no = frame.f_lineno
        filename = co.co_filename
        # print('%s line %s' % (func_name, line_no))
        instructions = self.get_line_instructions(line_no, dis.get_instructions(co))

        for instruct in instructions:
            c_frame.instructions.push(instruct)
            # print(" push", instruct.opname, instruct.argval, instruct.argrepr)

        self.execute_frame()

        if event == 'return':
            # print("Return")
            self.call_stack.pop()
            self.execute_frame()

    def trace_calls(self, frame, event, arg):
        if event != 'call':
            return
        co = frame.f_code
        func_name = co.co_name
        if func_name in self.trace_into:
            # Trace into this function
            current_frame = Frame(frame, self.mem_stack)
            if not self.call_stack.is_empty():
                current_frame.set_locals(self.call_stack.top().mem_stack)
            else:
                self.symbolic_inputs = current_frame.init_locals()
                self.z3_wrapper.set_variables(self.symbolic_inputs)
            # current_frame.set_local()
            self.call_stack.push(current_frame)
            return self.trace_lines

    def _is_exploration_complete(self):
        num_constr = self.constraints_to_solve.q_size()
        if num_constr == 0 and self.solved_constraints.is_empty():
            return True
        else:
            return False

    def explore(self, max_iterations=0, timeout=None):
        # TODO: Initialize arguments
        execute = self.functions[self.entry].obj
        var_n = execute.__code__.co_argcount
        init_vars = [] 
        for i in range(var_n):
            init_vars.append(i)

        # First Execution
        self._one_execution(init_vars)
        iterations = 1

        # TODO: Currently single thread
        while not self._is_exploration_complete():
            if max_iterations != 0 and iterations >= max_iterations:
                break
                
            if not self.solved_constraints.is_empty():
                selected_id, result, model = self.solved_constraints.pop()

                if selected_id in self.finished_constraints:
                    continue

                selected_constraint = self.path.find_constraint(selected_id)
            else:
                while not self.constraints_to_solve.is_empty():
                    target = self.constraints_to_solve.pop()
                    asserts, query = target.get_asserts_and_query()
                    ret, model = self.z3_wrapper.find_counter_example(asserts, query)
                    self.solved_constraints.push((target.id, ret, model))
                continue

            if model is not None:
                args = self._recordInputs(model)
                self._one_execution(args, selected_constraint)
                iterations += 1
                self.num_processed_constraints += 1
            self.finished_constraints.append(selected_id)

    def _getInputs(self):
        return self.symbolic_inputs.copy()

    def _recordInputs(self, model):
        args = []
        for name, value in model.items():
            args.append(value)
        return args


    def _one_execution(self, init_vars, expected_path=None):
        print("Inputs: " + str(init_vars))

        self.path.reset(expected_path)

        execute = self.functions[self.entry].obj
        sys.settrace(self.trace_calls)
        execute(*init_vars)
        sys.settrace(None)

        while len(self.new_constraints) > 0:
            constraint = self.new_constraints.pop()
            constraint.inputs = self._getInputs()
            self.constraints_to_solve.push(constraint)

