#!/usr/bin/env python3

"""
prototype::
    date = 2015-06-05    ???

This modules contains some utilities that can be useful for log messages.
"""

# Source used :
#    1) http://agiletesting.blogspot.com/2005/01/python-unit-testing-part-1-unittest.html
#    2) http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
#    3) http://docs.python.org/3.2/library/unittest.html?highlight=unittest.texttestrunner#basic-example

from collections import OrderedDict
from imp import load_source
from inspect import getmembers, isclass
from unittest import makeSuite, TestSuite, TextTestRunner


from mistool.os_use import listfile, name as osuse_name
from mistool.string_use import camelto, frame, FRAMES_FORMATS, replace


# ---------------------- #
# -- LOGGING MESSAGES -- #
# ---------------------- #

# This variable is used to define some formatting rules from one path or one
# name of a function, a method or a class.

ASCII_ASSOS = {
    '_'  : " ",
    '__' : " - ",
    '___': " ---> ",
    '/'  : " : "
}

def what(
    text,
    ismethod = False
):
    """
-----------------
Small description
-----------------

This function transforms some text like ``Abreviations__NewAdding_Good`` into
``Abreviations ---> New Adding - Good`` where the replacements are defined in
the global constant ``ASCII_ASSOS`` which is defined as follows.

python::
    ASCII_ASSOS = {
        '_'  : " ",
        '__' : " - ",
        '___': " ---> ",
        '/'  : " : "
    }


There is a usefull optional argument ``ismethod``. If ``ismethod = True``, then
the text must start with ``test``. If it is the case, this piece of text will be
removed. This is useful because the module ``unittest`` only calls the methods
with a name started by ``test``.


-------------
The arguments
-------------

This function uses two arguments.

    1) ``text`` is a text of something that is tested.

    2) ``ismethod`` is an optional boolean variable. By default, ``ismethod =
    False``.
    """
    if ismethod:
        if not text.startswith('test'):
            raise ValueError('the text does not start with "test".')

        text = text[len('test'):]

    text = camelto(text, "title")

    text = replace(
        text         = text,
        replacements = ASCII_ASSOS
    )

    return text.strip()

def _isdict(obj):
    """
This function returns ``True`` if the argument ``obj`` is a dictionnary (ordered
or not). If this is not the case, the function returns ``False``.
    """
    return isinstance(obj, (dict, OrderedDict))

def diffdict(
    dict_1,
    dict_2,
    dorecursive = False
):
    """
-----------------
Small description
-----------------

This function analyses if the two dictionaries ``dict_1`` and ``dict_2`` are
equal. If it is the case, an empty string is returned. In the other case, a
message indicating briefly the differences between the two dictionaries is
returned.


If you want a more precise message for the differences found, you can use the
optional argument ``dorecursive`` whose default value is ``False``. If
``dorecursive = True``, each time that two differents values are found and are
also two dictionaries, then the function ``diffdict`` will be called recursively
for a finer message indicating the differences.


-------------
The arguments
-------------

This function uses the following variables.

    1) ``dict_1`` and `` dict_2`` are the two dictionaries to analyse.

    2) ``dorecursive`` is a boolean variable to ask to recursively analysed
    different values that are dictionaries. By default, ``dorecursive = False``.
    """
    if not(dict_1 and dict_2):
        text = 'One of the dictionary is empty but not the other.'

    elif sorted(dict_1.keys()) != sorted(dict_2.keys()):
        text = 'The dictionaries have different keys.'

    else:
        text = ''

        for key_1, value_1 in dict_1.items():
            value_2 = dict_2[key_1]

            if value_1 != value_2:
                text = 'The values for the key << {0} >> are different.'.format(
                    repr(key_1)
                )

                if dorecursive \
                and _isdict(value_1) and _isdict(value_2):
                    text += '\n\n>>> RECURSIVE DIFFERENCES <<<\n\n' + diffdict(
                        value_1,
                        value_2,
                        recursive = True
                    )

                break

    return text


# ----------- #
# -- PRINT -- #
# ----------- #

