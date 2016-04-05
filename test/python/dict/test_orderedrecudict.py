#!/usr/bin/env python3

# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from mistool import python_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

ORDERED_RECU_DICT = python_use.OrderedRecuDict


# ------------- #
# -- QUOTING -- #
# ------------- #

def test_python_use_ordered_recu_dict():
    onerecudict = ORDERED_RECU_DICT()

    onerecudict[[1, 2, 4]] = "1st value"
    onerecudict[(1, 2, 4)] = "2nd value"

    assert onerecudict[1][2][4] == "1st value"
