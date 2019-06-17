# py-conbyte 

A Python concolic testing tool running on byte-code level.

This project is based on the structure purposed in
[A Peer Architecture for Lightweight Symbolic Execution](http://hoheinzollern.files.wordpress.com/2008/04/seer1.pdf)
and the tool [PyExZ3](https://github.com/GroundPound/PyExZ3).   
However, instead of overwriting the integer and string object, 
we trace the program to analysis on bytecode level and maintain an
independent stack with concolic states of variables.

With this approach, any objects will be disassembled into hierarchy
of basic elements including integer, string, arrays, and dictionaries,
which makes instrumenting rather simple.

py-conbyte currently supports:
- Builtin functions: 
  - `len()`
  - `int()`
  - `str()`
  - `dict()`
  - `list()`
  - `range()`
  - `sum()`
  - `max()`
  - `min()`
  - `abs()`
- Types: 
  - Integer
  - String
  - Array
  - Dictionary
  - Class containing these types
See `test/` for supported syntaxes.   

Formal parameters of the program to analysis can only integers
and strings for now.

## Usage
```
Usage: py-conbyte.py [options] <path to (target).py file>

Options:
  -h, --help            show this help message and exit

  Exploration Setup:
    -i INPUTS, --input=INPUTS
                        Specify initial inputs, default to 'inputs'
    -e ENTRY, --entry=ENTRY
                        Specify entry point, if different than (target).py
    -m ITERATION, --max_iter=ITERATION
                        Specify max iterations
    -t TIMEOUT, --timeout=TIMEOUT
                        Specify solver timeout

  Logging Configuration:
    -d, --debug         Enable debugging log
    -q QUERY, --query=QUERY
                        Store smt queries
    -l LOGFILE, --logfile=LOGFILE
                        Store log

  Solver Configuration:
    -s SOLVER_TYPE, --solver=SOLVER_TYPE
                        Solver=[z3, cvc4], default is z3

```

example:
```
 $ ./py-conbyte.py -i inputs test/do_numbers.py
```

