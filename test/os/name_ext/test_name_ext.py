#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from pathlib import Path

# Homemade ugly tools !
from pdt.orpyste import reader


# -------------------- #
# -- WHAT IS TESTED -- #
# -------------------- #

from mistool import os_use

PPATH = os_use.PPath


# ------------- #
# -- GENERAL -- #
# ------------- #

READER   = reader.Build
THIS_DIR = Path(__file__).parent


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READER(
    path = THIS_DIR / 'name_ext.txt',
    mode = "equal"
).dict


# ------------------------------------ #
# -- EXTENSION AND NAME FROM A PATH -- #
# ------------------------------------ #

def test_os_use_file_name_extension():
    for kind, datasfortest in THE_DATAS_FOR_TESTING.items():
        path  = datasfortest['path'].replace('/', os_use.SEP)
        name  = datasfortest['name']
        ext   = datasfortest['ext']
        noext = datasfortest['noext']

        path = PPATH(path)

        name_found  = FILE_NAME_FUNCTION(path)
        ext_found   = EXTENSION_FUNCTION(path)
        noext_found = PATH_NO_EXT_FUNCTION(path)

        assert name == name_found
        assert ext == ext_found
        assert noext == noext_found
