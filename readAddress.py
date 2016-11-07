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

# MAIN

# read the configuration file, wherin paths, data
# structures and keys of the yaml input are defined.
with open(cfgfile) as f:
        code = compile(f.read(), cfgfile, 'exec')
        exec(code)


# get commandline argument
for idx, arg in enumerate(sys.argv[1:]):
    if idx == 0:
        handle = arg
    if idx == 1:
        eprint("Only the first argument is considered. "
             + "Here I dump the rest. "
             + "After that I shall exit disgracefully."
             )
    if idx >= 1:
        eprint(arg + "\n")

# Do exit disgracefully.
if 'idx' not in locals():
    eprint("An argument is required, "
          + "it should specify the handle of "
          + " the address entry.")
    eprint("Oh dear, is this the end? Yes, indeed.")
    exit(5)

if idx > 0:
    eprint("I told you so!")
    exit(1)


# check for and strip extensions
if yamlExtension in handle:
    eprint("Please avoid extensions ("
          + yamlExtension
          + ") in the handle. "
          + "I shall proceed to strip it now."
         )
    handle = handle.strip(yamlExtension)

# some chars must not be in a valid handle
forbidden = ['/','\\','*']
for c in forbidden:
    if c in handle:
        eprint("This character cannot be in "
              + "a valid handle: "
              + c
              + "\nAlas, how far I came, "
              + "yet I must perish."
             )
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
