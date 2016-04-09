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

AUTO_COMPLETE = string_use.AutoComplete


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'autocomplete_magicdict.txt',
    mode    = {
        "container" : "magicdict",
        "keyval:: =": "prefixes",
        "verbatim"  : "words"
    }
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

def test_string_use_autocomplete_magicdict(or_datas):
    tests = THE_DATAS_FOR_TESTING.recudict(nosep = True)

    userwords = [x.strip(" ") for l in tests['words'] for x in l.split()]

    magicdict_expected = tests['magicdict']

    shortlist_words = [
        x.strip(" ")
        for l in magicdict_expected['words']
        for x in l.split()
    ]

    prefixes = {
        k: eval(v)
        for k, v in magicdict_expected['prefixes'].items()
    }

    magicdict_expected = {
        'words'   : shortlist_words,
        'prefixes': prefixes
    }

    magicdict_found = AUTO_COMPLETE(words = userwords).assos

    assert magicdict_expected == magicdict_found
