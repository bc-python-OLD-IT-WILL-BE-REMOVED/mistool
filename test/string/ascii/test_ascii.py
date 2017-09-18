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


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = Path(__file__).parent

ASCII_FUNCTION = string_use.asciify

STRING_USE_ERROR = ValueError


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = {}

for kind in ["good", "bad"]:
    THE_DATAS_FOR_TESTING[kind] = READ(
        content = THIS_DIR / 'ascii_{0}.txt'.format(kind),
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


# ---------------------------- #
# -- GOOD ASCII TRANSLATION -- #
# ---------------------------- #

def test_string_use_ascii_good(or_datas):
    tests = THE_DATAS_FOR_TESTING['good'].mydict("std nosep nonb")

    for testname, infos in tests.items():
        dirty = infos['dirty']

        pretty_wanted = infos['pretty']

        pretty_found = ASCII_FUNCTION(text = dirty)

        assert pretty_wanted == pretty_found


# --------------------------- #
# -- BAD ASCII TRANSLATION -- #
# --------------------------- #

def test_string_use_ascii_bad(or_datas):
    tests = THE_DATAS_FOR_TESTING['bad'].mydict("std nosep nonb")

    for testname, infos in tests.items():
        text = infos['text']

        with raises(ValueError):
            ASCII_FUNCTION(text = text)
