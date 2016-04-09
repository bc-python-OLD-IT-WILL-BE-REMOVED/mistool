#!/usr/bin/env python3

"""
prototype::
    date = 2016-04-05

This module contains some simple tools about the ¨python programming language.
"""

from collections import Hashable, OrderedDict


# ------------- #
# -- QUOTING -- #
# ------------- #

QUOTE_SYMBOLS = ["'", '"']

def quote(
    text,
    symbol = "'"
):
    """
prototype::
    arg = str: text ;
          the text to be quoted
    arg = str: symbol = "'" ;
          the prefered quoting symbol

    return = str ;
             the text quoted (the quote symbols in ``text`` are escaped if it is
             necessary)


Here is a some examples where you can see that the function tries to use the
less escaped quoting symbols, and when there is a choice that is the value of
``symbol`` which is used.

pyterm::
    >>> from mistool.python_use import quote
    >>> print(quote('First example.'))
    'First example.'
    >>> print(quote("Same example."))
    'Same example.'
    >>> print(quote('One "small" example.'))
    'One "small" example.'
    >>> print(quote("The same kind of 'example'."))
    "The same kind of 'example'."
    >>> print(quote("An example a 'little' more \"problematic\"."))
    'An example a \'little\' more "problematic".'


info::
    This function uses the global constant ``QUOTE_SYMBOLS`` which is defined
    by ``QUOTE_SYMBOLS = ["'", '"']``. This indicates the list of the possible
    quoting symbols.
    """
    if all(x in text for x in QUOTE_SYMBOLS):
        text = text.replace(symbol , '\\' + symbol)

    elif symbol in text:
        for x in QUOTE_SYMBOLS:
            if x != symbol:
                symbol = x

    return "{0}{1}{0}".format(symbol, text)


# ------------------ #
# -- DICTIONARIES -- #
# ------------------ #

def dictvalues(onedict):
    """
prototype::
    arg = dict: onedict

    return = list ;
             a list of the values used in the dictionary ``onedict`` without
             repetition


Here is an example showing a difference with the method ``values`` of the
dictionaries.

pyterm::
    >>> from mistool.python_use import dictvalues
    >>> onedict = {"a": 1, "b": 2, "c": 1}
    >>> print(dictvalues(onedict))
    [1, 2]
    >>> print(list(onedict.values()))
    [2, 1, 1]
    """
    return list(set(onedict.values()))


class OrderedRecuDict(OrderedDict):
    """
This subclass of ``collections.OrderedDict`` allows to use a list of hashable
keys, or just a single hashable key. Here is an example of use where the ouput
is hand formatted.

pyterm::
    >>> from mistool.python_use import OrderedRecuDict
    >>> onerecudict = OrderedRecuDict()
    >>> onerecudict[[1, 2, 4]] = "1st value"
    >>> onerecudict[(1, 2, 4)] = "2nd value"
    >>> print(onerecudict)
    OrderedRecuDict([
        (
            1,
            OrderedRecuDict([
                (
                    2,
                    OrderedRecuDict([ (4, '1st value') ])
                )
            ])
        ),
        (
            (1, 2, 4),
            '2nd value'
        )
    ])
    """
    def __init__(self):
        super().__init__()


    def __getitem__(self, keys):
        if isinstance(keys, Hashable):
            return super().__getitem__(keys)

        else:
            first, *others = keys

            if others:
                return self[first][others]

            else:
                return self[first]


    def __setitem__(self, keys, val):
        if isinstance(keys, Hashable):
            super().__setitem__(keys, val)

        else:
            first, *others = keys

            if first in self and others:
                self[first][others] = val

            else:
                if others:
                    subdict         = OrderedRecuDict()
                    subdict[others] = val
                    val             = subdict

                self[first] = val


    def __contains__(self, keys):
        if isinstance(keys, Hashable):
            return super().__contains__(keys)

        else:
            first, *others = keys

            if first in self:
                if not others:
                    return True

                subdict = self[first]

                if isinstance(subdict, OrderedDict):
                    return others in subdict

            return False
