import logging
import sys
import time
import os
from subprocess import Popen, PIPE, STDOUT
from hashlib import sha224
import subprocess
from string import Template

log = logging.getLogger("ct.z3_wrapper")

class Z3Wrapper(object):
    options = {"lan": "smt.string_solver=z3str3", "stdin": "-in"}
    cnt = 0

    def __init__(self, query_store):
        self.query = None
        self.asserts = None
        self.prefix = None
        self.ending = None
        self.variables = dict()
        self.query_store = query_store

    def set_variables(self, variables):
        self.varables = variables
        for v in variables:
            self.variables[v] = variables[v]


    def find_counter_example(self, asserts, query, timeout=None):
        start_time = time.process_time()
        if timeout is not None:
            self.options["timeout"] = "-T:" + str(timeout)
        else:
            self.options["timeout"] = "-T:15"
        self.asserts = asserts
        self.query = query
        result, model = self._find_model()
        endtime = time.process_time()
        solve_time = endtime - start_time
        return result, model

    def _find_model(self):
        z3_cmd = "z3"
        for option in self.options:
            z3_cmd = z3_cmd + " " + self.options[option]
        model = None

        formulas = self._build_expr()

        # log.debug("\n" + formulas)
        if self.query_store is not None:
            #smthash = sha224(bytes(str(self.query), 'UTF-8')).hexdigest()
            #filename = os.path.join(self.query_store, "{}.smt2".format(smthash))
            filename = os.path.join(self.query_store, "{}.smt2".format(self.cnt))
            with open(filename, 'w') as f:
                f.write(formulas)


        try:
            process = Popen(z3_cmd.split(" "), stdin=PIPE, stdout=PIPE, stderr=PIPE)
        except subprocess.CalledProcessError as e:
            print(e.output)

        stdout, stderr = process.communicate(input=formulas.encode())
        log.debug("\n" + stdout.decode())

        output = stdout.decode()

        if output is None or len(output) == 0:
            ret = "UNKNOWN"
        else:
            output = output.splitlines()
            while "error" in output[0]:
                output.pop(0)
            ret = output[0]
            if "unsat" in ret:
                ret = "UNSAT"
            elif "sat" in ret:
                ret = "SAT"
                model = self._get_model(output[1:])
            elif "timeout" in ret:
                ret = "TIMEOUT"
            else:
                ret = "UNKNOWN"

        log.info("%s smt, Result: %s" % (self.cnt, ret))
        self.cnt += 1
        return ret, model


    def _get_model(self, models):
        model = dict()
        for line in models:
            name, value = line.replace("((", "").replace("))", "").split(" ", 1)
            if self.variables[name] is "Int":
                if "(" in value:
                    value = value.replace("(", "").replace(")", "").split(" ")[1]
                    model[name] = -int(value)
                else:
                    model[name] = int(value)
            else:
                value = value.replace("\"", "", 1).replace("\"", "", -1)
                model[name] = value
        return model


    def _build_expr(self):
        f_template = Template("""
$declarevars

$query

(check-sat)

$getvars
""")
        assignments = dict()
        assignments['declarevars'] = "\n".join(
            "(declare-fun {} () {})".format(name, var) for name, var in self.variables.items())

        assignments['query'] = "\n".join(assertion.get_formula() for assertion in self.asserts)
        assignments['query'] += self.query.get_formula()

        assignments['getvars'] = "\n".join("(get-value ({}))".format(name) for name in self.variables)
        return f_template.substitute(assignments).strip()
