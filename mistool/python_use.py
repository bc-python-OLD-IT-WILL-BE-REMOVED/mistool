#!/usr/bin/env python3

"""
???


prototype::
    date = 2014-08

This module contains some simple tools about the Python programming language.
"""

from subprocess import check_call, check_output

from mistool.os_use import filename, nextfile, parentdir, relativepath


# ------------- #
# -- QUOTING -- #
# ------------- #

QUOTE_SYMBOLS = ["'", '"']

def _escape(data):
    """
This small function escapes all the characters that must be escaped in one
python-like string.
    """
    if isinstance(data, str):
        return data.replace('\\', '\\\\')

    else:
        return data

def quote(
    text,
    symbol = "'"
):
    """
This function put the content of the string variable ``text`` into quotes and
escapes the eventual quote symbols in ``text``.

This function has one optional variable ``symbol`` which indicates the prefered
quoting symbol which is the single quote ``'`` by default.


This function uses the global constant ``QUOTE_SYMBOLS`` which is defined by
``QUOTE_SYMBOLS = ["'", '"']``. This indicates the list of the possible quoting
symbols.

For example, ``quote("one \"small\" example")`` is equal to the text ``'one
"small" example``, and ``quote('another \'example\' to "see" more")``` is equal
to ``'another \'example\' to "see" more'``.
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

def dictvalues(obj):
    """
This function returns a list of all the values stored in one dictionary without
any repetition.
    """
    return list(set(obj.values()))


# --------------- #
# -- LAUNCHING -- #
# --------------- #

# Source :
#    * http://docs.python.org/py3k/library/subprocess.html
_SUBPROCESS_METHOD = {
# ``check_call`` prints informations given during the compilation.
    True : check_call ,
# ``check_output`` does not print informations given during the
# compilation. Indeed it returns all this stuff in one string.
    False: check_output
}

def runpys(
    main,
    prefixes  = {},
    depth     = 0,
    version   = 3,
    isverbose = False
):
    """
-----------------
Small description
-----------------

This function helps to launch easily several ¨python files.


-------------
The arguments
-------------

This function uses the following variables.

    1) The arguments ``main``, ``prefixes`` and``depth`` have exactly the same
    meaning than the ones of the function ``nextfile`` in the module ``os_use``.
    See the documentation of this function ``nextfile`` for more precisions.

    2) ``version`` can be either an integer, or a string.

        a) If ``version`` is an integer, even in string format, let's say ``2``
        for example, the function will use the command terminal::``python2`` so
        as to launch the ¨python files.

        b) If ``version`` is a string, the function will use it as the command
        so as to launch the ¨python files.

    By default we have ``version = 3`` which indicates that the command to launch
    ¨python is just terminal::``python3``.

    3) ``isverbose`` is a boolean argument to see or not all the stuffs printed
    in the terminal by every single ¨python script launched.

    The default value is ``False`` so as to only see in a terminal the names of
    the ¨python scripts launched.
    """
    if isinstance(version, int) or version.isdigit():
        pycommand = "python{0}".format(version)

    else:
        pycommand = version

    subprocess_method = _SUBPROCESS_METHOD[isverbose]

    for onefile in nextfile(
        main     = main,
        exts     = "py",
        prefixes = prefixes,
        depth    = depth
    ):
        print(
            '\t+ Launching "{0}"'.format(
                relativepath(
                    main = main,
                    sub  = onefile,
                )
            )
        )

        subprocess_method(
# We go in the directory of the file to compile.
            cwd = parentdir(onefile),
# We use the terminal actions.
            args = [pycommand, onefile]
        )
