#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from pathlib import Path

from mistool.term_use import buildframe


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR   = Path(__file__).parent
CONFIG_DIR = THIS_DIR / "config"

for parent in THIS_DIR.parents:
    if parent.name == "misTool":
        break

PY_FILE = parent / 'mistool/config/frame.py'

PY_TEXT = [
    """
#!/usr/bin/env python3

# Note: the following ugly dictionary was automatically built.
    """.strip()
]


# ----------- #
# -- TOOLS -- #
# ----------- #

def pyrepr(onedict, name):
    lines = [name + " = {}"]

    for k in sorted(onedict.keys()):
        v = onedict[k]
        lines.append("{0}['{1}'] = {2}".format(name, k, repr(v)))

    return "\n".join(lines)


# -------------------- #
# -- DEFAULT FRAMES -- #
# -------------------- #

FRAMES = {}

for path in CONFIG_DIR.glob("*/*.txt"):
    lang  = path.parent.stem
    style = path.stem

    with path.open(
        mode     = "r",
        encoding = "utf-8"
    ) as f:
        FRAMES["{0}_{1}".format(lang, style)] = buildframe(f.read().rstrip())


PY_TEXT += [
    "",
    pyrepr(
        onedict = FRAMES,
        name    = "ALL_FRAMES"
    )
]


# ------------------------------- #
# -- UPDATE OF THE PYTHON FILE -- #
# ------------------------------- #

print('    * Update of the Python file')

PY_TEXT = "\n".join(PY_TEXT)

with PY_FILE.open(
    mode     = 'w',
    encoding = 'utf-8'
) as f:
    f.write(PY_TEXT)
