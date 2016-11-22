#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from pathlib import Path as StdPath
from pytest import fixture, raises

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

THE_DATAS_FOR_TESTING = {}

for kind in ['good', 'bad']:
    THE_DATAS_FOR_TESTING[kind] = READ(
        content = THIS_DIR / 'depth_{0}.txt'.format(kind),
        mode    = {"keyval:: =": ":default:"}
    )

@fixture(scope="module")
def or_datas(request):
    for kind in THE_DATAS_FOR_TESTING:
        THE_DATAS_FOR_TESTING[kind].build()

    def remove_extras():
        for kind in THE_DATAS_FOR_TESTING:
            THE_DATAS_FOR_TESTING[kind].remove_extras()

    request.addfinalizer(remove_extras)


# ----------------- #
# -- GOOD INPUTS -- #
# ----------------- #

def test_os_use_depth_good(or_datas):
    tests = THE_DATAS_FOR_TESTING['good'].treedict

    for testname, infos in tests.items():
        main = infos['main']['value']
        main = PPATH_CLASS(main)

        sub = infos['sub']['value']
        sub = PPATH_CLASS(sub)

        depth_wanted = infos['depth']['value']

        depth_found = str(sub.depth_in(main))

        assert depth_wanted == depth_found


# ---------------- #
# -- BAD INPUTS -- #
# ---------------- #

def test_os_use_depth_bad(or_datas):
    tests = THE_DATAS_FOR_TESTING['bad'].treedict

    for testname, infos in tests.items():
        main = infos['main']['value']
        main = PPATH_CLASS(main)

        sub = infos['sub']['value']
        sub = PPATH_CLASS(sub)

        with raises(ValueError):
            sub.depth_in(main)
