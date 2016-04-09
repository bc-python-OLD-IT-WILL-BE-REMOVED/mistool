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

CLASS_MULTI_SPLIT = string_use.MultiSplit


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'multisplit_listview.txt',
    mode = {
        'container' : ":default:",
        'verbatim'  : ["text", "seps", "escape", "listview"]
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

def test_string_use_multisplit_listview(or_datas):
    tests = THE_DATAS_FOR_TESTING.recudict(nosep = True)

    for name, datas in tests.items():
        text = datas['text'][0]
        seps = eval(datas['seps'][0])

        escape = datas.get('escape', [''])
        escape = escape[0]

        listview = eval(" ".join(datas['listview']))

        msplit = CLASS_MULTI_SPLIT(
            seps     = seps,
            esc_char = escape,
            strip    = True
        )

        listview_found = msplit(text)

        assert listview == listview_found
