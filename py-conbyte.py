#!/usr/bin/env python

import sys
import os
import logging
import dis
import inspect
from optparse import OptionParser
from optparse import OptionGroup

from symbolic.depend import *

TRACE_INTO = []
func = ""

def print_inst(obj):
    lines = dis.get_instructions(obj)
    for line in lines:
        print(line)

# TODO: Complete all types
def get_members(target_module):
    for name, obj in inspect.getmembers(target_module):
        if inspect.ismodule(obj):
            print("import", name)
            get_members(obj)

        if inspect.isclass(obj):
            print("class", name)
            for name_o, obj_o in inspect.getmembers(obj):
                if inspect.isfunction(obj_o):
                    print("function ", name_o)
                    #print_inst(obj_o)
            #dis.dis(obj)
        if inspect.ismethod(obj):
            print("method", name)
            #dis.dis(obj)
            # print_inst(obj)
        if inspect.isfunction(obj):
            print("function ", name)
            #dis.dis(obj)
            # print_inst(obj)
            return Function(obj)

def trace_lines(frame, event, arg):
    if event != 'line':
        return
    co = frame.f_code
    func_name = co.co_name
    line_no = frame.f_lineno
    filename = co.co_filename
    print('%s line %s' % (func_name, line_no))

    for line in func.get_instruct_by_line(line_no):
        print("\t", line)

def trace_calls(frame, event, arg):
    if event != 'call':
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name in TRACE_INTO:
        # Trace into this function
        return trace_lines





def main():
    usage = "usage: %prog [options] <path to a *.py file>"
    parser = OptionParser(usage=usage)

    # Setup
    setup_group = OptionGroup(parser, "Exploration Setup")
    setup_group.add_option("-s", "--start", dest="entry", action="store", help="Specify entry point", default="")
    parser.add_option_group(setup_group)

    (options, args) = parser.parse_args()
    if len(args) == 0 or not os.path.exists(args[0]):
        parser.error("Missing app to execute")
        sys.exit(1)

    base_name = os.path.basename(args[0])
    filename = os.path.abspath(args[0])
    print(filename)
    sys.path.append(filename.replace(base_name, ""))
    new_model = __import__(options.entry)
    # TEMP: dis.dis(new_model)

    global func
    func = get_members(new_model)
    execute = func.get_obj()
    global TRACE_INTO
    TRACE_INTO = [func.get_name()]
    sys.settrace(trace_calls)
    print(execute(1,2))
    sys.settrace(None)
    # TEMP: clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    

if __name__ == '__main__':
    main()