def logprint(text):
    """
-----------------
Small description
-----------------

This function is used to display messages. By default, ``logprint`` is simply
equal to ``print``.


You can redefine this function to change the way the messages are "displayed"
so as to build log files for example.


-------------
The arguments
-------------

This function has only one variable ``text`` which is a string.
    """
    print(text)

def info(
    text,
    kind  = "Testing",
    start = "    + ",
    end   = "..."
):
    """
-----------------
Small description
-----------------

This function is usefull for displaying very short infos in one line.


-------------
The arguments
-------------

This function has four arguments.

    1) ``text`` is the text to display.

    2) ``kind`` is a leading text put just before ``text``. By default, ``kind =
    "Testing"``.

    3) ``start`` and ``end`` are texts put at the start and the end of the text
    ``kind + text``. By default ``start = "    + "``and ``end = "..."``.
    """
    logprint('{0}{1} "{2}"{3}'.format(start, kind, text, end))

FRAME_PROBLEM = FRAMES_FORMATS['unittest_problem']

def problem(
    text,
    format = FRAME_PROBLEM,
    center = True
):
    """
-----------------
Small description
-----------------

This function is useful for displaying problems met during one test.

Indeed this function just displays the text ``frame(text, format,
center)`` (take a look at the documentation of the module ``string_use`` if
you want to use your own format of frame).


-------------
The arguments
-------------

This function uses the following variables.

    1) ``text`` is the text indicating the problem.

    2) ``format`` is the format of the frame following the specifications of the
    function ``frame``. This an optional argument. By default,
    ``format = string_use.FRAMES_FORMATS['unittest_problem']``.

    3) ``center`` is a boolean optional variable which aks to center or not the
    text. By default, ``center = True``.
    """
    logprint(
        frame(
            text,
            format = format,
            center = center
        )
    )


# -------------------- #
# -- SUITE OF TESTS -- #
# -------------------- #

FRAME_LAUNCH_TEST = FRAMES_FORMATS['python_basic']

def runtests(
    dir,
    depth     = 0,
    verbosity = 0,
    message   = "",
    sort      = lambda x: x
):
    """
-----------------
Small description
-----------------

This function simplifies a lot the launching of unit tests made via the module
``unittest``.


See the meaning of the arguments so as to know how to use this function.


-------------
The arguments
-------------

This function uses the following variables.

    1) ``dir`` is the only obligatory argument. It indicates the directory where
    you have put all your files for testing.

    warning::
        You must follow the two simple rules beyond.

            a) All the files where the unit tests are defined must have a name
            starting with ``test_``.

            b) All the class making the unit tests must have a name starting
            with ``Test``.

    2) ``depth`` is an optional argument with default value ``0``. This is to
    indicate the maximal depth for the research of the files to remove.

    The very special value ``(-1)`` indicates that there is no maximum. The
    default value ``0`` asks to only look for in the direct content of the main
    directory to analyse.

    3) ``verbosity`` is an optional argument with default value ``0``. Indeed
    the meaning of this value is the same at its eponym for the class
    ``unittest.TextTestRunner``. See the documentation of ``unitttest``.

    4) ``message`` is an optional argument which is an empty string by default.
    You can use ``message`` if you want to display some text, via the function
    ``logprint``, at the very beginning of the test suite.

    5) ``sort`` is a function used to sort the path of the files doing the
    tests. By default, ``sort = lambda x: x``.
    """
# Let's look for the good Python files.
    testingfiles = listfile(
        main     = dir,
        exts     = "py",
        prefixes = "test_",
        depth    = depth
    )

# Let's sort the paths.
    testingfiles.sort(key = sort)

# Let's look for the testing classes.
    classes = []

    for pyfile in testingfiles:
        test = load_source(
            osuse_name(pyfile),
            pyfile
        )

        for classname, oneclass in getmembers(
            test,
            isclass
        ):
            if classname.startswith('Test'):
                classes.append(oneclass)

# It's time to test.
    if classes:
        suitetests = TestSuite()

        for oneclass in classes:
            suitetests.addTest(makeSuite(oneclass))

        if message:
            logprint(
                "\n" + frame(
                    text   = message,
                    format = FRAME_LAUNCH_TEST
                ) + "\n"
            )

        TextTestRunner(verbosity = verbosity).run(suitetests)

    else:
        logprint('No test has been found...')
