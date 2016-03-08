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

THIS_DIR = latex_use.PPath(__file__).parent


# --------------- #
# -- COMPILING -- #
# --------------- #

def test_latex_use_simple_compilation():
    latex_use.clean(ppath = THIS_DIR)

    latexobj = latex_use.Build(
        ppath      = THIS_DIR / 'minimal.tex',
        showoutput = False
    )
    latexobj.pdf()

    latex_use.clean(ppath = THIS_DIR)
