#!/usr/bin/python

import sys
import getopt
import re
import shutil
import tempfile


# Perform the pure-Python equivalent of in-place `sed` substitution: e.g.,
# `sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.
def sed_inplace(pattern, repl, filename):
    # For efficiency, precompile the passed regular expression.
    pattern_compiled = re.compile(pattern)

    # For portability, NamedTemporaryFile() defaults to mode "w+b" (i.e., binary
    # writing with updating). This is usually a good thing. In this case,
    # however, binary writing imposes non-trivial encoding constraints trivially
    # resolved by switching to text writing. Let's do that.
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(filename) as src_file:
            if pattern_compiled.flags & re.M:
                content = src_file.read()
                tmp_file.write(pattern_compiled.sub(repl, content))
            else:
                for line in src_file:
                    tmp_file.write(pattern_compiled.sub(repl, line))

    # Overwrite the original file with the munged temporary file in a
    # manner preserving file attributes (e.g., permissions).
    shutil.copystat(filename, tmp_file.name)
    shutil.move(tmp_file.name, filename)


def main(argv):
    pattern = ''
    replacement = ''
    inputfile = ''
    try:
        opts, prog_argv = getopt.getopt(
            argv, "p:r:i:", ["pattern=", "replacement=", "inputfile="])
    except getopt.GetoptError:
        print('sed_inplace.py -p <pattern> -r <replacement> -f <file>')
        print('sed_inplace.py --patern <pattern> --replacement <replacement> --file <file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-p", "--pattern"):
            pattern = arg
        elif opt in ("-r", "--replacement"):
            replacement = arg
        elif opt in ("-i", "--inputfile"):
            inputfile = arg
    sed_inplace(pattern, replacement, inputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
