#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

import datetime
from pathlib import Path
from pytest import fixture

from orpyste.data import ReadBlock as READ


# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from mistool import date_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = Path(__file__).parent

NEXTDAY_FUNCTION = date_use.nextday


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

    def remove():
        THE_DATAS_FOR_TESTING.remove()

    request.addfinalizer(remove)


# ---------------- #
# -- NEXT DAY ? -- #
# ---------------- #

def test_date_use_nextday(or_datas):
    tests = THE_DATAS_FOR_TESTING.flatdict(nosep = True)

    for name, datas in tests.items():
        date_start = datas["start"]
        y, m, d    = [int(x) for x in date_start.split('-')]
        date_start = datetime.date(y, m, d)

        next_date = datas["next"]
        y, m, d   = [int(x) for x in next_date.split('-')]
        next_date = datetime.date(y, m, d)

        name = datas["name"]

        date_found = NEXTDAY_FUNCTION(
            date = date_start,
            name = name
        )

        assert next_date == date_found
