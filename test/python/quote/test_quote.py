#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from pathlib import Path
from pytest import fixture

from orpyste.data import ReadBlock as READ


# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from mistool import python_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = Path(__file__).parent

QUOTE_FUNCTION = python_use.quote


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'quote.txt',
    mode    = {"keyval:: =": ":default:"}
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove():
        THE_DATAS_FOR_TESTING.remove()

    request.addfinalizer(remove)


# ------------- #
# -- QUOTING -- #
# ------------- #

def test_python_use_quote(or_datas):
    tests = THE_DATAS_FOR_TESTING.dico(
        nosep    = True,
        nonbline = True
    )

    for name, datas in tests.items():
        text   = datas['text']
        quoted = datas['quoted']

        quoted_found = QUOTE_FUNCTION(text)

        assert quoted == quoted_found
