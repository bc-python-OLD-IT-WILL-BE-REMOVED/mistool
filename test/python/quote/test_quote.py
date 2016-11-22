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

    def remove_extras():
        THE_DATAS_FOR_TESTING.remove_extras()

    request.addfinalizer(remove_extras)


# ------------- #
# -- QUOTING -- #
# ------------- #

def test_python_use_quote(or_datas):
    tests = THE_DATAS_FOR_TESTING.treedict

    for testname, infos in tests.items():
        text = infos['text']['value']

        quoted_wanted = infos['quoted']['value']

        quoted_found = QUOTE_FUNCTION(text)

        assert quoted_wanted == quoted_found
