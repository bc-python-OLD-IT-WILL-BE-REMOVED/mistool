#!/usr/bin/env python3

# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from mistool import python_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

RECU_DICT = python_use.RecuOrderedDict


# -------------------------- #
# -- RECURSIVE DICTIONARY -- #
# -------------------------- #

def test_python_use_recu_dict():
    onerecudict = RECU_DICT()

    onerecudict[[1, 2, 4]] = "1st value"
    onerecudict[(1, 2, 4)] = "2nd value"
    onerecudict["string"]  = "3rd value"

    assert onerecudict[1][2][4]   == "1st value"
    assert onerecudict[(1, 2, 4)] == "2nd value"
    assert onerecudict["string"]  == "3rd value"

    assert bool([1, 2, 4] in onerecudict) == True
    assert bool([2, 4] in onerecudict[1]) == True
