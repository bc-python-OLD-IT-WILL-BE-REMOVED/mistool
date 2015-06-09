#!/usr/bin/env python3

"""
prototype::
    date = 2015-06-03

This module contains some simple tools about the ¨python programming language.
"""

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
