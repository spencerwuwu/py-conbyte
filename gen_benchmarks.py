#!/usr/bin/env python3.7

import sys
import os
from subprocess import Popen, PIPE, STDOUT

def main(target):
    pys = ["targets/leetcode_int/add_binary.py",
           "targets/leetcode_int/addStrings.py",
           "targets/leetcode_int/numDecodings.py",
           "targets/leetcode_int/restoreIpAddresses.py",
           "targets/leetcode_int/validIPAddress.py",
           "targets/leetcode_int/validWordAbbreviation.py",
           "targets/lib_int/datetime__parse_hh_mm_ss_ff.py",
           "targets/lib_int/datetime__parse_isoformat_date.py",
           "targets/lib_int/distutils_get_build_version.py",
           "targets/lib_int/email__parsedate_tz.py",
           "targets/lib_int/http_parse_request.py",
           "targets/lib_int/nntplib__parse_datetime.py",
           "targets/lib_int/smtpd_parseargs.py",
           "targets/lib_int/wsgiref_check_status.py"]

    inputs = ["[\"1001\", \"111\"]",
              "[\"14950\", \"385769\"]",
              "[\"215381249207226\"]",
              "[\"25525511135\"]",
              "[\"172.16.254.1\"]",
              "[\"internationalization\", \"i12iz4n\"]",
              "[\"12:01:23.123456\"]",
              "[\"2019-07-19\"]",
              "[\"MSC v.1912 abc\"]",
              "[\"Mon, 16 Nov 2009 13:32:02 +0100\"]",
              "[\"HTTP/1.0\"]",
              "[\"20190723121212\"]",
              "[\"localhost:8025\", \"localhost:25\"]",
              "[\"200 ok\"]"
             ]
    index = 0
    for py in pys:
        b_path = "benchmarks/py-conbyte_%s/%s" % (target, py.replace("targets/", "").replace(".py", "").replace("/", "-"))
        os.system("mkdir -p %s" % b_path)
        cmd = "./py-conbyte.py --stdin -s %s -m 300 -t 3 -q %s " % (target, b_path)
        if "add_binary" in py:
            cmd += " --ss "
        cmd += py
        print(cmd)
        try:
            process = Popen(cmd, shell=True, stdin=PIPE)
        except subprocess.CalledProcessError as e:
            print(e.output)
        
        process.communicate(input=("INI_ARGS = %s" % inputs[index]).encode())
        index += 1





if __name__ == '__main__':
    main(sys.argv[1])
