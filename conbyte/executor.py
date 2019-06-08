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

        elif instruct.opname is "POP_TOP":
            mem_stack.pop()

        elif instruct.opname is "ROT_TWO":
            fir = mem_stack.pop()
            sec = mem_stack.pop()
            mem_stack.push(fir)
            mem_stack.push(sec)

        elif instruct.opname is "ROT_THREE":
            fir = mem_stack.pop()
            sec = mem_stack.pop()
            thi = mem_stack.pop()
            mem_stack.push(fir)
            mem_stack.push(thi)
            mem_stack.push(sec)

        elif instruct.opname is "DUP_TOP":
            top = mem_stack.top()
            mem_stack.push(top)

        elif instruct.opname is "DUP_TOP_TWO":
            fir = mem_stack.pop()
            sec = mem_stack.pop()
            mem_stack.push(sec)
            mem_stack.push(fir)
            mem_stack.push(sec)
            mem_stack.push(fir)

        #
        # Unary operations
        #

        elif instruct.opname is "UNARY_POSITIVE":
            return

        elif instruct.opname is "UNARY_NEGATIVE":
            target = mem_stack.pop()
            target.negate()
            mem_stack.push(target)

        elif instruct.opname is "UNARY_NOT":
            target = mem_stack.pop()
            target.negate()
            mem_stack.push(target)

        elif instruct.opname is "UNARY_INTERT":
            # TODO: maybe?
            target = mem_stack.pop()
            target.negate()
            mem_stack.push(target)

        elif instruct.opname is "GET_ITER":
            # TODO: 
            return

        elif instruct.opname is "GET_YIELD_FROM_ITER":
            # TODO: 
            return
        #
        # Binary operations
        #

        elif instruct.opname is "BINARY_POWER":
            # TODO: 
            return

        elif instruct.opname is "BINARY_MULTIPLY":
            multiplicand = mem_stack.pop()
            multiplier = mem_stack.pop()
            result = multiplicand * multiplier
            mem_stack.push(result)

        elif instruct.opname is "BINARY_MATRIX_MULTIPLY":
            # TODO: 
            return

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

        elif instruct.opname is "BINARY_SUBSCR":
            # TODO: 
            return

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

        elif instruct.opname is "INPLACE_POWER":
            # TODO: 
            return

        elif instruct.opname is "INPLACE_MULTIPLY":
            multiplicand = mem_stack.pop()
            multiplier = mem_stack.pop()
            result = multiplicand * multiplier
            mem_stack.push(result)

        elif instruct.opname is "INPLACE_MATRIX_MULTIPLY":
            # TODO: 
            return

        elif instruct.opname is "INPLACE_FLOOR_DIVIDE":
            divisor = mem_stack.pop()
            dividend = mem_stack.pop()
            result = dividend // divisor
            mem_stack.push(result)

        elif instruct.opname is "INPLACE_DIVIDE":
            divisor = mem_stack.pop()
            dividend = mem_stack.pop()
            result = dividend / divisor
            mem_stack.push(result)

        elif instruct.opname is "INPLACE_MODULO":
            divisor = mem_stack.pop()
            dividend = mem_stack.pop()
            result = dividend % divisor
            mem_stack.push(result)

        elif instruct.opname is "INPLACE_ADD":
            addend = mem_stack.pop()
            augend = mem_stack.pop()
            result = augend + addend
            mem_stack.push(result)

        elif instruct.opname is "INPLACE_SUBTRACT":
            subtrahend = mem_stack.pop()
            minuend = mem_stack.pop()
            result = minuend - subtrahend
            mem_stack.push(result)

        elif instruct.opname is "INPLACE_SUBSCR":
            # TODO: 
            return

        elif instruct.opname is "INPLACE_LSHIFT":
            to = mem_stack.pop()
            to1 = mem_stack.pop()
            result = to1 << to
            mem_stack.push(result)

        elif instruct.opname is "INPLACE_RSHIFT":
            to = mem_stack.pop()
            to1 = mem_stack.pop()
            result = to1 >> to
            mem_stack.push(result)

        elif instruct.opname is "INPLACE_AND":
            to = mem_stack.pop()
            to1 = mem_stack.pop()
            result = to1 & to
            mem_stack.push(result)

        elif instruct.opname is "INPLACE_XOR":
            to = mem_stack.pop()
            to1 = mem_stack.pop()
            result = to1 ^ to
            mem_stack.push(result)

        elif instruct.opname is "INPLACE_OR":
            to = mem_stack.pop()
            to1 = mem_stack.pop()
            result = to1 | to
            mem_stack.push(result)

        #
        # Coroutine opcodes
        #

        elif instruct.opname is "GET_AWAITABLE":
            # TODO: 
            return

        elif instruct.opname is "GET_AITER":
            # TODO: 
            return

        elif instruct.opname is "GET_ANEXT":
            # TODO: 
            return

        elif instruct.opname is "BEFORE_ASYNC_WITH":
            # TODO: 
            return

        elif instruct.opname is "SETUP_ASYNC_WITH":
            # TODO: 
            return

        #
        # Miscellaneous opcodes
        #

        elif instruct.opname is "PRINT_EXPR":
            return

        elif instruct.opname is "BREAK_LOOP":
            return

        elif instruct.opname is "CONTINUE_LOOP":
            return

        elif instruct.opname is "SET_ADD":
            # TODO
            return

        elif instruct.opname is "LIST_APPEND":
            # TODO
            return

        elif instruct.opname is "MAP_ADD":
            # TODO
            return

        elif instruct.opname is "RETURN_VALUE":
            ret_value = mem_stack.pop()
            if ret_value is None or ret_value is 0:
                if func_name is "__init__":
                    ret_value = variables["self"]
            mem_stack.push(ret_value)
            print("    Return: ", ret_value)
            return True

        elif instruct.opname is "YIELD_VALUE":
            # TODO
            return

        elif instruct.opname is "YIELD_FROM":
            # TODO
            return

        elif instruct.opname is "SETUP_ANNOTATIONS":
            # TODO
            return

        elif instruct.opname is "IMPORT_STAR":
            # TODO
            return

        elif instruct.opname is "POP_BLOCK":
            # TODO
            return

        elif instruct.opname is "POP_EXCEPT":
            # TODO
            return

        elif instruct.opname is "END_FINALLY":
            # TODO
            return

        elif instruct.opname is "WITH_CLEAN_START":
            # TODO
            return

        elif instruct.opname is "WITH_CLEAN_FINISH":
            # TODO
            return

        elif instruct.opname is "STORE_NAME":
            # TODO
            return

        elif instruct.opname is "DELETE_NAME":
            # TODO
            return

        elif instruct.opname is "UNPACK_SEQUENCE":
            # TODO
            return

        elif instruct.opname is "UNPACK_EX":
            # TODO
            return

        elif instruct.opname is "STORE_ATTR":
            attr_name = instruct.argval
            object_var = mem_stack.pop() 
            object_var.store_attr(attr_name, mem_stack.pop())

        elif instruct.opname is "DELETE_ATTR":
            # TODO
            return

        elif instruct.opname is "STORE_GLOBAL":
            # TODO
            return

        elif instruct.opname is "DELETE_GLOBAL":
            # TODO
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

        elif instruct.opname is "LOAD_NAME":
            # TODO
            return

        elif instruct.opname is "BUILD_TUPLE":
            # TODO
            return

        elif instruct.opname is "BUILD_LIST":
            # TODO
            return

        elif instruct.opname is "BUILD_MAP":
            # TODO
            return

        elif instruct.opname is "BUILD_CONST_KEY_MAP":
            # TODO
            return

        elif instruct.opname is "BUILD_STRING":
            # TODO
            return

        elif instruct.opname is "BUILD_TUPLE_UNPACK":
            # TODO
            return

        elif instruct.opname is "BUILD_TUPLE_UNPACK_WITH_CALL":
            # TODO
            return

        elif instruct.opname is "BUILD_LIST_UNPACK":
            # TODO
            return

        elif instruct.opname is "BUILD_SET_UNPACK":
            # TODO
            return

        elif instruct.opname is "BUILD_MAP_UNPACK":
            # TODO
            return

        elif instruct.opname is "BUILD_MAP_UNPACK_WITH_CALL":
            # TODO
            return

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

        elif instruct.opname is "COMPARE_OP":
            op = instruct.argval
            comparand = mem_stack.pop()
            operand = mem_stack.pop()
            self.path.which_branch(operand.compare_op(op, comparand))

        elif instruct.opname is "IMPORT_NAME":
            # TODO
            return

        elif instruct.opname is "IMPORT_FROM":
            # TODO
            return

        elif instruct.opname is "JUMP_FORWARD":
            # TODO
            return

        elif instruct.opname is "POP_JUMP_IF_TRUE":
            # TODO
            return

        elif instruct.opname is "POP_JUMP_IF_FALSE":
            # TODO
            return

        elif instruct.opname is "JUMP_IF_TRUE_OR_POP":
            # TODO
            return

        elif instruct.opname is "JUMP_IF_FALSE_OR_POP":
            # TODO
            return

        elif instruct.opname is "JUMP_ABSOLUTE":
            # TODO
            return

        elif instruct.opname is "FOR_ITER":
            # TODO
            return

        elif instruct.opname is "LOAD_GLOBAL":
            # TODO
            return

        elif instruct.opname is "SETUP_LOOP":
            # TODO
            return

        elif instruct.opname is "SETUP_EXCEPT":
            # TODO
            return

        elif instruct.opname is "SETUP_FINALLY":
            # TODO
            return

        elif instruct.opname is "LOAD_FAST":
            load_name = instruct.argval
            load_var = variables[load_name]
            mem_stack.push(load_var)

        elif instruct.opname is "STORE_FAST":
            store_name = instruct.argval
            var = mem_stack.pop() 
            variables[store_name] = var
            print("Store:", var)

        elif instruct.opname is "DELETE_FAST":
            # TODO
            return

        elif instruct.opname is "LOAD_CLOSURE":
            # TODO
            return

        elif instruct.opname is "LOAD_DEREF":
            # TODO
            return

        elif instruct.opname is "STORE_DEREF":
            # TODO
            return

        elif instruct.opname is "DELETE_DEREF":
            # TODO
            return

        elif instruct.opname is "RAISE_VARARGS":
            # TODO
            return

        elif instruct.opname is "CALL_FUNCTION":
            # Will not enter
            return

        elif instruct.opname is "CALL_FUNCTION_KW":
            # TODO
            return

        elif instruct.opname is "CALL_FUNCTION_EX":
            # TODO
            return

        elif instruct.opname is "LOAD_METHOD":
            return

        elif instruct.opname is "CALL_METHOD":
            return

        elif instruct.opname is "MAKE_FUNCTION":
            # TODO
            return

        elif instruct.opname is "BUILD_SLICE":
            # TODO
            return

        elif instruct.opname is "EXTENDED_ARG":
            # TODO
            return

        elif instruct.opname is "FORMAT_VALUE":
            # TODO
            return

        elif instruct.opname is "HAVE_ARGUMENT":
            # TODO
            return

