#!/usr/bin/env python3

"""
prototype::
    date = 2015-06-02

This script proposes two useful functions to manipulate urls.
"""

from urllib.parse import quote
from urllib.request import urlopen
from urllib.error import URLError


# ---------------- #
# -- FORMATTING -- #
# ---------------- #

CHAR_TO_KEEP = "/:#&?="

def escape(url):
    """
prototype::
    arg    = str: url ;
             the link that must be escaped
    return = str ;
             the escaped ¨http version of the url


This function escapes the url using the ¨http ¨ascii convention. Here is an
example of use.

pyterm::
    >>> from mistool.url_use import escape
    >>> print(escape("http://www.vivaespaña.com/camión/"))
    http://www.vivaespa%C3%B1a.com/cami%C3%B3n/


info::
    The function uses the global string ``CHAR_TO_KEEP = "/:#&?="`` which
    contains the characters that mustn't be escaped.
    """
    return quote(
        string = url,
        safe   = CHAR_TO_KEEP
    )


# ------------- #
# -- TESTING -- #
# ------------- #

def islinked(url, timeout = -1):
    """
prototype::
    arg    = str: url ;
             the link that must be tested
    arg    = float: timeout = -1 ;
             an upper bound in seconds for the whole duration of the test, the
             value ``(-1)`` indicates a merly infinite time
    return = bool ;
             ``True`` if the script has been able to open the link, and ``False``
             otherwise


This function try to open the url given in the variable ``url`` so as to know if
the url is a real one. If the connection works then ``True`` is returned, if not
that is ``False`` which is sent.

pyterm::
    >>> from mistool.url_use import islinked
    >>> islinked("http://www.google.com")
    True
    >>> islinked("http://www.g-o-o-g-l-e.com")
    False


warning::
    A poor connection can lead to false negatives.
    """
    try:
        if timeout == -1:
            urlopen(url)

        else:
            urlopen(
                url = url,
                timeout = timeout
            )

        return True

    except URLError as e:
        ...

    return False
