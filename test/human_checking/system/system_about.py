#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from pathlib import Path


# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from mistool import os_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

LOG_FILE = Path(__file__).parent / "system_about.txt"


# ---------------------------- #
# -- INFOS ABOUT THE SYSTEM -- #
# ---------------------------- #

infos_found = []

infos_found.append(
    "system\n\t--> {0}\n".format(os_use.system())
)

infos_found.append(
    "pathenv\n\t--> {0}\n".format(os_use.pathenv())
)

infos_found = '\n'.join(infos_found)

with LOG_FILE.open(
    mode     = "w",
    encoding = "utf-8"
) as f:
    f.write(infos_found)
