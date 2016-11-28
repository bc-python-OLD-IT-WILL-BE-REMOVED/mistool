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

TRANSLATE_FUNCTION = date_use.translate


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'translate.txt',
    mode    = {"keyval:: =": ":default:"}
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove_extras():
        THE_DATAS_FOR_TESTING.remove_extras()

    request.addfinalizer(remove_extras)


# --------------------- #
# -- TRANSLATE DATES -- #
# --------------------- #

def test_date_use_translate(or_datas):
    tests = THE_DATAS_FOR_TESTING.mydict("std nosep nonb")

    for testname, infos in tests.items():
        date    = infos['date']
        y, m, d = [int(x) for x in date.split('-')]
        date    = datetime.date(y, m, d)

        lang      = infos['lang']
        strformat = infos['format']

        translation_wanted = infos['translation']

        translation_found = TRANSLATE_FUNCTION(
            date      = date,
            strformat = strformat,
            lang      = lang
        )

        assert translation_wanted == translation_found
