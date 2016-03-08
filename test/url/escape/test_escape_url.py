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

from mistool import url_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = Path(__file__).parent

ESCAPE_FUNCTION = url_use.escape


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'escape_url.txt',
    mode    = {"keyval:: =": ":default:"}
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove():
        THE_DATAS_FOR_TESTING.remove()

    request.addfinalizer(remove)


# --------------------- #
# -- ESCAPING IN URL -- #
# --------------------- #

def test_url_use_escape(or_datas):
    tests = THE_DATAS_FOR_TESTING.dico(
        nosep    = True,
        nonbline = True
    )

    for name, datas in tests.items():
        url    = datas['url']
        escape = datas['escape']

        escape_found = ESCAPE_FUNCTION(url)

        assert escape == escape_found
