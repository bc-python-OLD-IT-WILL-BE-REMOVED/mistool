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

ASCII_FUNCTION = string_use.ascii_it

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

    def remove():
        for kind in THE_DATAS_FOR_TESTING:
            THE_DATAS_FOR_TESTING[kind].remove()

    request.addfinalizer(remove)


# ---------------------------- #
# -- GOOD ASCII TRANSLATION -- #
# ---------------------------- #

def test_string_use_ascii_good(or_datas):
    tests = THE_DATAS_FOR_TESTING['good'].flatdict(nosep = True)

    for name, datas in tests.items():
        dirty  = datas['dirty']
        pretty = datas['pretty']

        pretty_found = ASCII_FUNCTION(text = dirty)

        assert pretty == pretty_found


# --------------------------- #
# -- BAD ASCII TRANSLATION -- #
# --------------------------- #

def test_string_use_ascii_bad(or_datas):
    tests = THE_DATAS_FOR_TESTING['bad'].flatdict(nosep = True)

    for name, datas in tests.items():
        text = datas['text']

        with raises(ValueError):
            ASCII_FUNCTION(text = text)
