#!/usr/bin/python

import sys
import getopt
import re
import shutil
import tempfile


# Perform the pure-Python equivalent of in-place `sed` substitution: e.g.,
# `sed -i -e 's/'${pattern}'/'${repl}' "${filename}"`.
def sed_inplace(patterns, replacements, filename):
    # For portability, NamedTemporaryFile() defaults to mode "w+b" (i.e., binary
    # writing with updating). This is usually a good thing. In this case,
    # however, binary writing imposes non-trivial encoding constraints trivially
    # resolved by switching to text writing. Let's do that.
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
        with open(filename) as src_file:
            content = src_file.read()
            for pattern_index in range(len(patterns)):
                # For efficiency, precompile the passed regular expression.
                pattern_compiled = re.compile(patterns[pattern_index])
                if pattern_compiled.flags & re.M:
                    content = pattern_compiled.sub(
                        replacements[pattern_index], content)
                else:
                    lines = content.splitlines()
                    for line_index in range(len(lines)):
                        lines[line_index] = pattern_compiled.sub(
                            replacements[pattern_index], lines[line_index])
                    content = ''.join(lines)
            tmp_file.write(content)
    # Overwrite the original file with the munged temporary file in a
    # manner preserving file attributes (e.g., permissions).
    shutil.copystat(filename, tmp_file.name)
    shutil.move(tmp_file.name, filename)


def usage():
    print('sed_inplace.py -p <pattern> -r <replacement> -f <file>')
    print('sed_inplace.py --patern <pattern> --replacement <replacement> --file <file>')
    print('sed_inplace.py -p <pattern1> -r <replacement1> -p <pattern2> -r <replacement2> -f <file>')
    print('sed_inplace.py --patern <pattern1> --replacement <replacement1> --patern <pattern2> --replacement <replacement2> --file <file>')
    sys.exit(2)


def main(argv):
    patterns = []
    replacements = []
    input_file = ''
    try:
        opts, prog_argv = getopt.getopt(
            argv, "p:r:i:", ["pattern=", "replacement=", "inputfile="])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt in ("-p", "--pattern"):
            patterns.append(arg)
        elif opt in ("-r", "--replacement"):
            replacements.append(arg)
        elif opt in ("-i", "--inputfile"):
            input_file = arg
    patterns_len = len(patterns)
    replacements_len = len(replacements)
    if patterns_len < 1 or replacements_len < 1 or patterns_len != replacements_len or not input_file:
        usage()
    sed_inplace(patterns, replacements, input_file)


if __name__ == "__main__":
    main(sys.argv[1:])
