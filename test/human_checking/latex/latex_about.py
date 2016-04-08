#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from pathlib import Path


# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from mistool import latex_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

LOG_FILE = Path(__file__).parent / "latex_about.txt"


# ---------------------------------------- #
# -- INFOS ABOUT THE LATEX DISTRIBUTION -- #
# ---------------------------------------- #

infos_found = []

for kind, info in latex_use.about().items():
    infos_found.append(
        "{0}\n\t--> {1}\n".format(kind, info)
    )

infos_found = '\n'.join(infos_found)

with LOG_FILE.open(
    mode     = "w",
    encoding = "utf-8"
) as f:
    f.write(infos_found)
