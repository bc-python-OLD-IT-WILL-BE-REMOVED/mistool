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
    content = THIS_DIR / 'escape.txt',
    mode    = {"keyval:: =": ":default:"}
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove_extras():
        THE_DATAS_FOR_TESTING.remove_extras()

    request.addfinalizer(remove_extras)


# --------------------- #
# -- ESCAPING IN URL -- #
# --------------------- #

def test_url_use_escape(or_datas):
    tests = THE_DATAS_FOR_TESTING.treedict

    for name, datas in tests.items():
        url    = datas['url']['value']
        escape = datas['escape']['value']

        escape_found = ESCAPE_FUNCTION(url)

        assert escape == escape_found
