#!/usr/bin/env python3

"""
prototype::
    date = 2015-06-02


This script contains two functions to ease the use of the package ``datetime``.
"""

from datetime import (
    datetime,
    timedelta
)

from mistool.config import date_name


# ------------------- #
# -- SPECIAL DATES -- #
# ------------------- #

_WEEKDAYS = {
    "monday"   : 0,
    "tuesday"  : 1,
    "wednesday": 2,
    "thursday" : 3,
    "friday"   : 4,
    "saturday" : 5,
    "sunday"   : 6
}

def nextday(date, name):
    """
prototype::
    see = datetime

    arg = datetime.date: date ;
          the date
    arg = str: name ;
          the english long name of the day wanted

    return = datetime.date ;
             the date of the next day with name equal to the value of ``name``


In some applications, you have a date and you want to find the nearest coming
day given by its name, for example the next nearest sunday after november the
30th of the year 2013. You can achieve this using a code like the one above
(the local settings of the computer used were english ones).

pyterm::
    >>> from datetime import datetime
    >>> from mistool.date_use import nextday
    >>> onedate = datetime.strptime("2013-11-30", "%Y-%m-%d")
    >>> print(onedate.strftime("%Y-%m-%d is a %A"))
    2013-11-30 is a Saturday
    >>> nextsunday = nextday(date = onedate, name = "sunday")
    >>> print("Next Sunday:", nextsunday.strftime("%Y-%m-%d"))
    Next Sunday: 2013-12-01


info::
    The simple but efficient method used in the code was found in cf::``this
    discussion ; http://stackoverflow.com/a/6558571/1054158``.
    """
    name = name.lower()

    if name not in _WEEKDAYS:
        raise ValueError("illegal day name.")

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


def translate(date, strformat, lang = DEFAULT_LANG):
    """
prototype::
    see = datetime

    arg = datetime.date: date ;
          the date
    arg = str: strformat ;
          this string follows the special formatters available in the method
          ``strftime`` of the class ``datetime.date``.
    arg = str: lang = DEFAULT_LANG ;
          this defines the language to use, the syntax is the one of the
          function ``locale.setlocale`` of the standard package ``locale``.

    return = str ;
             the date formatting by ``strftime`` but with the name translating
             regarding to the value of ``lang``


The aim of this function is to avoid the use of something like in the following
code (the documentation of the standard package ``locale`` avoids to do that kind
of things).

pyterm::
    >>> import locale
    >>> import datetime
    >>> print (datetime.date(2015, 6, 2).strftime("%A %d %B %Y"))
    Tuesday 02 June 2015
    >>> locale.setlocale(locale.LC_ALL, 'fr_FR')
    'fr_FR'
    >>> print (datetime.date(2015, 6, 2).strftime("%A %d %B %Y"))
    Mardi 02 juin 2015


The same thing can be achieved using the function ``translate`` like in the
following lines of code (the mechanism used in backstage is very basic : it
never calls the standard package ``locale``).

pyterm::
    >>> import datetime
    >>> from mistool.date_use import translate
    >>> onedate   = datetime.date(2015, 6, 2)
    >>> oneformat = "%A %d %B %Y"
    >>> print(translate(date = onedate, strformat = oneformat))
    Tuesday 02 June 2015
    >>> print(translate(date = onedate, strformat = oneformat, lang = "fr_FR"))
    Mardi 02 juin 2015
"""
    if lang not in LANGS:
        raise ValueError(
            'illegal value << {0} >> for the argument ``lang``.'.format(lang)
        )

    nbday   = date.weekday()
    nbmonth = date.month - 1

    for oneformat in ['%a', '%A']:
        if oneformat in strformat:
            dayname = _POINTERS[
                _FORMATS_TRANSLATIONS[oneformat][lang]
            ][nbday]

            strformat = strformat.replace(oneformat, dayname)

    for oneformat in ['%b', '%B']:
        if oneformat in strformat:
            monthname = _POINTERS[
                _FORMATS_TRANSLATIONS[oneformat][lang]
            ][nbmonth]

            strformat = strformat.replace(oneformat, monthname)

    return date.strftime(strformat)
