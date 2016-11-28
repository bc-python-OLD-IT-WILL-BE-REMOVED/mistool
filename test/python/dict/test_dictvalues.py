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

from mistool import python_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = Path(__file__).parent

DICT_VALUES_FUNCTION = python_use.dictvalues


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'dictvalues.txt',
    mode    = {"keyval:: =": ":default:"}
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove_extras():
        THE_DATAS_FOR_TESTING.remove_extras()

    request.addfinalizer(remove_extras)


# ------------- #
# -- QUOTING -- #
# ------------- #

def test_python_use_dictvalues(or_datas):
    tests = THE_DATAS_FOR_TESTING.mydict("std nosep nonb")

    for testname, infos in tests.items():
        onedict = infos['onedict']
        onedict = eval(onedict)

        singlevalues_wanted = infos['singlevalues']
        singlevalues_wanted = eval(singlevalues_wanted)

        singlevalues_found = DICT_VALUES_FUNCTION(onedict)
        singlevalues_found = sorted(singlevalues_found)

        assert singlevalues_wanted == singlevalues_found
