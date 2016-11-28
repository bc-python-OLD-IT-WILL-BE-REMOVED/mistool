#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from pathlib import Path
from pytest import fixture, raises

from orpyste.data import ReadBlock as READ


# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from mistool import string_use
from mistool.config.pattern import PATTERNS_WORDS

# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = Path(__file__).parent

BETWEEN_FUNCTION = string_use.between


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = {}

for kind in ["good", "bad"]:
    THE_DATAS_FOR_TESTING[kind] = READ(
        content = THIS_DIR / 'between_{0}.txt'.format(kind),
        mode    = {"keyval:: =": ":default:"}
    )

@fixture(scope="module")
def or_datas(request):
    for kind in THE_DATAS_FOR_TESTING:
        THE_DATAS_FOR_TESTING[kind].build()

    def remove_extras():
        for kind in THE_DATAS_FOR_TESTING:
            THE_DATAS_FOR_TESTING[kind].remove_extras()

    request.addfinalizer(remove_extras)


# ---------------- #
# -- GOOD INPUT -- #
# ---------------- #

def test_string_use_between_good(or_datas):
    tests = THE_DATAS_FOR_TESTING['good'].mydict("std nosep nonb")

    for testname, infos in tests.items():
        text  = infos['text']
        start = infos['start']
        end   = infos['end']

        before_wanted = infos['before']
        before_wanted = before_wanted.replace(':space:', ' ')

        between_wanted = infos['between']
        between_wanted = between_wanted.replace(':space:', ' ')

        after_wanted = infos['after']
        after_wanted = after_wanted.replace(':space:', ' ')

        before_found, between_found, after_found = BETWEEN_FUNCTION(
            text  = text,
            seps = [start, end]
        )

        assert before_wanted == before_found
        assert between_wanted == between_found
        assert after_wanted == after_found


# --------------- #
# -- BAD INPUT -- #
# --------------- #

def test_string_use_between_bad(or_datas):
    tests = THE_DATAS_FOR_TESTING['bad'].mydict("std nosep nonb")

    for testname, infos in tests.items():
        start = infos['start']
        end   = infos['end']

        with raises(ValueError):
            BETWEEN_FUNCTION(
                text = "",
                seps = [start, end]
            )
