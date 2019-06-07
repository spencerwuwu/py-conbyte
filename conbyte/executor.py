from .utils import * 
from .concolic_types.concolic_type import * 
from .concolic_types.concolic_int import * 
from .concolic_types.concolic_str import * 
from .concolic_types.concolic_object import * 

class Executor:
    def __init__(self, path):
        self.path = path

    def execute_instr(self, call_stack, instruct, func_name=None):
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

        elif instruct.opname is "BINARY_MULTIPLY":
            multiplicand = mem_stack.pop()
            multiplier = mem_stack.pop()
            result = multiplicand * multiplier
            mem_stack.push(result)

        elif instruct.opname is "BINARY_FLOOR_DIVIDE":
            divisor = mem_stack.pop()
            dividend = mem_stack.pop()
            result = dividend // divisor
            mem_stack.push(result)

        elif instruct.opname is "BINARY_DIVIDE":
            divisor = mem_stack.pop()
            dividend = mem_stack.pop()
            result = dividend / divisor
            mem_stack.push(result)

        elif instruct.opname is "BINARY_MODULO":
            divisor = mem_stack.pop()
            dividend = mem_stack.pop()
            result = dividend % divisor
            mem_stack.push(result)

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

        elif instruct.opname is "BINARY_LSHIFT":
            to = mem_stack.pop()
            to1 = mem_stack.pop()
            result = to1 << to
            mem_stack.push(result)

        elif instruct.opname is "BINARY_RSHIFT":
            
            to = mem_stack.pop()
            to1 = mem_stack.pop()
            result = to1 >> to
            mem_stack.push(result)

        elif instruct.opname is "BINARY_AND":
            to = mem_stack.pop()
            to1 = mem_stack.pop()
            result = to1 & to
            mem_stack.push(result)

        elif instruct.opname is "BINARY_XOR":
            to = mem_stack.pop()
            to1 = mem_stack.pop()
            result = to1 ^ to
            mem_stack.push(result)

        elif instruct.opname is "BINARY_OR":
            to = mem_stack.pop()
            to1 = mem_stack.pop()
            result = to1 | to
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

        # TODO
        elif instruct.opname is "LOAD_GLOBAL":
            return

        elif instruct.opname is "LOAD_METHOD":
            return

        elif instruct.opname is "CALL_FUNCTION":
            # Will not enter
            return

        elif instruct.opname is "LOAD_CONST":
            load_value = instruct.argval
            if isinstance(load_value, int):
                value = ConcolicInteger(load_value, load_value)
            elif isinstance(load_value, str):
                expr = '\"' + load_value + '\"'
                value = ConcolicStr(expr, load_value)
            else:
                value = None
            mem_stack.push(value)

        elif instruct.opname is "LOAD_FAST":
            load_name = instruct.argval
            load_var = variables[load_name]
            mem_stack.push(load_var)

        elif instruct.opname is "LOAD_ATTR":
            load_name = instruct.argval
            object_var = mem_stack.pop() 
            if object_var.has_attr(load_name):
                load_attr = object_var.get_attr(load_name)
                mem_stack.push(load_attr)
            else:
                # Probally is calling a function
                # Store the object back, passing to the function as self
                mem_stack.push(object_var)

        elif instruct.opname is "RETURN_VALUE":
            ret_value = mem_stack.pop()
            if ret_value is None or ret_value is 0:
                if func_name is "__init__":
                    ret_value = variables["self"]
            mem_stack.push(ret_value)
            print("Return: ", ret_value)
            return True

        elif instruct.opname is "STORE_FAST":
            store_name = instruct.argval
            var = mem_stack.pop() 
            variables[store_name] = var
            print("Store:", var)

        elif instruct.opname is "STORE_ATTR":
            attr_name = instruct.argval
            object_var = mem_stack.pop() 
            object_var.store_attr(attr_name, mem_stack.pop())

        elif instruct.opname is "COMPARE_OP":
            op = instruct.argval
            comparand = mem_stack.pop()
            operand = mem_stack.pop()
            self.path.which_branch(operand.compare_op(op, comparand))
