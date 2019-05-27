#!/usr/bin/env python

import sys
import os
import logging
import dis
import inspect
from optparse import OptionParser
from optparse import OptionGroup

from conbyte.function import *
from conbyte.explore import *

TRACE_INTO = []
FUNCTIONS = dict()

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
            global TRACE_INTO
            TRACE_INTO.append(name)
            global FUNCTIONS
            FUNCTIONS[name] = Function(obj)

def trace_lines(frame, event, arg):
    if event != 'line':
        return
    co = frame.f_code
    func_name = co.co_name
    line_no = frame.f_lineno
    filename = co.co_filename
    print('%s line %s' % (func_name, line_no))

    for line in FUNCTIONS[func_name].get_instruct_by_line(line_no):
        print("\t", line)

def trace_calls(frame, event, arg):
    if event != 'call':
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name in TRACE_INTO:
        # Trace into this function
        print("global")
        for g_name in frame.f_globals:
            if "__doc__" in g_name:
                continue
            if "__builtins__" in g_name:
                continue
            print(g_name,":",frame.f_globals[g_name])
        print()
        print()
        print("locals")
        for g_name in frame.f_locals:
            if "__doc__" in g_name:
                continue
            if "__builtins__" in g_name:
                continue
            print(g_name,":",frame.f_locals[g_name])
        print()
        print()
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
    path = filename.replace(base_name, "")
    module = base_name.replace(".py", "")
    engine = ExplorationEngine(path, filename, module)

    engine.one_execution(options.entry)
    

if __name__ == '__main__':
    main()
