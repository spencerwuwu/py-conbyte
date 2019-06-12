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



def main():
    usage = "usage: %prog [options] <path to a *.py file>"
    parser = OptionParser(usage=usage)

    # Setup
    setup_group = OptionGroup(parser, "Exploration Setup")
    setup_group.add_option("-e", "--entry", dest="entry", action="store", help="Specify entry point", default=None)
    setup_group.add_option("-i", "--input", dest="inputs", action="store", help="Specify initial inputs", default="")
    parser.add_option_group(setup_group)

    # Logging configuration
    logging_group = OptionGroup(parser, "Logging Configuration")
    logging_group.add_option("--debug", dest='debug', action="store_true", help="Enable debugging log")
    logging_group.add_option("-q", "--query", dest='query', action="store", help="Store smt queries", default=None)

    parser.add_option_group(logging_group)
    (options, args) = parser.parse_args()
    if len(args) == 0 or not os.path.exists(args[0]):
        parser.error("Missing app to execute")
        sys.exit(1)

    if options.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    # logging.basicConfig(level=logging.INFO, format='%(asctime)s\t%(levelname)s\t%(message)s')
    logging.basicConfig(level=log_level, format='  %(name)s\t%(levelname)s\t%(message)s')
    # logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

    base_name = os.path.basename(args[0])
    filename = os.path.abspath(args[0])
    path = filename.replace(base_name, "")
    module = base_name.replace(".py", "")
    ini = __import__(options.inputs)
    query = options.query
    engine = ExplorationEngine(path, filename, module, options.entry, ini.INI_ARGS, query)

    engine.explore()
    

if __name__ == '__main__':
    main()
