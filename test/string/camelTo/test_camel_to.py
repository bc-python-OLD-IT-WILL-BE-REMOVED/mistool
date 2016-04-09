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

from mistool import string_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = Path(__file__).parent

CAMEL_TO_FUNCTION = string_use.camelto


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'camel_to.txt',
    mode    = {"keyval:: =": ":default:"}
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove():
        THE_DATAS_FOR_TESTING.remove()

    request.addfinalizer(remove)


# ---------------------------- #
# -- CAMEL TO CASE VARIANTS -- #
# ---------------------------- #

def test_string_use_camelto(or_datas):
    tests = THE_DATAS_FOR_TESTING.flatdict(nosep = True)

    for name, datas in tests.items():
        text   = datas['text']
        kind   = datas['kind']
        output = datas['output']

        output_found = CAMEL_TO_FUNCTION(
            text = text,
            kind = kind
        )

        assert output == output_found
