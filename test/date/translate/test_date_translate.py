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

TRANSLATE_FUNCTION = date_use.translate


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'date_translate.txt',
    mode    = {"keyval:: =": ":default:"}
)


# --------------------- #
# -- TRANSLATE DATES -- #
# --------------------- #

def test_date_use_translate():
    THE_DATAS_FOR_TESTING.build()

    for oneinfo in THE_DATAS_FOR_TESTING:
        if oneinfo.isdata():
            datas = oneinfo.short_rtu_data

            date    = datas["date"]["value"]
            y, m, d = [int(x) for x in date.split('-')]
            date    = datetime.date(y, m, d)

            lang        = datas["lang"]["value"]
            strformat   = datas["format"]["value"]
            translation = datas["translation"]["value"]

            translation_found = TRANSLATE_FUNCTION(
                date      = date,
                strformat = strformat,
                lang      = lang
            )

            assert translation == translation_found

    THE_DATAS_FOR_TESTING.remove()
