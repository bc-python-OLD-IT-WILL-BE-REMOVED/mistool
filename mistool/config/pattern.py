#!/usr/bin/env python3

import re


# ----------- #
# -- WORDS -- #
# ----------- #

FR_ACCENTUED_LETTERS = "âàéèêëîïôùüç"

PATTERNS_WORDS = {
# Natural language
    'en': re.compile("([a-zA-Z]+)"),
    'fr': re.compile(
        "([a-z{0}A-Z{1}]+)".format(
            FR_ACCENTUED_LETTERS,
            FR_ACCENTUED_LETTERS.upper()
        )
    ),
# Coding
    'var': re.compile("([a-zA-Z][\d_a-zA-Z]*)"),
}


# ----------------- #
# -- REGPATTERNS -- #                       # DOC OK !!
# ----------------- #

_PATH_QUERIES       = set(["visible", "dir", "file"])
_SHORT_PATH_QUERIES = {x[0]: x for x in _PATH_QUERIES}
_FILE_DIR_QUERIES   = _PATH_QUERIES - set(["visible"])

def regpat2meta(regpattern, regexit = True):
    """
lkind of mix between regex and Unix-glob syntax


 It allows to use almost
all the power of regexes in a pattern with also some additional queries.



Here are the difference between the regpatterns and the traditional regexes.

    1) ``*`` indicates any character except the separator of the OS.

    2) ``**`` indicates any character with also the separator of the OS.

    3) ``.`` is not a spcieal character, this is just a point.


warning::
    still experimental with known bug , just use the precedin example for the momemnt




Let's see some examples of patterns ``regpattern``.

    1) By default, ``regpattern = **"``. This will macth anything.

    2) ``"*.(py|txt)"`` asks to keep only direct files with either path::``py``
    or path::``txt``. This is the main reason of the add of a new method.

    3) For example, if you want to keep only the Python files, just use
    ``"file::**.py"``. We have used a filter at the begining of the pattern
    ``regpattern``. Here are all the queries.

        a) ``file::`` asks to keep only files. You can use the shortcut ``f``.

        b) ``dir::`` asks to keep only directories, or folders. You can use the
        shortcut ``d``.

        c) ``visible::`` asks to keep only visible files and directories which
        have name begining with ``.``. If a file is inside an invisible folder,
        it is also invisible ! You can use the shortcut ``v``.

        d) ``visible-file::`` and ``visible-dir::`` ask to respectively keep
        only visible files, or only visible directories.




info::
    This function is used by the method ``walk`` and ``clean`` of the class
    ``os_use.PPath`` and also by the class ``os_use.DirView`` so as to keep or
    discard some paths.
    """
    i = regpattern.find("::")

    if i > -1:
        queries, pattern = regpattern[:i], regpattern[i+2:]
        queries = set(_SHORT_PATH_QUERIES.get(x, x) for x in queries.split("-"))

        if not queries <= _PATH_QUERIES:
            raise ValueError("illegal filter in the regpattern.")

    else:
        queries, pattern = _FILE_DIR_QUERIES, regpattern

# The regex
    if regexit:
        for old, new in {
            '*': ".*",
            '.': "\.",
        }.items():
            pattern = pattern.replace(old, new)

    return queries, pattern
