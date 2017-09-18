#!/usr/bin/env python3

"""
prototype::
    date = 2017-09-18


This script tries to ease the use of dates.
"""

from copy import deepcopy
from datetime import *

from dateutil.parser import (
    parse as _parsedate,
    parserinfo as _ParserInfo
)

from mistool.config.date_name import *


# --------------------------------------------------- #
# -- ENHANCED VERSION OF ``dateutil.parser.parse`` -- #
# --------------------------------------------------- #

_PARSER_INFOS_USED = {}

def _buildnamesparsed(lang, lowformat):
    """
This hidden function is used to build the attributs ``WEEKDAYS`` and ``MONTHS``
of the subclasses of ``dateutil.parser.parserinfo`` used to localize the
parsing.
    """
    return list(
        zip(
            POINTERS[FORMATS_TRANSLATIONS[lowformat][lang]],
            POINTERS[FORMATS_TRANSLATIONS[lowformat.upper()][lang]]
        )
    )

def _buildnewparserinfo(lang):
    """
This hidden function builds a subclass of ``dateutil.parser.parserinfo`` for a
special supported language such as to parse string as a date.
    """
    if lang not in JUMP_TRANSLATIONS:
        raise ValueError(f"unsupported language ''{lang}''")

    class _NewParserInfo(_ParserInfo):
        WEEKDAYS = _buildnamesparsed(
            lang      = lang,
            lowformat = '%a'
        )

        MONTHS = _buildnamesparsed(
            lang      = lang,
            lowformat = '%b'
        )

        JUMP = EXTRAS_POINTERS[JUMP_TRANSLATIONS[lang]] \
             + [' ', '.', ',', ';', '-', '/', "'", '"']

        HMS = EXTRAS_POINTERS[HMS_TRANSLATIONS[lang]]

    _PARSER_INFOS_USED[lang] = deepcopy(_NewParserInfo())


def parsedate(timestr, lang = "en_GB"):
    """
prototype::
    see = dateutil.parser.parse

    arg = str: timestr ;
          a string to parse
    arg = str: lang = "en_GB" ;
          the language in ISO format

    return = ddatetime ;
             the date found after parsing


Here are some examples of used.

pyterm::
    >>> from mistool.datetime_use import parsedate
    >>> parsedate("Friday 01 august 2017")
    ddatetime(2017, 8, 1, 0, 0)
    >>> parsedate(timestr = "Vendredi 1er Août 2017", lang = "fr_FR")
    ddatetime(2017, 8, 1, 0, 0)
    >>> parsedate(timestr = "Montag, 11. April 2016", lang = "de_DE")
    [...]
    ValueError: unsupported language ''de_DE''
    """
    if lang not in LANGS:
        raise ValueError(
            'illegal value << {0} >> for the argument ``lang``.'.format(lang)
        )

    elif lang not in _PARSER_INFOS_USED:
        _buildnewparserinfo(lang)

    return build_ddatetime(
        _parsedate(
            timestr    = timestr,
            parserinfo = _PARSER_INFOS_USED[lang]
        )
    )


# -------------------------------------- #
# -- ENHANCED VERSION OF ``datetime`` -- #
# -------------------------------------- #

def build_ddatetime(*args, **kwargs):
    """
prototype::
    see = ddatetime

    return = ddatetime ;
             the date indicated using one special format


This function allaows to use different ways to define one date that will be
transformed in one instance of the "homemade" class ``ddatetime``.


Here are some examples of used.

pyterm::
    >>> from mistool.datetime_use import build_ddatetime
    >>> build_ddatetime((2017, 8, 1))
    ddatetime(2017, 8, 1, 0, 0)
    >>> build_ddatetime(2017, 8, 1)
    ddatetime(2017, 8, 1, 0, 0)
    >>> build_ddatetime("2017-08-01")
    ddatetime(2017, 8, 1, 0, 0)
    >>> build_ddatetime("Friday 01 august 2017")
    ddatetime(2017, 8, 1, 0, 0)
    >>> build_ddatetime("Vendredi 1er août 2017", lang = "fr_FR")
    ddatetime(2017, 8, 1, 0, 0)
    >>> build_ddatetime("Vendredi 1er août 2017")
    [...]
    ValueError: Unknown string format
    >>> build_ddatetime("Vendredi 1er août 2017", "fr_FR")
    [...]
    TypeError: an integer is required (got type str)


warning::
    You **must** define a special language using ``lang = "fr_FR"`` as you can
    see in the two last commands in the preceding example.
    """
    datetime_version = None

