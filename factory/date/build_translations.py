#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

import locale
import datetime

from pathlib import Path


# --------------- #
# -- CONSTANTS -- #
# --------------- #

THIS_DIR = Path(__file__).parent

for parent in THIS_DIR.parents:
    if parent.name == "misTool":
        break

PY_FILE = parent / 'mistool/config/date_name.py'


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
lang2word = {}
langs_supported = []

for onelang in langs:
    try:
        locale.setlocale(locale.LC_ALL, onelang)

#    * Days
        for format_ in ["%A", "%a"]:
            l2w = lang2word.get(format_, {})

            alldaynames = []

            for day in DAY_NAME:
                dayname = day.strftime(format_).strip()

                if dayname:
                    alldaynames.append(dayname)

            if len(alldaynames) == 7:
                if format_ == "%A":
                    langs_supported.append(onelang)

                if onelang in langs_supported:
                    l2w[onelang]       = alldaynames
                    lang2word[format_] = l2w

#   * Months
        for format_ in ["%B", "%b"]:
            l2w = lang2word.get(format_, {})

            allmonthnames = []

            for month in MONTH_NAME:
                monthname = month.strftime(format_).strip()

                if monthname:
                    allmonthnames.append(monthname)

            if len(allmonthnames) == 12:
                if onelang in langs_supported:
                    l2w[onelang]       = allmonthnames
                    lang2word[format_] = l2w

    except locale.Error:
        ...


# -------------- #
# -- POINTERS -- #
# -------------- #

print('    * Building the pointers')

pointers = []

for _, trans in lang2word.items():
    newTrans = {}

    for lang, words in trans.items():
        if not words in pointers:
            pointers.append(words)

        trans[lang] = pointers.index(words)


# ---------------------------- #
# -- UPDATE THE PYTHON FILE -- #
# ---------------------------- #

print('    * Updating the Python file')

PY_TEXT = """#!/usr/bin/env python3

# Note: the following ugly variables were automatically built.

LANGS = {0}

_POINTERS = {1}

_FORMATS_TRANSLATIONS = {2}
""".format(
    repr(langs_supported),
    repr(pointers),
    repr(lang2word)
)

with PY_FILE.open(
    mode     = 'w',
    encoding = 'utf-8'
) as f:
    f.write(PY_TEXT)
