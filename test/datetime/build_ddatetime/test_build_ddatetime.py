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

from mistool import datetime_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = Path(__file__).parent

BUILD_DDATETIME = datetime_use.build_ddatetime


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'builddate.txt',
    mode    = {"keyval:: =": ":default:"}
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove_extras():
        THE_DATAS_FOR_TESTING.remove_extras()

    request.addfinalizer(remove_extras)


# ---------------- #
# -- NEXT DAY ? -- #
# ---------------- #

def test_datetime_use_build_ddatetime(or_datas):
    tests = THE_DATAS_FOR_TESTING.mydict("std nosep nonb")

    for testname, infos in tests.items():
        if 'lang' in infos:
            _instr = f"BUILD_DDATETIME({infos['in']}, lang = '{infos['lang']}')"

        else:
            _instr = f"BUILD_DDATETIME({infos['in']})"

        _in  = str(eval(_instr))
        _out = f"{infos['out']} 00:00:00"

        assert _in == _out
