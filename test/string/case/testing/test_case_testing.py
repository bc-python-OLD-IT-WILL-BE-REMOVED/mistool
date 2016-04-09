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

    def remove():
        for kind in THE_DATAS_FOR_TESTING:
            THE_DATAS_FOR_TESTING[kind].remove()

    request.addfinalizer(remove)


# ------------------- #
# -- CASE VARIANTS -- #
# ------------------- #

def test_string_use_case_testing(or_datas):
    for kind, tests in THE_DATAS_FOR_TESTING.items():
        tests  = tests.flatdict(nosep = True)
        answer = (kind == 'good')

        for case, texts in tests.items():
            for onetext in texts:
                answer_found = CASE_TESTING_FUNCTION(
                    text = onetext,
                    kind = case
                )

        assert answer == answer_found
