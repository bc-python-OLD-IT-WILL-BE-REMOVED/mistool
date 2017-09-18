#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

import locale
import datetime
from pathlib import Path

from orpyste.data import ReadBlock


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = Path(__file__).parent

for parent in THIS_DIR.parents:
    if parent.name == "misTool":
        break

PY_FILE = parent / 'mistool/config/date_name.py'


# ------------------- #
# -- NAME TO INDEX -- #
# ------------------- #

WEEKDAYS_TO_INDEXES = {
    name: i
    for i,  name in enumerate([
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
    ])
}


# ------------------ #
# -- TRANSLATIONS -- #
# ------------------ #

print('    * Looking for the translations...')

# List of the candidate for the translations
langs = []

for onelang in locale.locale_alias.items():
    onelang = onelang[1]

    if "_" in onelang:
        onelang = onelang.split('.')[0]

        if not onelang in langs \
        and not onelang in ['am_ET']:
            langs.append(onelang)

langs.sort()

# List of date for naming days and months.
#
# We know that the 16 September was a monday.
DAY_NAME = [
    datetime.date(2013, 9, day) for day in range(16, 23)
]

MONTH_NAME = [
    datetime.date(2013, month, 1) for month in range(1, 13)
]

# Each word translated and all the languages that correspond to it.
LANG2WORD = {}
LANGS_SUPPORTED = []

for onelang in langs:
    try:
        locale.setlocale(locale.LC_ALL, onelang)

#    * Days
        for format_ in ["%A", "%a"]:
            l2w = LANG2WORD.get(format_, {})

            alldaynames = []

            for day in DAY_NAME:
                dayname = day.strftime(format_).strip()

                if dayname:
                    alldaynames.append(dayname)

            if len(alldaynames) == 7:
                if format_ == "%A":
                    LANGS_SUPPORTED.append(onelang)

                if onelang in LANGS_SUPPORTED:
                    l2w[onelang]       = alldaynames
                    LANG2WORD[format_] = l2w

#   * Months
        for format_ in ["%B", "%b"]:
            l2w = LANG2WORD.get(format_, {})

            allmonthnames = []

            for month in MONTH_NAME:
                monthname = month.strftime(format_).strip()

                if monthname:
                    allmonthnames.append(monthname)

            if len(allmonthnames) == 12:
                if onelang in LANGS_SUPPORTED:
                    l2w[onelang]       = allmonthnames
                    LANG2WORD[format_] = l2w

    except locale.Error:
        ...


# -------------- #
# -- POINTERS -- #
# -------------- #

print('    * Building the POINTERS FOR WORDS')

POINTERS = []

for _, trans in LANG2WORD.items():
    newTrans = {}

    for lang, words in trans.items():
        if not words in POINTERS:
            POINTERS.append(words)

        trans[lang] = POINTERS.index(words)


# ------------- #
# -- PARSING -- #
# ------------- #

print('    * Looking for parsing infos...')


EXTRAS_POINTERS = []
HMS             = {}
JUMP            = {}

PARSE_EXTRAS_DIR = THIS_DIR / "config" / "parse_extras"

for langfile in PARSE_EXTRAS_DIR.glob("*.peuf"):
    lang = langfile.stem

    with ReadBlock(
        content = langfile,
        mode    = "verbatim"
    ) as datas:
        datas = datas.mydict("std nosep nonb")

        hms = []

        for kind in ["hour", "minute", "second"]:
            pieces = []

            for onepiece in " ".join(datas[kind]).split(" "):
                onepiece = onepiece.strip()

                if onepiece:
                    pieces.append(onepiece)

            if len(pieces) != 3:
                raise ValueError(f"illegal definition for ``{kind}`` in file ``{lang}.peuf``")

            hms.append(tuple(pieces))

            if hms not in EXTRAS_POINTERS:
                EXTRAS_POINTERS.append(hms)

            HMS[lang] = EXTRAS_POINTERS.index(hms)


        jump = []

        for onepiece in " ".join(datas["jump"]).split(" "):
            onepiece = onepiece.strip()

            if onepiece:
                jump.append(onepiece)

        if jump not in EXTRAS_POINTERS:
            EXTRAS_POINTERS.append(jump)

        JUMP[lang] = EXTRAS_POINTERS.index(jump)


# Auto added lang
for onedict in [HMS, JUMP]:
    langs = list(onedict.keys())

    for lang in langs:
        pointers_infos = LANG2WORD['%A']
        pointerwanted  = pointers_infos[lang]

        for otherlang in pointers_infos:
            if otherlang != lang \
            and pointers_infos[otherlang] == pointerwanted:
                onedict[otherlang] = onedict[lang]


# ---------------------------- #
# -- UPDATE THE PYTHON FILE -- #
# ---------------------------- #

print('    * Updating the Python file')

PY_TEXT = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Note: the following ugly variables were automatically built.

WEEKDAYS = {WEEKDAYS_TO_INDEXES}

LANGS = {LANGS_SUPPORTED}

POINTERS = {POINTERS}

FORMATS_TRANSLATIONS = {LANG2WORD}

EXTRAS_POINTERS = {EXTRAS_POINTERS}

HMS_TRANSLATIONS = {HMS}

JUMP_TRANSLATIONS = {JUMP}
"""

with PY_FILE.open(
    mode     = 'w',
    encoding = 'utf-8'
) as f:
    f.write(PY_TEXT)
