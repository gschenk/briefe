from yaml import dump, load
import os


# path to the configuration file
cfgfile = 'address.cfg'


def addr_lang(key):
    """querries for the language, taking posix strings"""
    known = ["de", "cn", "en"]
    line = ''
    while len(line) != 2:
        rawline = input(
            'please enter language '
            + str(known)
            + ': '
        )
        line = rawline.strip()
        if line not in known:
            line = ''
            print("Language key unknown.")
    return line


def addr_entry(key):
    """querries the user for address data, cleans it"""

    # getting the input
    rawline = input(
        'please enter ' + key + ': '
    )

    # get rid of trailing whitespace
    line = rawline.strip()

    # replace tabs
    line = line.replace('\t', ' ')

    # remove forbidden strings
    trans_tab = dict.fromkeys(
        map(ord, '\:.\"\'!@#$\\\/'), None
    )

    line = line.translate(trans_tab)

    if rawline != line:
        print(
            'Warning: string has been changed: \''
            + rawline
            + '\' to \''
            + line
            + '\'.'
        )
    return line


def get_handle():
    """offers a handle for an entry, checks if used"""

    trial = entries["familyName"] + '_' + entries["givenName"]
    if not check_handle(trial):
        if query_acceptance(trial):
            print("\n")
            return trial
    else:
        print("Handle already in use. You might want "
              + "to check if an entry for this person "
              + "already exists.")

    handle = input("No automatic handle was chosen"
                   + "try to write one yourself:"
                   )
    print("The entry will be stored at:"
          + get_path_filename(handle) + "\n")
    return handle


def query_acceptance(trial):
    """ ask the user if they accept the handle and filename"""
    ys = ['y', 'Y']
    ns = ['n', 'N']
    yns = ys + ns
    a = ''

    while a not in yns:
        a = input(
            "Would you like to use "
            + trial
            + " as handle (stored in: '"
            + get_path_filename(trial)
            + "' " + str(yns) + "? "
        )

    if a in ys:
        return True
    if a in ns:
        return False


def get_path_filename(handle):
    """ cleans path, combines it"""
    path = config['path'].strip('/').strip()
    return path + '/' + handle + config['extension']


def check_handle(handle):
    """checks if a filename is already in use"""
    return os.path.isfile(get_path_filename(handle))


# MAIN

# read the configuration file, wherin paths, data
# structures and keys for the yaml output are defined.

with open(cfgfile) as f:
        config = load(f)

entries = config['entries']


# get necessary entries
for key in dict.keys(entries):
    value = ''
    if key != 'nameLanguage' and key != 'theAddress':
        while not value:
            value = addr_entry(key)
        entries[key] = value

    if key == 'nameLanguage':
        entries[key] = addr_lang(key)


# find a file name
handle = get_handle()


# get the bulk of the data
empty_keys = []
for key in dict.keys(entries['theAddress']):
    entries['theAddress'][key] = addr_entry(key)

    # add empty entries on list to be removed
    if not entries['theAddress'][key]:
        empty_keys.append(key)

# remove empty keys from list
for key in empty_keys:
    del entries['theAddress'][key]

# output to yaml
outfile = get_path_filename(handle)
with open(outfile, 'w') as fp:
        dump(entries, fp, default_flow_style=False)
