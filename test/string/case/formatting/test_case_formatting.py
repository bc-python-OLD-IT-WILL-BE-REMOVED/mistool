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

CASE_FORMATTING_FUNCTION = string_use.case


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'case_formatting.txt',
    mode    = {"keyval:: =": ":default:"}
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove():
        THE_DATAS_FOR_TESTING.remove()

    request.addfinalizer(remove)


# ------------------- #
# -- CASE VARIANTS -- #
# ------------------- #

def test_string_use_case_formatting(or_datas):
    tests = THE_DATAS_FOR_TESTING.flatdict(nosep = True)

    for name, datas in tests.items():
        text   = datas['text']
        kind   = datas['kind']
        output = datas['output']

        output_found = CASE_FORMATTING_FUNCTION(
            text = text,
            kind = kind
        )

        assert output == output_found
