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

CLASS_MULTI_SPLIT = string_use.MultiSplit


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'multisplit_iterator.txt',
    mode = {
        'container' : ":default:",
        'verbatim'  : ["text", "seps", "listiter"]
    }
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove():
        THE_DATAS_FOR_TESTING.remove()

    request.addfinalizer(remove)


# --------------- #
# -- REPLACING -- #
# --------------- #

def test_string_use_multisplit_iterator(or_datas):
    tests = THE_DATAS_FOR_TESTING.recudict(nosep = True)

    for name, datas in tests.items():
        text = datas['text'][0]
        seps = eval(datas['seps'][0])

        listiter = [eval("(" + x + ")") for x in datas['listiter']]

        msplit = CLASS_MULTI_SPLIT(
            seps  = seps,
            strip = True
        )

        listview = msplit(text)

        listiter_found = [(x.type, x.val) for x in msplit.iter()]

        assert listiter == listiter_found
