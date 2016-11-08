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


# some functions for writing the latex output
def setkomavar(var, arg):
    # a latex KOMA class way to assign variables
    texstring = (r"\setkomavar{"
                 + var + r"}{" + arg + r"}"
                )

    return texstring


def newcommand(cmd, arg):
    # a latex macro containing arg
    texstring = (r"\newcommand{"
                 + cmd + r"}[0]{" + arg + "}"
                )
    return texstring


def no_white_trail(thedict):
    # removes trailing whitespace from dict values
    for key, val in dict.items(thedict):
        if isinstance(val, str) and val.endswith(' '):
            thedict[key] = val.strip()


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
forbidden = ['/', '\\', '*']
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

# remove trailing whitespace
# apparently not needed, yaml takes care of it
#no_white_trail(entries)
#no_white_trail(entries["theAddress"])

# the script needs to learn whether German,
# English, or another language is used
# at this has to be added.
# as a placeholder it checks the language
# tag in the address file, assuming one
# would be written to in their native language


if entries["nameLanguage"] == "de":
    is_german = True
else:
    is_german = False

if entries["nameLanguage"] == "cn":
    is_chinese = True
else:
    is_chinese = False


# komavar toname, complete name of addresse

toname = ""
if is_german:
    # the name needs to contain the 'Anrede'
    if "styleInSalutation" in entries["theAddress"]:
        toname = ( toname +
            entries["theAddress"]["styleInSalutation"]
            + r"\\"
            )
    # and some academic degrees
    if "academicDegrees" in entries["theAddress"]:
        degree = entries["theAddress"]["academicDegrees"]
        # which might need some formatting
        if degree[-2:] == 'Dr':
            degree = degree + '.'
        if degree.endswith('.'):
            degree = degree + ' '
        degree = degree.replace(". ",r".\ ")

        # but is eventually added
        toname = toname + degree

# at last something that applies always, the name
if is_chinese:
    toname = (toname
              + entries["familyName"]
              + " "
              + entries["givenName"]
             )
else:
    toname = (toname
              + entries["givenName"]
              + " "
              + entries["familyName"]
             )
#entries["theAddress"]["givenName"]
#entries["theAddress"]["familyName"]

# if the addresse is an actual person

print(setkomavar('toname', toname))
