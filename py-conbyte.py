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
    usage = "usage: %prog [options] <path to (target).py file>"
    parser = OptionParser(usage=usage)

    # Setup
    setup_group = OptionGroup(parser, "Exploration Setup")
    setup_group.add_option("-i", "--input", dest="inputs", action="store", help="Specify initial inputs, default to \'inputs\'", default="inputs")
    setup_group.add_option("-e", "--entry", dest="entry", action="store", help="Specify entry point, if different than (target).py", default=None)
    setup_group.add_option("-m", "--max_iter", dest="iteration", action="store", help="Specify max iterations", default=None)
    setup_group.add_option("-t", "--timeout", dest="timeout", action="store", help="Specify solver timeout", default=None)
    parser.add_option_group(setup_group)

    # Logging configuration
    logging_group = OptionGroup(parser, "Logging Configuration")
    logging_group.add_option("-d", "--debug", dest='debug', action="store_true", help="Enable debugging log")
    logging_group.add_option("-q", "--query", dest='query', action="store", help="Store smt queries", default=None)
    logging_group.add_option("-l", "--logfile", dest='logfile', action="store", help="Store log", default=None)

    parser.add_option_group(logging_group)
    (options, args) = parser.parse_args()
    if len(args) == 0 or not os.path.exists(args[0]):
        parser.error("Missing app to execute")
        sys.exit(1)

    if options.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logfile = options.logfile
    if logfile is not None:
        logging.basicConfig(filename=options.logfile, level=log_level, 
                            format='%(asctime)s  %(name)s\t%(levelname)s\t%(message)s', 
                            datefmt = '%m/%d/%Y %I:%M:%S %p')
    else:
        logging.basicConfig(filename=options.logfile, level=log_level, 
                            format='  %(name)s\t%(levelname)s\t%(message)s')

    base_name = os.path.basename(args[0])
    filename = os.path.abspath(args[0])
    path = filename.replace(base_name, "")
    module = base_name.replace(".py", "")
    ini = __import__(options.inputs)
    query = options.query
    engine = ExplorationEngine(path, filename, module, options.entry, ini.INI_ARGS, query)

    engine.explore(options.iteration, options.timeout)

    print()
    print("Results")
    for inputs in engine.input_sets:
        print(inputs)
    

if __name__ == '__main__':
    main()
