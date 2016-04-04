#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from mistool.os_use import PPath, runthis, cd


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = PPath(__file__).parent


# -------------------------------------- #
# -- LAUNCHING ALL THE BUILDING TOOLS -- #
# -------------------------------------- #

with cd(THIS_DIR):
    print("+ Launching all the tests...")

    try:
        tests_passed = True

        runthis(
            cmd        = "py.test -v --resultlog=log.txt",
            showoutput = True
        )

    except Exception as e:
        tests_passed = False
