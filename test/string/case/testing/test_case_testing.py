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

CASE_TESTING_FUNCTION = string_use.iscase


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = {}

for kind in ["good", "bad"]:
    THE_DATAS_FOR_TESTING[kind] = READ(
        content = THIS_DIR / 'case_{0}.txt'.format(kind),
        mode    = {"verbatim": ":default:"}
    )

@fixture(scope="module")
def or_datas(request):
    for kind in THE_DATAS_FOR_TESTING:
        THE_DATAS_FOR_TESTING[kind].build()

    def remove_extras():
        for kind in THE_DATAS_FOR_TESTING:
            THE_DATAS_FOR_TESTING[kind].remove_extras()

    request.addfinalizer(remove_extras)


# ------------------- #
# -- CASE VARIANTS -- #
# ------------------- #

def test_string_use_case_testing(or_datas):
    for kind, tests in THE_DATAS_FOR_TESTING.items():
        tests  = tests.mydict("std nosep nonb")

        answer_wanted = (kind == 'good')

        for case, texts in tests.items():
            answer_found = CASE_TESTING_FUNCTION(
                text = texts[0],
                kind = case
            )

        assert answer_wanted == answer_found
