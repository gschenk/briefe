# This script expects an address handle as an argument
# this handle corresponds to the file names of the
# address entries without extension.

from yaml import load, YAMLError
import sys

# path to the configuration file
cfgfile = 'address.cfg'

# temporary asgt
handle = 'test_test'


def get_path_filename(handle):
    """ cleans path, combines it"""
    path = yamlPath.strip('/').strip()
    return path + '/' + handle + yamlExtension


def eprint(argument):
    """ print to stderr """
    sys.stderr.write(argument)


def strip_extension(handle):
    """ remove extension if one is there """
    ext = config['extension']
    if ext in handle:
        eprint("Please avoid extensions ("
               + ext
               + ") in the handle. "
               + "I shall proceed to strip it now.")
        return handle.strip(ext)
    else:
        return handle


def check_if_valid(s):
    """ warn and return false if handle is invalid """
    forbidden = r"@%?\/*"
    for c in s:
        if c in forbidden:
            eprint("The characters (" + forbidden
                   + ") cannot be in a valid string: "
                   + c + " in " + s
                   + "\nAlas, how far I came, "
                   + "yet I must perish.")
            return False
    return True


# MAIN

# read the configuration file, wherin paths, data
# structures and keys of the yaml input are defined.
# the configuration file is also in yaml format
with open(cfgfile) as f:
        config = load(f)

yamlExtension = config['extension']
yamlPath = config['path']

try:
    handle = (sys.argv[1])
except:
    eprint("An argument is required, "
           + "it should specify the handle of "
           + " the address entry.")
    eprint("\nOh dear, is this the end? Yes, indeed.")
    exit(4)

if len(sys.argv) > 2:
    eprint("Only the first argument is considered. "
           + "Here I dump the rest:"
           + str(sys.argv[2:])
           + "\nAfter that I shall exit disgracefully.")
    exit(2)


# check for and strip extensions
handle = strip_extension(handle)

# some chars must not be in a valid handle
if not check_if_valid(handle):
    exit(2)

# read address entries from yaml
infile = get_path_filename(handle)
with open(infile, 'r') as fp:
    try:
        entries = load(fp)
    except YAMLError as exc:
        eprint(exc)
        exit(3)


# what follows is only an example, print to stdout
for key, val in dict.items(entries):
    if key != 'theAddress':
        print(key, val)

for key, val in dict.items(entries["theAddress"]):
    print(key, val)