# One single argument
    if len(args) == 1:
        onearg = args[0]

        if isinstance(onearg, (tuple, list)):
            datetime_version = datetime(*onearg)

        elif isinstance(onearg, str):
            lang = kwargs.get("lang", "en_GB")

            datetime_version = parsedate(
                timestr = onearg,
                lang    = lang
            )

        elif isinstance(onearg, datetime):
            datetime_version = onearg

        else:
            raise TypeError(
                "unsupported single argument with type ``{0}``".format(
                    type(onearg)
                )
            )

# Several arguments used.
    else:
        datetime_version = datetime(*args, **kwargs)

# From a datetime object to a DDateTime object.
    kwargs = {
        oneattr: getattr(datetime_version, oneattr)
        for oneattr in [
            "year", "month", "day",
            "hour", "minute", "second", "microsecond",
            "tzinfo"
        ]
    }

    return ddatetime(**kwargs)


class ddatetime(datetime):
    """
prototype::
    see = build_ddatetime

    type = cls ;
           an enhanced version of the standard class ``datetime.datetime``


====================================
Next day having a fixed english name
====================================

In some applications, you have a date and you want to find the nearest coming
day given by its name, for example the next nearest sunday after november the
30th of the year 2013. You can achieve this using a code like the one above
(the local settings of the computer used were english ones).

pyterm::
    >>> from mistool.datetime_use import ddatetime
    >>> onedate = ddatetime(2017,8, 1)
    >>> print(onedate.strftime("%Y-%m-%d is a %A."))
    2017-08-01 is a Tuesday.
    >>> nextfriday = onedate.nextday(name = "friday")
    >>> print("Next Friday:", nextfriday.strftime("%Y-%m-%d"))
    Next Friday: 2017-08-04


==================
Translating a date
==================

The class ``ddatetime`` has one method ``translate`` so as to avoid the use of
something like in the following code (the documentation of the standard package
``locale`` says to not do that kind of things).

pyterm::
    >>> import locale
    >>> import datetime
    >>> print (datetime.date(2015, 6, 2).strftime("%A %d %B %Y"))
    Tuesday 02 June 2015
    >>> locale.setlocale(locale.LC_ALL, 'fr_FR')
    'fr_FR'
    >>> print (datetime.date(2015, 6, 2).strftime("%A %d %B %Y"))
    Mardi 02 juin 2015


The same thing can be achieved using the following lines of code (the mechanism
used in backstage is very basic : it will never call the standard package
``locale``).

pyterm::
    >>> from mistool.datetime_use import ddatetime
    >>> onedate   = ddatetime(2015, 6, 2)
    >>> oneformat = "%A %d %B %Y"
    >>> print(onedate.translate(strformat = oneformat))
    Tuesday 02 June 2015
    >>> print(onedate.translate(strformat = oneformat, lang = "fr_FR"))
    Mardi 02 juin 2015
    """

    def __init__(self, *args, **kwargs):
        super().__init__()

    def nextday(self, name):
        """
prototype::
    see = datetime

    arg = datetime.date: date ;
          the date
    arg = str: name ;
          the english long name of the day wanted

    return = datetime.date ;
             the date of the next day with name equal to the value of ``name``


info::
    The simple but efficient method used here in the code was found in
    cf::``this discussion ; http://stackoverflow.com/a/6558571/1054158``.
    """
        name = name.lower()

        if name not in WEEKDAYS:
            raise ValueError("illegal day name ``{0}``.".format(name))

        daysahead = WEEKDAYS[name] - self.weekday()

        if daysahead <= 0:
            daysahead += 7

        return build_ddatetime(self + timedelta(daysahead))

    def translate(self, strformat, lang = 'en_GB'):
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
"""
        if lang not in LANGS:
            raise ValueError(
                'illegal value << {0} >> for the argument ``lang``.'.format(lang)
            )

        nbday   = self.weekday()
        nbmonth = self.month - 1

        for nbid, formats in [
            (nbday  , ('%a', '%A')),
            (nbmonth, ('%b', '%B'))
        ]:
            for oneformat in formats:
                if oneformat in strformat:
                    name = POINTERS[
                        FORMATS_TRANSLATIONS[oneformat][lang]
                    ][nbid]

                    strformat = strformat.replace(oneformat, name)

        return self.strftime(strformat)
