#!/usr/bin/env python

import sys
import os
import logging
import dis
import inspect
from optparse import OptionParser
from optparse import OptionGroup

def get_members(target_module):
    for name, obj in inspect.getmembers(target_module):
        if inspect.ismodule(obj):
            print("import", name)
            get_members(obj)

        if inspect.isclass(obj):
            print("class", name)
            dis.dis(obj)
        if inspect.ismethod(obj):
            print("method", name)
            dis.dis(obj)
        if inspect.isfunction(obj):
            print("function ", name)
            dis.dis(obj)

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
    #dis.dis(new_model)

    get_members(new_model)
    #clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    

if __name__ == '__main__':
    main()
