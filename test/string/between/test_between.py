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

    def remove():
        for kind in THE_DATAS_FOR_TESTING:
            THE_DATAS_FOR_TESTING[kind].remove()

    request.addfinalizer(remove)


# ---------------- #
# -- GOOD INPUT -- #
# ---------------- #

def test_string_use_between_good(or_datas):
    tests = THE_DATAS_FOR_TESTING['good'].flatdict(nosep = True)

    for name, datas in tests.items():
        text  = datas['text']
        start = datas['start']
        end   = datas['end']

        before  = datas['before'].replace(':space:', ' ')
        between = datas['between'].replace(':space:', ' ')
        after   = datas['after'].replace(':space:', ' ')

        before_found, between_found, after_found = BETWEEN_FUNCTION(
            text  = text,
            seps = [start, end]
        )

        assert before == before_found
        assert between == between_found
        assert after == after_found


# --------------- #
# -- BAD INPUT -- #
# --------------- #

def test_string_use_between_bad(or_datas):
    tests = THE_DATAS_FOR_TESTING['bad'].flatdict(nosep = True)

    for name, datas in tests.items():
        start = datas['start']
        end   = datas['end']

        with raises(ValueError):
            BETWEEN_FUNCTION(
                text = "",
                seps = [start, end]
            )
