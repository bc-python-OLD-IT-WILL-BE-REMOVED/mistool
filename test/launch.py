#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

import platform

from mistool.os_use import (
    cd,
    PPath,
    runthis
)
from mistool.term_use import withframe


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = PPath(__file__).parent
LOG_FILE = THIS_DIR / "log.txt"


# --------------- #
# -- FUNCTIONS -- #
# --------------- #

def printtile(text):
    print(
        "",
        withframe(text),
        "",
        sep = "\n"
    )


# ----------------------------- #
# -- LAUNCHING ALL THE TESTS -- #
# ----------------------------- #

with cd(THIS_DIR):
    printtile("Launching all the tests...")

    try:
        tests_passed = True

        runthis(
            cmd        = "py.test -v --resultlog=x-pytest_log-x.txt",
            showoutput = True
        )

    except Exception as e:
        tests_passed = False


# ---------------------------------------- #
# -- LAUNCHING ALL THE "HUMAN CHECKING" -- #
# ---------------------------------------- #

printtile("Launching the scripts producing infos to be checked by a human...")

for onepath in THIS_DIR.walk("file::human_checking/**.py"):
    print('   + "{0}" executed.'.format(onepath.name))

    runthis(
        cmd        = 'python "{0}"'.format(onepath),
        showoutput = True
    )


# ---------------------- #
# -- UPDATING THE LOG -- #
# ---------------------- #

printtile("Updating the log file...")

if tests_passed:
    message = ["OK"]

else:
    message = ["PAS OK"]


message = "\n".join(message)
with LOG_FILE.open(
    mode     = 'w',
    encoding = 'utf-8'
) as f:
    f.write(message)
