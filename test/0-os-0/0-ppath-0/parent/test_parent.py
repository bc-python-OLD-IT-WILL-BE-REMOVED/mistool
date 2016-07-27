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
    content = THIS_DIR / 'parent.txt',
    mode    = {"keyval:: =": ":default:"}
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove():
        THE_DATAS_FOR_TESTING.remove()

    request.addfinalizer(remove)


# ---------------------- #
# -- PARENT DIRECTORY -- #
# ---------------------- #

def test_os_use_parent_dir(or_datas):
    tests = THE_DATAS_FOR_TESTING.flatdict(nosep = True)

    for kind, datas in tests.items():
        path = datas['path'].replace('/', os_use.SEP)
        path = PPATH_CLASS(path)

        parent = datas['parent'].replace('/', os_use.SEP)
        parent = PPATH_CLASS(parent)

        parent_found = path.parent

        assert parent == parent_found