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

    def remove():
        for kind in THE_DATAS_FOR_TESTING:
            THE_DATAS_FOR_TESTING[kind].remove()

    request.addfinalizer(remove)


# ----------------- #
# -- GOOD INPUTS -- #
# ----------------- #

def test_os_use_depth_good(or_datas):
    tests = THE_DATAS_FOR_TESTING['good'].flatdict(nosep = True)

    for name, datas in tests.items():
        main = datas['main'].replace('/', os_use.SEP)
        main = PPATH_CLASS(main)

        sub = datas['sub'].replace('/', os_use.SEP)
        sub = PPATH_CLASS(sub)

        depth = datas['depth']

        depth_found = str(sub.depth_in(main))

        assert depth == depth_found
        print(name)


# ---------------- #
# -- BAD INPUTS -- #
# ---------------- #

def test_os_use_depth_bad(or_datas):
    tests = THE_DATAS_FOR_TESTING['bad'].flatdict(nosep = True)

    for name, datas in tests.items():
        main = datas['main'].replace('/', os_use.SEP)
        main = PPATH_CLASS(main)

        sub = datas['sub'].replace('/', os_use.SEP)
        sub = PPATH_CLASS(sub)

        with raises(ValueError):
            sub.depth_in(main)
