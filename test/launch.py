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


# -------------------------------------- #
# -- LAUNCHING ALL THE BUILDING TOOLS -- #
# -------------------------------------- #

def printtile(text):
    print(
        "",
        withframe(text),
        "",
        sep = "\n"
    )

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


# ---------------------- #
# -- UPDATING THE LOG -- #
# ---------------------- #

printtile("Updating the log file...")

if tests_passed:
    ...


with LOG_FILE.open(
    mode     = 'w',
    encoding = 'utf-8'
) as f:
    f.write("OK")
