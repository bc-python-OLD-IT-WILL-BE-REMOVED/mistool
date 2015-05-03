#!/usr/bin/env python3

"""
Directory : mistool
Name      : date_use
Version   : 2014.08
Author    : Christophe BAL
Mail      : projetmbc@gmail.com

This script contains some functions to ease the use pof the standard package
``datetime``.
"""

from datetime import datetime, timedelta

from mistool.config import date_name


# ------------------- #
# -- SPECIAL DATES -- #
# ------------------- #

now = datetime.now

_WEEKDAYS = {
    "monday"   : 0,
    "tuesday"  : 1,
    "wednesday": 2,
    "thursday" : 3,
    "friday"   : 4,
    "saturday" : 5,
    "sunday"   : 6
}

def nextday(
    date,
    name
):
    """
-----------------
Small description
-----------------

In some applications, you have a date and you want to find the nearest coming
day given by its name, for example the next nearest sunday after november the
30th of the year  2013. You can achieve this using a code like the following
one which will print terminal::``2013-12-01``.

python::
    from datetime import datetime

    from mistool import date_use

    print(
        date_use.nextday(
            date = datetime.strptime("2013-11-30", "%Y-%m-%d"),
            name = "sunday",
        ).strftime("%Y-%m-%d")
    )


info::
    The simple but efficient method used in the code was found in cf::``this
    discussion ; http://stackoverflow.com/a/6558571/1054158``.


-------------
The arguments
-------------

This function uses two variables.

    1) ``date`` is a date defined using the class ``datetime.date`` from the
    standard package ``datetime``.

    2) ``name`` is the english long name of the day wanted.
    """
    if name not in _WEEKDAYS:
        raise ValueError("unknown name << {0} >>.".format(name))

    daysahead = _WEEKDAYS[name] - date.weekday()

    if daysahead <= 0:
        daysahead += 7

    return date + timedelta(daysahead)


# ----------------- #
# -- TRANSLATING -- #
# ----------------- #

DEFAULT_LANG = 'en_GB'
LANGS        = date_name.LANGS

_POINTERS             = date_name._POINTERS
_FORMATS_TRANSLATIONS = date_name._FORMATS_TRANSLATIONS

def translate(
    date,
    format,
    lang = DEFAULT_LANG
):
    """
-----------------
Small description
-----------------

The aim of this function is to avoid the use of something like in the following
code (the documentation of the standard package ``locale`` avoids to do that kind
of things).

python::
    import locale
    import datetime

    locale.setlocale(locale.LC_ALL, 'fr_FR')

    print(
        datetime.date(2013, 9, 21).strftime("%A %d %B %Y")
    )

This code prints the text terminal::``Samedi 29 septembre 2013`` in a terminal.
This can be achieved using the function ``translate`` like in the following code.

python::
    from datetime import date

    from mistool import date_use

    print(
        date_use.translate(
            date   = date(2013, 9, 21),
            format = "%A %d %B %Y",
            lang   = "fr_FR"
        )
    )


If you always want to use the same language, you can do it like this.

python::
    import datetime

    from mistool import date_use

    date_use.LANG = 'fr_FR'

    print(
        date_use.translate(
            date   = datetime.date(2013, 9, 21),
            format = "%A %d %B %Y"
        )
    )


info::
    The mechanism used in backstage is very primitive : it never calls the
    standard package ``locale`` !


-------------
The arguments
-------------

This function uses three variables.

    1) ``date`` is a date defined using the class ``datetime.date`` from the
    standard package ``datetime``.

    2) ``format`` is a string that uses the special formatters available with
    the method ``strftime`` of the class ``datetime.date``.

    3) ``lang`` is a language respecting the convention needed for the use of
    the function ``locale.setlocale`` of the standard package ``locale``.

    This optional variable used the default value ``DEFAULT_LANG`` which is a
    module constant defined by ``DEFAULT_LANG = "en_GB"``.
"""
    if lang not in LANGS:
        raise ValueError(
            'illegal value << {0} >> for the argument ``lang``.'.format(lang)
        )

    nbday   = date.weekday()
    nbmonth = date.month - 1

    for oneformat in ['%a', '%A']:
        if oneformat in format:
            dayname = _POINTERS[
                _FORMATS_TRANSLATIONS[oneformat][lang]
            ][nbday]

            format = format.replace(oneformat, dayname)

    for oneformat in ['%b', '%B']:
        if oneformat in format:
            monthname = _POINTERS[
                _FORMATS_TRANSLATIONS[oneformat][lang]
            ][nbmonth]

            format = format.replace(oneformat, monthname)

    return date.strftime(format)
