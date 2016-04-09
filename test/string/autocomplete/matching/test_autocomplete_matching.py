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

CLASS_AUTO_COMPLETE = string_use.AutoComplete


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'autocomplete_matching.txt',
    mode    = {"verbatim" : ":default:"}
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove():
        THE_DATAS_FOR_TESTING.remove()

    request.addfinalizer(remove)


# ---------------- #
# -- GOOD INPUT -- #
# ---------------- #

def test_string_use_autocomplete_matching(or_datas):
    tests = THE_DATAS_FOR_TESTING.recudict(nosep = True)

    userwords = [
        x.strip(" ")
        for l in tests['words_to_find']
        for x in l.split()
    ]

    del tests['words_to_find']

    for prefix, matching in tests.items():
        if prefix == "empty_prefix":
            prefix = ""

        matching_expected = [
            x.strip(" ")
            for l in matching
            for x in l.split()
        ]

        matching_found = CLASS_AUTO_COMPLETE(
            words   = userwords,
            minsize = 0
        ).matching(prefix)

        assert matching_expected == matching_found
