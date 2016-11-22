#!/usr/bin/env python3

# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from mistool import python_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

MULTIKEYS_DICT = python_use.MKOrderedDict


# -------------------------- #
# -- MULTIKEYS DICTIONARY -- #
# -------------------------- #

def test_python_use_multikeys_dict():
    onemkdict = MULTIKEYS_DICT()

    onemkdict[(1, 2, 4)] = "1st value"
    onemkdict["key"] = "2nd value"
    onemkdict["key"] = "3rd value"

    assert onemkdict.getitembyid(0, (1, 2, 4)) == "1st value"
    assert onemkdict.getitembyid(0, "key") == "2nd value"
    assert onemkdict.getitembyid(1, "key") == "3rd value"

    onemkdict.setitembyid(0, "key", "New 2nd value")
    assert onemkdict.getitembyid(0, "key") == "New 2nd value"
