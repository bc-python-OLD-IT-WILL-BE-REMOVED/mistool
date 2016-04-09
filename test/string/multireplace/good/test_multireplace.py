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

CLASS_MULTI_REPLACE = string_use.MultiReplace


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'multireplace.txt',
    mode = {
        'container' : ":default:",
        'verbatim'  : ["pattern", "before", "after"],
        'keyval:: =': "oldnew"
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

def test_string_use_multireplace(or_datas):
    tests = THE_DATAS_FOR_TESTING.recudict(nosep = True)

    for name, datas in tests.items():
        oldnew  = datas['oldnew']
        pattern = datas['pattern'][0].strip()

        before = "\n".join(datas['before'])
        before = before.strip()

        after = "\n".join(datas['after'])
        after = after.strip()

        mreplace = CLASS_MULTI_REPLACE(
            oldnew  = oldnew,
            pattern = PATTERNS_WORDS[pattern]
        )

        after_found = mreplace(before)

        assert after == after_found
