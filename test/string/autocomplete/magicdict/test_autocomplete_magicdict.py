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

    def remove_extras():
        THE_DATAS_FOR_TESTING.remove_extras()

    request.addfinalizer(remove_extras)


# ---------------- #
# -- GOOD INPUT -- #
# ---------------- #

def test_string_use_autocomplete_magicdict(or_datas):
    infos = THE_DATAS_FOR_TESTING.treedict

    userwords = [
        x.strip()
        for _, l in infos['words']
        for x in l.split(" ")
    ]

    infos = infos['magicdict']

    magicdict_words_wanted = [
        l for _, l in infos['words']
    ]

    magicdict_prefixes_wanted = {
        k: eval(v['value'])
        for k, v in infos['prefixes'].items()
    }

    magicdict_wanted = {
        'words'   : magicdict_words_wanted,
        'prefixes': magicdict_prefixes_wanted
    }

    magicdict_found = AUTO_COMPLETE(words = userwords).assos

    assert magicdict_wanted == magicdict_found
