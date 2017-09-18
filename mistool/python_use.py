#!/usr/bin/env python3

"""
prototype::
    date = 2016-11-28

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
             the text quoted (the quote symbols in ``text`` are escaped if it
             is necessary)


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
    >>> print(quote("Another kind of \"example\"."))
    'Another kind of "example".'
    >>> print(quote("An example a 'little' more \"problematic\"."))
    'An example a \'little\' more "problematic".'


info::
    This function uses the global constant ``QUOTE_SYMBOLS`` which is defined
    by ``QUOTE_SYMBOLS = ["'", '"']``. This indicates the list of the possible
    quoting symbols.
    """
    if all(x in text for x in QUOTE_SYMBOLS):
        text = text.replace(symbol, '\\' + symbol)

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


class MKOrderedDict():
    """
This class allows to work easily with multikeys ordered dictionaries. Here is
a complete example of use where some ouputs have been hand formatted.

pyterm::
    >>> from mistool.python_use import MKOrderedDict
    >>> onemkdict = MKOrderedDict()
    >>> onemkdict[(1, 2, 4)] = "1st value"
    >>> onemkdict["key"] = "2nd value"
    >>> onemkdict["key"] = "3rd value"
    >>> print(onemkdict)
    MKOrderedDict([
        ((id=0, key=(1, 2, 4)), value='1st value'),
        ((id=0, key='key')    , value='2nd value'),
        ((id=1, key='key')    , value='3rd value')
    ])
    >>> for k_id, val in onemkdict["key"]:
    ...     print(k_id, val)
    ...
    0 2nd value
    1 3rd value
    >>> print(onemkdict.getitembyid(1, "key"))
    3rd value
    >>> for (k_id, key), val in onemkdict.items():
    ...     print((k_id, key), "===>", val)
    ...
    (0, (1, 2, 4)) ===> 1st value
    (0, 'key') ===> 2nd value
    (1, 'key') ===> 3rd value
    >>> for key, val in onemkdict.items(noid=True):
    ...     print(key, "===>", val)
    ...
    (1, 2, 4) ===> 1st value
    key ===> 2nd value
    key ===> 3rd value
    >>> "key" in onemkdict
    True
    >>> "kaaaay" in onemkdict
    False
    >>> onemkdict.setitembyid(0, "key", "New 2nd value")
    >>> print(onemkdict)
    MKOrderedDict([
        ((id=0, key=(1, 2, 4)), value='1st value'),
        ((id=0, key='key')    , value='New 2nd value'),
        ((id=1, key='key')    , value='3rd value')])
    """

    def __init__(self):
        self._internaldict = OrderedDict()
        self._keyids       = {}
        self._len          = 0

    def __setitem__(self, key, val):
        if not isinstance(key, Hashable):
            raise KeyError("key must be hashable")

        if key in self._keyids:
            self._keyids[key] += 1

        else:
            self._keyids[key] = 0

        self._internaldict[(self._keyids[key], key)] = val

        self._len += 1

    def setitembyid(self, keyid, key, val):
        if (keyid, key) not in self._internaldict:
            self._len += 1

        self._internaldict[(keyid, key)] = val

    def __getitem__(self, key, keyid = None):
        keyfound = False

        for (oneid, onekey), oneval in self._internaldict.items():
            if key == onekey:
                keyfound = True

                yield oneid, oneval

        if not keyfound:
            raise KeyError("key not used in the MKOrderedDict")

    def getitembyid(self, keyid, key):
        for (oneid, onekey), oneval in self._internaldict.items():
            if keyid == oneid and key == onekey:
                return oneval

        raise KeyError("key not used in the MKOrderedDict")

    def items(self, noid = False):
        for id_key, oneval in self._internaldict.items():
            if noid:
                yield id_key[1], oneval

            else:
                yield id_key, oneval

    def __contains__(self, key):
        for (oneid, onekey), oneval in self._internaldict.items():
            if key == onekey:
                return True

        return False

    def __len__(self):
        return self._len

    def __eq__(self, other):
        if not isinstance(other, MKOrderedDict):
            return False

        if self._internaldict.keys() != other._internaldict.keys():
            return False

        for k, v in self._internaldict.items():
            if v != other.getitembyid(*k):
                return False

        return True

    def __str__(self):
        text = repr(self)

        while "\n    " in text:
            text = text.replace("\n    ", "\n")

        text = text.replace("\n", "")

        return text

    def __repr__(self):
        text = ["MKOrderedDict(["]

        for (oneid, onekey), oneval in self._internaldict.items():
            text.append(
                "    (id={0}, key={1}, value={2}), ".format(
                    oneid,
                    repr(onekey),
                    repr(oneval).replace("\n    ", "\n        ")
                )
            )

        if len(text) != 1:
            text[-1] = text[-1][:-2]

        text.append("])")

        text = "\n".join(text)

        return text


class RecuOrderedDict(OrderedDict):
    """
This subclass of ``collections.OrderedDict`` allows to use a list of hashable
keys, or just a single hashable key. Here is a complete example of use where
some ouputs have been hand formatted.

pyterm::
    >>> from mistool.python_use import RecuOrderedDict
    >>> onerecudict = RecuOrderedDict()
    >>> onerecudict[[1, 2, 4]] = "1st value"
    >>> onerecudict[(1, 2, 4)] = "2nd value"
    >>> onerecudict["key"] = "3rd value"
    >>> print(onerecudict)
    RecuOrderedDict([
        (
            1,
            RecuOrderedDict([
                (
                    2,
                    RecuOrderedDict([ (4, '1st value') ])
                )
            ])
        ),
        (
            (1, 2, 4),
            '2nd value'
        ),
        (
            'key',
            '3rd value'
        )
    ])
    >>> [1, 2, 4] in onerecudict
    True
    >>> [2, 4] in onerecudict[1]
    True
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                    subdict         = RecuOrderedDict()
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
