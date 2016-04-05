#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from pathlib import Path

from orpyste.data import ReadBlock


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR   = Path(__file__).parent
CONFIG_DIR = THIS_DIR / "config"

for parent in THIS_DIR.parents:
    if parent.name == "misTool":
        break

PY_FILE    = parent / 'mistool/config/latex.py'
FORUM_FILE = THIS_DIR / 'forum.txt'


# ----------- #
# -- TOOLS -- #
# ----------- #

def doubleslash(text):
    return text.replace("\\" ,"\\\\")


# ---------------- #
# -- EXTENSIONS -- #
# ---------------- #

data = ReadBlock(
    content = CONFIG_DIR / "extension.peuf",
    mode    = {
        'container': ":default:",
        'verbatim' : ["extension", "comment"]
    }
)

data.build()
dicoview = data.recudict(nosep = True)
data.remove()


onetab = ' '*4
twotab = onetab*2

TEXT_CLASS_EXT = [
"""
#!/usr/bin/env python3

from collections import OrderedDict

# Note: the following variables were automatically built.

TEMP_EXTS = OrderedDict([
""".strip()
]

TEXT_ALL_EXT = ['EXTS_TO_CLEAN = [']

TEXT_FORUM = []


for kind, spec in dicoview.items():
# The infos
    exts = " ".join(spec['extension'])

    if '¨' in exts:
        print(' '*9 + '+ TODO ---> {0}'.format(exts))
        continue

    comment = spec.get('comment', "")

# Text for Python code
    exts = [x.strip() for x in exts.split(',')]

    TEXT_CLASS_EXT.append(
        onetab + "('" + kind + "', " + str(exts) + '),'
    )

    TEXT_ALL_EXT.append('# ' + kind)

    if comment:
        TEXT_ALL_EXT += [
            '#',
            '# ' + '\n# '.join(comment)
        ]

    TEXT_ALL_EXT.append(onetab + str(exts)[1:-1] + ',')

# Text for terminal
    if TEXT_FORUM:
        TEXT_FORUM.append('')

    deco = "="*len(kind)

    TEXT_FORUM += [
        deco,
        kind,
        deco,
        '',
        onetab + '+ ' + str(sorted(exts))[1:-1].replace("'", "")
    ]

    if comment:
        TEXT_FORUM += [''] + comment

# No final coma...
TEXT_CLASS_EXT[-1] = TEXT_CLASS_EXT[-1][:-1]
TEXT_ALL_EXT[-1]   = TEXT_ALL_EXT[-1][:-1]

# List to text...
TEXT_FORUM  = '\n'.join(TEXT_FORUM)

PY_TEXT = TEXT_CLASS_EXT + ['])', ''] + TEXT_ALL_EXT + [']']


# ------------------ #
# -- TO ESCAPE IT -- #
# ------------------ #

data = ReadBlock(
    content = CONFIG_DIR / "escape.peuf",
    mode    = "verbatim"
)

data.build()
dicoview = data.recudict(nosep = True)
data.remove()


PY_TEXT += [
"""
# Sources :
#    * The page 7 in "The Comprehensive LATEX Symbol List" of Scott Pakin.
#    * http://www.grappa.univ-lille3.fr/FAQ-LaTeX/21.26.html

CHARS_TO_ESCAPE = {"""
]

charbykind = {
    'text': "",
    'math': ""
}

for kind, chars in dicoview.items():
    chars = ''.join(chars)
    chars = chars.replace(" ", "")

    for k in kind.split('_'):
        charbykind[k] += chars

PY_TEXT += [
"""    'text': "{0}",
    'math': "{1}" """.format(
        charbykind['text'],
        charbykind['math']
    ),
"""}

CHARS_TO_LATEXIFY = {"""
]

# ------ #

data = ReadBlock(
    content = CONFIG_DIR / "latexify.peuf",
    mode    = 'keyval:: ='
)

data.build()
dicoview = data.flatdict(nosep = True)
data.remove()


texifybykind = {
    'text': [],
    'math': []
}

for name, info in dicoview.items():
    ascii_ = doubleslash(info['ascii'])

    for kind in ['text', 'math']:
        texifybykind[kind].append(
            "'{0}': \"{1}\",".format(ascii_, doubleslash(info[kind]))
        )

for kind in ['text', 'math']:
    texifybykind[kind][-1] = texifybykind[kind][-1][:-1]

    PY_TEXT += [
        "    '" + kind + "': {",
        "        " + "\n        ".join(texifybykind[kind]),
        "    },"
    ]

PY_TEXT[-1] = PY_TEXT[-1][:-1]

PY_TEXT.append('}')
PY_TEXT = '\n'.join(PY_TEXT)


# ------------------------------- #
# -- UPDATE OF THE PYTHON FILE -- #
# ------------------------------- #

print('    * Updating the Python file')

with PY_FILE.open(encoding ="utf-8", mode = "w") as f:
    f.write(PY_TEXT)


# --------------------- #
# -- TEXT FOR FORUMS -- #
# --------------------- #

print('    * Updating the "Forum" file')

with FORUM_FILE.open(encoding ="utf-8", mode = "w") as f:
    f.write(TEXT_FORUM)
