from .utils import * 
from .concolic_types.concolic_type import * 
from .concolic_types.concolic_int import * 
from .concolic_types.concolic_str import * 
from .concolic_types.concolic_object import * 
from .concolic_types.concolic_list import * 

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
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "GET_YIELD_FROM_ITER":
            # TODO: 
            log.warning("%s Not support" % instruct.opname)
            return
        #
        # Binary operations
        #

        elif instruct.opname is "BINARY_POWER":
            # TODO: 
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "BINARY_MULTIPLY":
            multiplicand = mem_stack.pop()
            multiplier = mem_stack.pop()
            result = multiplicand * multiplier
            mem_stack.push(result)

        elif instruct.opname is "BINARY_MATRIX_MULTIPLY":
            # TODO: 
            log.warning("%s Not support" % instruct.opname)
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
            tos = mem_stack.pop()
            if isinstance(tos, ConcolicInteger):
                index = tos.value
                target_list = mem_stack.pop()
                mem_stack.push(target_list.get(index))
            elif isinstance(tos, int):
                index = tos
                target_list = mem_stack.pop()
                mem_stack.push(target_list.get(index))
            else:
                # Sliced object (Hopefully)
                mem_stack.push(tos)

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
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "INPLACE_MULTIPLY":
            multiplicand = mem_stack.pop()
            multiplier = mem_stack.pop()
            result = multiplicand * multiplier
            mem_stack.push(result)

        elif instruct.opname is "INPLACE_MATRIX_MULTIPLY":
            # TODO: 
            log.warning("%s Not support" % instruct.opname)
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
            log.warning("%s Not support" % instruct.opname)
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
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "GET_AITER":
            # TODO: 
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "GET_ANEXT":
            # TODO: 
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "BEFORE_ASYNC_WITH":
            # TODO: 
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "SETUP_ASYNC_WITH":
            # TODO: 
            log.warning("%s Not support" % instruct.opname)
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
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "LIST_APPEND":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "MAP_ADD":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "RETURN_VALUE":
            ret_value = mem_stack.pop()
            if ret_value is None or ret_value is 0:
                if func_name is "__init__":
                    ret_value = variables["self"]
            mem_stack.push(ret_value)
            log.debug("    Return: %s" % ret_value)
            return True

        elif instruct.opname is "YIELD_VALUE":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "YIELD_FROM":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "SETUP_ANNOTATIONS":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "IMPORT_STAR":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "POP_BLOCK":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "POP_EXCEPT":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "END_FINALLY":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "WITH_CLEAN_START":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "WITH_CLEAN_FINISH":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "STORE_NAME":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "DELETE_NAME":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "UNPACK_SEQUENCE":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "UNPACK_EX":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "STORE_ATTR":
            attr_name = instruct.argval
            object_var = mem_stack.pop() 
            object_var.store_attr(attr_name, mem_stack.pop())

        elif instruct.opname is "DELETE_ATTR":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "STORE_GLOBAL":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "DELETE_GLOBAL":
            # TODO
            log.warning("%s Not support" % instruct.opname)
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
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "BUILD_TUPLE":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "BUILD_LIST":
            size = instruct.argval
            new_list = ConcolicList()
            while size > 0:
                size -= 1
                new_list.append(mem_stack.pop())
            log.debug("List build reverse")
            new_list.value.reverse()
            mem_stack.push(new_list)

        elif instruct.opname is "BUILD_MAP":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "BUILD_CONST_KEY_MAP":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "BUILD_STRING":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "BUILD_TUPLE_UNPACK":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "BUILD_TUPLE_UNPACK_WITH_CALL":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "BUILD_LIST_UNPACK":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "BUILD_SET_UNPACK":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "BUILD_MAP_UNPACK":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "BUILD_MAP_UNPACK_WITH_CALL":
            # TODO
            log.warning("%s Not support" % instruct.opname)
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
            tos = mem_stack.pop()
            tos1 = mem_stack.pop()
            if op == "in":
                mem_stack.push(tos.contains(tos1))
            else:
                mem_stack.push(tos1.compare_op(str(op), tos))

        elif instruct.opname is "IMPORT_NAME":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "IMPORT_FROM":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "JUMP_FORWARD":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "POP_JUMP_IF_TRUE":
            self.path.which_branch(mem_stack.pop())
            return

        elif instruct.opname is "POP_JUMP_IF_FALSE":
            self.path.which_branch(mem_stack.pop())
            return

        elif instruct.opname is "JUMP_IF_TRUE_OR_POP":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "JUMP_IF_FALSE_OR_POP":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "JUMP_ABSOLUTE":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "FOR_ITER":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "LOAD_GLOBAL":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "SETUP_LOOP":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "SETUP_EXCEPT":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "SETUP_FINALLY":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "LOAD_FAST":
            load_name = instruct.argval
            load_var = variables[load_name]
            mem_stack.push(load_var)
            log.debug("Load: %s" % load_var)

        elif instruct.opname is "STORE_FAST":
            store_name = instruct.argval
            var = mem_stack.pop() 
            variables[store_name] = var
            log.debug("Store: %s" % var)

        elif instruct.opname is "DELETE_FAST":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "LOAD_CLOSURE":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "LOAD_DEREF":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "STORE_DEREF":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "DELETE_DEREF":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "RAISE_VARARGS":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "CALL_FUNCTION":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "CALL_FUNCTION_KW":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "CALL_FUNCTION_EX":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "LOAD_METHOD":
            method = instruct.argrepr
            target = mem_stack.pop()
            method_to_call = getattr(target, method)
            mem_stack.push(method_to_call)
            return

        elif instruct.opname is "CALL_METHOD":
            argv = instruct.argval
            args = []
            while argv > 0:
                args.append(mem_stack.pop())
                argv -= 1
            args.reverse()
            method_to_call = mem_stack.pop()
            mem_stack.push(method_to_call(*args))
            return

        elif instruct.opname is "MAKE_FUNCTION":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "BUILD_SLICE":
            argv = instruct.argval
            if argv > 2:
                log.error("Does not support genative step yet")
            args = []
            while argv > 0:
                var = mem_stack.pop().value
                if var < 0:
                    log.error("Does not support genative step yet")
                args.append(var)
                argv -= 1
            args.reverse()
            target = mem_stack.pop()
            mem_stack.push(target.get_slice(*args))

        elif instruct.opname is "EXTENDED_ARG":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "FORMAT_VALUE":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

        elif instruct.opname is "HAVE_ARGUMENT":
            # TODO
            log.warning("%s Not support" % instruct.opname)
            return

