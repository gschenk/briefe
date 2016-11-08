# This script expects an address handle as an argument
# this handle corresponds to the file names of the
# address entries without extension.

from yaml import load, YAMLError
import sys

# path to the configuration file
cfgfile = 'address.cfg'


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
                 + var + "}{%\n    " + arg
                 + "%\n    }")

    return texstring


def renewcommand(cmd, arg):
    # a latex macro containing arg
    texstring = (r"\renewcommand{"
                 + cmd + "}[0]{%\n    "
                 + arg + "%\n    }")
    return texstring


def company(adict):
    key = "companyName"
    if key in adict:
        return r"\\" + "%\n    " + adict[key]
    else:
        return ""


def get_entry(key, adict):
    if key in adict:
        return adict[key]
    else:
        return ""


def get_country(adict):
    key = "country"
    if key in adict:
        return r"\\" + "%\n    " + adict[key]
    else:
        return ""


def degrees(adict):
    if "academicDegrees" in adict:
        degree = adict["academicDegrees"]
        # which might need some formatting
        if degree[-2:] == 'Dr':
            degree = degree + '.'
        if degree.endswith('.'):
            degree = degree + ' '
        # spaces in TeX need protection
        # after an abbr. point
        return degree.replace(". ", r".\ ")
    else:
        return ""


def degree_in_salut(adict):
    key = "academicDegreeInSalutation"
    if key in adict:
        degree = adict[key] + " %\n    "
        if degree.endswith('.'):
            degree = degree + r'\ '
    elif degrees(adict):
        degree = degrees(adict)
    else:
        degree = ""
    return degree


def style_in_salut(adict):
    # check if there is a salutation and return it
    if "styleInSalutation" in adict:
        return adict["styleInSalutation"]
    else:
        return ""


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


def strip_comments(handle):
    trans_tab = dict.fromkeys(
        map(ord, r"% "), None)
    return handle.translate(trans_tab)



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
    sys.argv[1]
except:
    eprint("An argument is required, "
           + "it should specify the handle of "
           + " the address entry.")
    eprint("\nOh dear, is this the end? Yes, indeed.")
    exit(4)

# join all arguments to a single string
handle = "".join(sys.argv[1:])

# check for and strip extensions
handle = strip_extension(handle)

# strip laTeX commments and whitespace, anywhere in str
handle = strip_comments(handle)

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
    toname = (toname
              + style_in_salut(entries["theAddress"])
              + r"\\" + "%\n    ")
    # and all academic degrees Dr and up
    toname = toname + degrees(entries["theAddress"])

# these strings are often used, variables:
f_name = entries["familyName"]
g_name = entries["givenName"]

# correct name order in Chinese
if is_chinese:
    toname = toname + f_name + " " + g_name
else:
    toname = toname + g_name + " " + f_name

# append the company
toname = toname + company(entries["theAddress"])
# often the company ought to go before the name,
# the user may change this in the actual tex output


# the postal address: toaddress

def germanaddress(adict):
    """ put together an address using german style """
    return (get_entry("street", adict) + " "
            + get_entry("houseNumber", adict)
            + r"\\" + "%\n    "
            + get_entry("postalCode", adict)
            + " "
            + get_entry("city", adict)
            + get_country(adict)
            )

if is_german:
    toaddress = germanaddress(entries["theAddress"])
else:
    toaddress = germanaddress(entries["theAddress"])
    eprint("Only German address conventions have been implemented yet.")


# print to stdout latex statements to assign string
for thevar in [toname, toaddress]:
    print(setkomavar('toname', thevar))


# creating the automatic salutation line
if is_german:
    style = style_in_salut(entries["theAddress"])
    if style:
        # the it is a real person
        if style == "Herr":
            salutation = "Sehr geehrter Herr "
        elif style == "Frau":
            salutation = "Sehr geehrte Frau "
        else:
            salutation = ""
    else:
        salutation = ""

    if salutation:
        salutation = (salutation
                      + degree_in_salut(entries["theAddress"])
                      + f_name
                      )
    else:
        salutation = "Sehr geehrte Damen und Herren"

# print the latex statement
print(renewcommand(r"\autosalutation", salutation))
