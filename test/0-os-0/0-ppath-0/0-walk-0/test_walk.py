#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from pathlib import Path as StdPath
from pytest import fixture


# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from mistool import os_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = StdPath(__file__).parent

PPATH_CLASS = os_use.PPath


# --------------------------------------- #
# -- THE_DATAS_FOR_TESTING FOR TESTING -- #
# --------------------------------------- #

DIR_PPATH = THIS_DIR

while DIR_PPATH.name != "test":
    DIR_PPATH = DIR_PPATH.parent

DIR_PPATH = DIR_PPATH / "virtual_dir" / "complex_dir"
DIR_PPATH = PPATH_CLASS(DIR_PPATH)

# To find paths, we have to use standard methods ! So boring...
# We use the method ``glob`` coming directly from ``pathlib.Path``.
ALL_PATHS_WANTED = []
ALL_FILES_WANTED = []
ALL_DIRS_WANTED  = []

MAX_DEPTH = 10

for i in range(MAX_DEPTH):
    files  = []
    dirs   = []
    prefix = "*/"*i

# Files
    for ppath in DIR_PPATH.glob("{0}*".format(prefix)):
        strpath = str(ppath.relative_to(DIR_PPATH))

        if "." in strpath:
            files.append(strpath)

        else:
            dirs.append(strpath)

    ALL_PATHS_WANTED += files + dirs
    ALL_FILES_WANTED += files
    ALL_DIRS_WANTED  += dirs


# ------------------------- #
# -- WALKING IN A FOLDER -- #
# ------------------------- #

def test_walk_all():
    paths_found = [
        str(p.relative_to(DIR_PPATH))
        for p in DIR_PPATH.walk()
    ]

    assert ALL_PATHS_WANTED == paths_found


def test_walk_all_dirs():
    paths_found = [
        str(p.relative_to(DIR_PPATH))
        for p in DIR_PPATH.walk("dir::**")
    ]

    assert ALL_DIRS_WANTED == paths_found


def test_walk_all_files():
    paths_found = [
        str(p.relative_to(DIR_PPATH))
        for p in DIR_PPATH.walk("file::**")
    ]

    assert ALL_FILES_WANTED == paths_found


def test_walk_all_python_files():
    paths_found = [
        str(p.relative_to(DIR_PPATH))
        for p in DIR_PPATH.walk("file::**.py")
    ]

    all_py_files_wanted = [p for p in ALL_FILES_WANTED if p.endswith(".py")]

    assert all_py_files_wanted == paths_found
