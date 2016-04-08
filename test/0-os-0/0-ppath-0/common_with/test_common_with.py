#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from pathlib import Path as StdPath
from pytest import fixture

from orpyste.data import ReadBlock as READ


# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from mistool import os_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = StdPath(__file__).parent

PPATH_CLASS = os_use.PPath


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'common_with.txt',
    mode    = {
        "container": ":default:",
        "verbatim" : ["common", "main_path", "other_paths"]
    }
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove():
        THE_DATAS_FOR_TESTING.remove()

    request.addfinalizer(remove)


# ----------------- #
# -- COMMON PATH -- #
# ----------------- #

def test_os_use_common_with(or_datas):
    tests = THE_DATAS_FOR_TESTING.recudict()

    for name, datas in tests.items():
        main_path = datas['main_path'][0].replace('/', os_use.SEP)
        main_path = PPATH_CLASS(main_path)

        other_paths = [
            PPATH_CLASS(x.replace('/', os_use.SEP))
            for x in datas['other_paths']
        ]

        common = datas.get('common', "/")[0].replace('/', os_use.SEP)
        common = PPATH_CLASS(common)

        common_found = main_path.common_with(other_paths)

        assert common == common_found
