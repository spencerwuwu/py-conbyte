from .utils import * 
from .concolic_types.concolic_type import * 
from .concolic_types.concolic_int import * 
from .concolic_types.concolic_string import * 

class Executor:
    def __init__(self, path):
        self.path = path

    def execute_instr(self, call_stack, instruct):
        c_frame = call_stack.top()
        mem_stack = c_frame.mem_stack
        variables = c_frame.variables

        #
        # General instructions
        #

        if instruct.opname is "NOP":
            return


        #
        # Unary operations
        #

        #
        # Binary operations
        #

        elif instruct.opname is "BINARY_ADD":
            addend = mem_stack.pop()
            augend = mem_stack.pop()
            result = augend + addend
            mem_stack.push(result)

        elif instruct.opname is "BINARY_SUBTRACT":
            subtrahend = mem_stack.pop()
            minuend = mem_stack.pop()
            result = minuend - subtrahend
            mem_stack.push(result)

        #
        # In-place operations
        #

        #
        # Coroutine opcodes
        #

        #
        # Miscellaneous opcodes
        #

        elif instruct.opname is "LOAD_CONST":
            load_value = instruct.argval
            if isinstance(load_value, int):
                value = ConcolicInteger(load_value, load_value)
            elif isinstance(load_value, str):
                expr = '\"' + load_value + '\"'
                value = ConcolicString(expr, load_value)
            mem_stack.push(value)

        elif instruct.opname is "LOAD_FAST":
            load_name = instruct.argval
            mem_stack.push(variables[load_name])

        elif instruct.opname is "STORE_FAST":
            store_name = instruct.argval
            variables[store_name] = mem_stack.pop() 

        elif instruct.opname is "COMPARE_OP":
            op = instruct.argval
            comparand = mem_stack.pop()
            operand = mem_stack.pop()
            self.path.which_branch(operand.compare_op(op, comparand))
