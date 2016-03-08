#!/usr/bin/env python3

"""
prototype::
    date = 2015-06-26

This script proposes two useful functions to manipulate urls.
"""

import requests
from requests.exceptions import ConnectionError
from requests.utils import quote


# ---------------- #
# -- FORMATTING -- #
# ---------------- #

CHAR_TO_KEEP = "/:#&?="

def escape(url):
    """
prototype::
    arg = str: url ;
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

def islinked(url):
    """
prototype::
    arg = str: url ;
          the link that must be tested

    return = bool ;
             ``True`` if the script has been able to open the link, and ``False``
             otherwise


This function try to open the url given in the variable ``url`` so as to know if
the url is accessible. If the connection is possible then ``True`` is returned,
if not that is ``False`` which is sent.

pyterm::
    >>> from mistool.url_use import islinked
    >>> islinked("http://www.google.com")
    True
    >>> islinked("http://www.g-o-o-g-l-e.com")
    False
    """
    try:
        requests.get(url)
        return True

    except ConnectionError as e:
        return False
