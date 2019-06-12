import logging

from .utils import * 
from .concolic_types.concolic_type import * 
from .concolic_types.concolic_int import * 
from .concolic_types.concolic_str import * 
from .concolic_types.concolic_object import * 
from .concolic_types.concolic_list import * 
from .concolic_types.concolic_map import * 

log = logging.getLogger("ct.executor")

class Executor:
    def __init__(self, path):
        self.path = path
        self.overwrite_method = False

    def _handle_jump(self, frame, instruct):
        offset = instruct.argval
        frame.next_offset = offset
        if instruct.offset > offset:
            frame.instructions.sanitize()
    
    # Implement builtin range()
    def _do_range(self, argv, mem_stack):
        args = []
        for i in range(argv):
            var = mem_stack.pop().value
            args.append(var)
        args.reverse()
        r_list = ConcolicList()
        for i in range(*args):
            r_list.append(ConcolicInteger(i))
        return r_list 

    # Implement builtin sum()
    def _do_sum(self, array):
        ret = ConcolicInteger(0)
        for element in array.value:
            ret += element
        return ret

    # Implement builtin max()
    def _do_max(self, a, b):
        value = a.value if a.value > b.value else b.value
        expr = ["ite", [">", a.expr, b.expr], a.expr, b.expr]
        return ConcolicInteger(expr, value)

    # Implement builtin min()
    def _do_min(self, a, b):
        value = a.value if a.value < b.value else b.value
        expr = ["ite", ["<", a.expr, b.expr], a.expr, b.expr]
        return ConcolicInteger(expr, value)

    def constant_compare(self, operator, val_l, val_r):
        if isinstance(val_l, str):
            expr_l = '\"' + val_l + '\"' 
        else:
            expr_l = val_l
        if isinstance(val_r, str):
            expr_r = '\"' + val_r + '\"' 
        else:
            expr_r = val_r

        if operator == "==":
            value = val_l == val_r
            expr = ["=", expr_l, val_r]
        elif operator == "!=":
            value = val_l != val_r
            expr = ['not', ["=", expr_l, val_r]]
        elif operator == ">":
            value = val_l > val_r
            expr = [operator, expr_l, val_r]
        elif operator == "<":
            value = val_l < val_r
            expr = [operator, expr_l, val_r]
        elif operator == ">=":
            value = val_l >= val_r
            expr = [operator, expr_l, val_r]
        elif operator == "<=":
            value = val_l <= val_r
            expr = [operator, expr_l, val_r]
        else:
            return None

        return ConcolicType(expr, value)

    def execute_instr(self, call_stack, instruct, func_name=None):
        c_frame = call_stack.top()
        mem_stack = c_frame.mem_stack
        variables = c_frame.variables
        g_variables = c_frame.g_variables

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
            # Get a queue
            tos = mem_stack.pop()
            mem_stack.push(tos.get_iter())
            return

        elif instruct.opname is "GET_YIELD_FROM_ITER":
            # TODO: 
            log.warning("%s Not implemented" % instruct.opname)
            return
        #
        # Binary operations
        #

        elif instruct.opname is "BINARY_POWER":
            # TODO: 
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "BINARY_MULTIPLY":
            multiplicand = mem_stack.pop()
            multiplier = mem_stack.pop()
            result = multiplicand * multiplier
            mem_stack.push(result)

        elif instruct.opname is "BINARY_MATRIX_MULTIPLY":
            # TODO: 
            log.warning("%s Not implemented" % instruct.opname)
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
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "INPLACE_MULTIPLY":
            multiplicand = mem_stack.pop()
            multiplier = mem_stack.pop()
            result = multiplicand * multiplier
            mem_stack.push(result)

        elif instruct.opname is "INPLACE_MATRIX_MULTIPLY":
            # TODO: 
            log.warning("%s Not implemented" % instruct.opname)
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
            log.warning("%s Not implemented" % instruct.opname)
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

        elif instruct.opname is "STORE_SUBSCR":
            tos = mem_stack.pop()
            if isinstance(tos, ConcolicInteger) or \
               isinstance(tos, ConcolicStr):
                tos = tos.value
            tos1 = mem_stack.pop()
            tos2 = mem_stack.pop()
            tos1.store(tos, tos2)

        elif instruct.opname is "DELETE_SUBSCR":
            # TODO: 
            log.warning("%s Not implemented" % instruct.opname)
            return

        #
        # Coroutine opcodes
        #

        elif instruct.opname is "GET_AWAITABLE":
            # TODO: 
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "GET_AITER":
            # TODO: 
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "GET_ANEXT":
            # TODO: 
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "BEFORE_ASYNC_WITH":
            # TODO: 
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "SETUP_ASYNC_WITH":
            # TODO: 
            log.warning("%s Not implemented" % instruct.opname)
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
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "LIST_APPEND":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "MAP_ADD":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
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
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "YIELD_FROM":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "SETUP_ANNOTATIONS":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "IMPORT_STAR":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "POP_BLOCK":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "POP_EXCEPT":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "END_FINALLY":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "WITH_CLEAN_START":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "WITH_CLEAN_FINISH":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "STORE_NAME":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "DELETE_NAME":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "UNPACK_SEQUENCE":
            size = instruct.argval
            seqs = mem_stack.pop()
            for seq in seqs:
                if isinstance(seq, int):
                    value = ConcolicInteger(seq, seq)
                elif isinstance(seq, str):
                    expr = '\"' + seq + '\"'
                    value = ConcolicStr(seq, seq)
                else:
                    value = None
                mem_stack.push(value)
            return

        elif instruct.opname is "UNPACK_EX":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "STORE_ATTR":
            attr_name = instruct.argval
            object_var = mem_stack.pop() 
            object_var.store_attr(attr_name, mem_stack.pop())

        elif instruct.opname is "DELETE_ATTR":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "STORE_GLOBAL":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "DELETE_GLOBAL":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "LOAD_CONST":
            load_value = instruct.argval
            if isinstance(load_value, int):
                value = ConcolicInteger(load_value, load_value)
            elif isinstance(load_value, str):
                expr = '\"' + load_value + '\"'
                value = ConcolicStr(expr, load_value)
            else:
                value = load_value
            mem_stack.push(value)

        elif instruct.opname is "LOAD_NAME":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "BUILD_TUPLE":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "BUILD_LIST":
            size = instruct.argval
            new_list = ConcolicList()
            while size > 0:
                size -= 1
                new_list.append(mem_stack.pop())
            log.debug("     List build reverse")
            new_list.value.reverse()
            mem_stack.push(new_list)

        elif instruct.opname is "BUILD_MAP":
            mem_stack.push(ConcolicMap())
            return

        elif instruct.opname is "BUILD_CONST_KEY_MAP":
            names = mem_stack.pop()
            size = instruct.argval
            build_map = ConcolicMap()
            for i in range(size):
                build_map.store(names[i], mem_stack.pop())
            mem_stack.push(build_map)
            return

        elif instruct.opname is "BUILD_STRING":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "BUILD_TUPLE_UNPACK":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "BUILD_TUPLE_UNPACK_WITH_CALL":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "BUILD_LIST_UNPACK":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "BUILD_SET_UNPACK":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "BUILD_MAP_UNPACK":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "BUILD_MAP_UNPACK_WITH_CALL":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
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
                if isinstance(tos1, ConcolicInteger) or \
                   isinstance(tos1, ConcolicStr):
                    mem_stack.push(tos1.compare_op(str(op), tos))
                else:
                    mem_stack.push(self.constant_compare(op, tos1, tos))

        elif instruct.opname is "IMPORT_NAME":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "IMPORT_FROM":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "JUMP_FORWARD":
            # TODO
            self._handle_jump(c_frame, instruct)
            return

        elif instruct.opname is "POP_JUMP_IF_TRUE":
            condition = mem_stack.pop()
            if condition.value:
                self._handle_jump(c_frame, instruct)
            self.path.which_branch(condition)
            return

        elif instruct.opname is "POP_JUMP_IF_FALSE":
            condition = mem_stack.pop()
            if not condition.value:
                self._handle_jump(c_frame, instruct)
            self.path.which_branch(condition)
            return

        elif instruct.opname is "JUMP_IF_TRUE_OR_POP":
            # TODO
            log.warning("%s Not checked" % instruct.opname)
            condition = mem_stack.top()
            self.path.which_branch(condition)
            if condition.value:
                self._handle_jump(c_frame, instruct)
            else:
                mem_stack.pop()

        elif instruct.opname is "JUMP_IF_FALSE_OR_POP":
            # TODO
            log.warning("%s Not checked" % instruct.opname)
            condition = mem_stack.top()
            self.path.which_branch(condition)
            if not condition.value:
                self._handle_jump(c_frame, instruct)
            else:
                mem_stack.pop()

        elif instruct.opname is "JUMP_ABSOLUTE":
            self._handle_jump(c_frame, instruct)
            return

        elif instruct.opname is "FOR_ITER":
            next_offset = instruct.argval
            if not mem_stack.top().is_empty():
                mem_stack.push(mem_stack.top().pop())
            else:
                mem_stack.pop()
                c_frame.next_offset = next_offset
            return

        elif instruct.opname is "LOAD_GLOBAL":
            # TODO
            if instruct.argval in g_variables:
                load_var = instruct.argval
                mem_stack.push(g_variables[load_var])
            else:
                mem_stack.push(instruct.argval)
            return

        elif instruct.opname is "SETUP_LOOP":
            return

        elif instruct.opname is "SETUP_EXCEPT":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "SETUP_FINALLY":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "LOAD_FAST":
            load_name = instruct.argval
            load_var = variables[load_name]
            mem_stack.push(load_var)
            log.debug("     Load: %s" % load_var)

        elif instruct.opname is "STORE_FAST":
            store_name = instruct.argval
            var = mem_stack.pop() 
            variables[store_name] = var
            log.debug("     Store: %s" % var)

        elif instruct.opname is "DELETE_FAST":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "LOAD_CLOSURE":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "LOAD_DEREF":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "STORE_DEREF":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "DELETE_DEREF":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "RAISE_VARARGS":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "CALL_FUNCTION":
            """ 
            Note: arg will be handled in explore.trace_call
            """
            # Get the function stored
            argv = instruct.argval
            args = Stack()
            for i in range(argv):
                args.push(mem_stack.pop())
            func = mem_stack.pop()
            for i in range(argv):
                mem_stack.push(args.pop())

            # Especially handle
            # Overwrite: implemented in classes
            overwrite = ["len", "int", "join"]
            if func in overwrite:
                target = mem_stack.pop()
                if isinstance(target, ConcolicList) or \
                   isinstance(target, ConcolicMap):
                    mem_stack.push(ConcolicInteger(target.size))
                    return
                function_to_call = getattr(target, func)
                mem_stack.push(function_to_call())
            elif func == "str":
                target = mem_stack.pop()
                if isinstance(target, ConcolicInteger):
                    mem_stack.push(ConcolicStr(target.get_str()))
                else:
                    mem_stack.push(str(target))
            elif func == "dict":
                mem_stack.push(ConcolicMap())
                # TODO
                if argv != 0:
                    log.warrning("Not implemented: dict(<with args>)")
            elif func == "list":
                new_list = ConcolicList()
                for i in range(argv):
                    new_list.append(mem_stack.pop())
                mem_stack.push(new_list)
            elif func == "range":
                range_list = self._do_range(argv, mem_stack)
                mem_stack.push(range_list)
            elif func == "sum":
                value = self._do_sum(mem_stack.pop())
                mem_stack.push(value)
            elif func == "max":
                b = mem_stack.pop()
                a = mem_stack.pop()
                mem_stack.push(self._do_max(a, b))
            elif func == "min":
                b = mem_stack.pop()
                a = mem_stack.pop()
                mem_stack.push(self._do_min(a, b))
            return

        elif instruct.opname is "CALL_FUNCTION_KW":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "CALL_FUNCTION_EX":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "LOAD_METHOD":
            method = instruct.argrepr
            target = mem_stack.pop()
            if isinstance(target, ConcolicInteger) or \
               isinstance(target, ConcolicStr) or \
               isinstance(target, ConcolicMap) or \
               isinstance(target, ConcolicList):
                method_to_call = getattr(target, method)
                mem_stack.push(method_to_call)
                self.overwrite_method = True
                log.debug("Load overwite: %s" % method)
            else:
                # Pass in as self
                if isinstance(target, ConcolicObject):
                    mem_stack.push(target)
                self.overwrite_method = False
                log.debug("Load outside: %s" % method)
            return

        elif instruct.opname is "CALL_METHOD":
            if self.overwrite_method:
                argv = instruct.argval
                args = []
                for i in range(argv):
                    args.append(mem_stack.pop())
                args.reverse()
                method_to_call = mem_stack.pop()
                mem_stack.push(method_to_call(*args))
                self.overwrite_method = False
            else:
                return

        elif instruct.opname is "MAKE_FUNCTION":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "BUILD_SLICE":
            argv = instruct.argval
            if argv > 2:
                log.error("Does not support genative step yet")
            args = []
            while argv > 0:
                var = mem_stack.pop()
                if var.value < 0:
                    log.error("Does not support genative step yet")
                args.append(var)
                argv -= 1
            args.reverse()
            target = mem_stack.pop()
            mem_stack.push(target.get_slice(*args))

        elif instruct.opname is "EXTENDED_ARG":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "FORMAT_VALUE":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

        elif instruct.opname is "HAVE_ARGUMENT":
            # TODO
            log.warning("%s Not implemented" % instruct.opname)
            return

