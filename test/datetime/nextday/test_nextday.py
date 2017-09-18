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
    content = THIS_DIR / 'nextday.txt',
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

def test_datetime_use_nextday(or_datas):
    tests = THE_DATAS_FOR_TESTING.mydict("std nosep nonb")

    for testname, infos in tests.items():
        date_start  = infos['start']
        y, m, d     = [int(x) for x in date_start.split('-')]
        ddate_start = BUILD_DDATETIME(y, m, d)

        next_date_wanted  = infos['next']
        y, m, d           = [int(x) for x in next_date_wanted.split('-')]
        next_ddate_wanted = BUILD_DDATETIME(y, m, d)

        name = infos['name']

        next_ddate_found = ddate_start.nextday(name = name)

        assert next_ddate_wanted == next_ddate_found
