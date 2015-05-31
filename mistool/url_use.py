#!/usr/bin/env python3

"""
???


prototype::
    date = 2014-08

This script proposes some useful functions to manipulate urls.
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
This function escapes no ASCII characters in urls. For example,
``escape("http://www.vivaespaña.com/camión/")`` is equal to
``http://www.vivaespa%C3%B1a.com/cami%C3%B3n/``.

The function uses the global string ``CHAR_TO_KEEP`` which contains the
characters that must not be escaped : ``"/:#&?="``.
    """
    return quote(
        string = url,
        safe   = CHAR_TO_KEEP
    )


# ------------- #
# -- TESTING -- #
# ------------- #

def test(
    url,
    timeout = -1
):
    """
This function try to open the url given in the variable ``url`` so as to know if
the url is a real one. If the connection works ``True`` is returned, if not that
is ``False`` which is sent.

There is one optional argument ``timeout`` to indicate an upper bound in seconds
for the whole duration of the test. By default, this variable is equal to
``(-1)`` which indicates no upper bound.
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
