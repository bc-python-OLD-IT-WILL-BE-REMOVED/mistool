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
from mistool.config.pattern import PATTERNS_WORDS

# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = Path(__file__).parent

JOIN_AND_FUNCTION = string_use.joinand


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #



THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'joinand.txt',
    mode    = {"keyval:: =": ":default:"}
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove():
        THE_DATAS_FOR_TESTING.remove()

    request.addfinalizer(remove)


# ---------------------- #
# -- JOIN USING "AND" -- #
# ---------------------- #

def test_string_use_joinand(or_datas):
    tests = THE_DATAS_FOR_TESTING.flatdict(nosep = True)

    for name, datas in tests.items():
        thelist = [x.strip() for x in datas['list'].split(',')]
        text    = datas['text']
        andtext = datas['andtext']

        text_found = JOIN_AND_FUNCTION(
            texts   = thelist,
            andtext = andtext
        )

        assert text == text_found
