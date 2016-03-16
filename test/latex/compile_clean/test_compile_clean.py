#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from pathlib import Path
from mistool.os_use import cd


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

    tex_ppath = THIS_DIR / 'minimal.tex'
    pdf_ppath = tex_ppath.with_ext("pdf")

    if pdf_ppath.is_file():
        pdf_ppath.remove()

    latexobj = latex_use.Build(
        ppath      = tex_ppath,
        showoutput = False
    )

    latexobj.pdf()

    latex_use.clean(ppath = THIS_DIR)
