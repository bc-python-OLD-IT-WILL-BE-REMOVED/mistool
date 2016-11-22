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
    content = THIS_DIR / 'multireplace_cycle_problem.txt',
    mode = {
        'container' : ":default:",
        'verbatim'  : "pattern",
        'keyval:: =': "oldnew"
    }
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove_extras():
        THE_DATAS_FOR_TESTING.remove_extras()

    request.addfinalizer(remove_extras)


# --------------- #
# -- REPLACING -- #
# --------------- #

def test_string_use_multireplace_cycle_problem(or_datas):
    tests = THE_DATAS_FOR_TESTING.treedict

    for testname, infos in tests.items():
        oldnew = {
            k: v['value']
            for k, v in infos['oldnew'].items()
        }

        _, pattern = infos['pattern'][0]
        pattern    = pattern.strip()

        with raises(ValueError):
            multireplace = CLASS_MULTI_REPLACE(
                oldnew    = oldnew,
                pattern   = PATTERNS_WORDS[pattern],
                recursive = True
            )

            multireplace.build()
