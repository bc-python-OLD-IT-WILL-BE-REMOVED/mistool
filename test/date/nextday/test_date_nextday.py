#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

import datetime
from pathlib import Path

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


# ---------------- #
# -- NEXT DAY ? -- #
# ---------------- #

def test_date_use_nextday():
    THE_DATAS_FOR_TESTING.build()

    for oneinfo in THE_DATAS_FOR_TESTING:
        if oneinfo.isdata():
            datas = oneinfo.short_rtu_data

            date_start = datas["start"]["value"]
            y, m, d    = [int(x) for x in date_start.split('-')]
            date_start = datetime.date(y, m, d)

            next_date = datas["next"]["value"]
            y, m, d   = [int(x) for x in next_date.split('-')]
            next_date = datetime.date(y, m, d)

            name = datas["name"]["value"]

            date_found = NEXTDAY_FUNCTION(
                date = date_start,
                name = name
            )

            assert next_date == date_found

    THE_DATAS_FOR_TESTING.remove()
