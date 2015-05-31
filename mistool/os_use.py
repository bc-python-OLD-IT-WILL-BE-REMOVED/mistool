#!/usr/bin/env python3

"""
prototype::
    date = 2015-05-31


The main feature of this module is the class ``PPath`` which is an enhanced
version of the standard class ``pathlib.Path`` that allows to manipulate easily
paths and as a consequence files and folders.

There is also a class ``DirView`` so as to display the content of a directory
using filters if necessary, and two functions which give informations about the
system.
"""

import os
import pathlib
import re
import shutil
import platform
from subprocess import check_call

from mistool.latex_use import escape as latex_escape


# ------------------- #
# -- GENERAL INFOS -- #
# ------------------- #

def pathenv():                        # DOC OK !!
    """
prototype::
    return = str ;
             the variable ``PATH`` that contains paths of some executables
             known by your OS
    """
    return os.getenv('ppath')


def system():                        # DOC OK !!
    """
prototype::
    return = str ;
             the name, in lower case, of the OS used (possible names can be
             "windows", "mac", "linux" and also "java")
    """
    osname = platform.system()

    if not osname:
        raise SystemError("the operating sytem can't be found.")

    if osname == 'Darwin':
        return "mac"

    else:
        return osname.lower()


# --------------------------------------------- #
# -- SPECIAL FUNCTIONS FOR THE SPECIAL CLASS -- #
# --------------------------------------------- #

# << Warning ! >>
#
# Sublcassing ``pathlib.Path`` is not easy ! We have to dirty a little our
# hands. Hints are hidden in the source and especially in the code of the class
# ``pathlib.PurePath``.
#
# Sources:
#     * http://stackoverflow.com/a/29851079/4589608
#     * https://hg.python.org/cpython/file/151cab576cab/Lib/pathlib.py
#
# Extra methods added to ``PPath`` must be defined using functions. We choose to
# use names which all llok like ``_ppath_somename`` where ``somename`` will be
# the name used in the class ``PPath``.


# ----------- #
# -- ABOUT -- #
# ----------- #

@property
def _ppath_parent(cls):                     # DOC OK !!
    """
prototype::
    type   = property ;
             a hack is used so as to transform this function into a property
             method ``parent`` of the class ``PPath`` (uggly but functional)
    see    = PPath
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``parent`` of the class ``PPath``
    return = PPath ;
             a new path corresponding to the first "parent folder" of the
             current path


Here is an example made using a ¨mac. The ``PosixPath`` refers to the Unix
version of ``PPath``.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path = PPath("dir/subdir/file.txt")
    >>> path.parent
    PosixPath('dir/subdir')
    """
    return cls.parents[0]


@property
def _ppath_ext(cls):                        # DOC OK !!
    """
prototype::
    type   = property ;
             a hack is used so as to transform this function into a property
             method ``ext`` of the class ``PPath`` (uggly but functional)
    see    = PPath
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``ext`` of the class ``PPath``
    return = str ;
             the extension of the path


Here is a small example of use where you can see that the attribut ``ext`` is
just the value of the attribut ``suffix``, from ``pathlib.Path``, but without
the leading point.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path = PPath("dir/subdir/file.txt")
    >>> print(path.ext)
    'txt'
    >>> print(path.suffix)
    '.txt'
    """
# An extension is a suffix without the leading point.
    return cls.suffix[1:]


def _ppath_with_ext(cls, ext):              # DOC OK !!
    """
prototype::
    type   = method ;
             a hack is used so as to transform this function into a method
             ``with_ext`` of the class ``PPath`` (uggly but functional)
    see    = PPath
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``with_ext`` of the class ``PPath``
    arg    = str: ext ;
             value of the extension
    return = PPath ;
             a new path obtained from the current path by adding or changing
             the extension using the value of ``ext``


Here is ane example made using a ¨mac. The ``PosixPath`` refers to the Unix
version of ``PPath``.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path = PPath("dir/subdir")
    >>> path.with_ext("ext")
    PosixPath('dir/subdir.ext')
    >>> path = PPath("dir/subdir/file.txt")
    >>> path.with_ext("ext")
    PosixPath('dir/subdir/file.ext')
    """
    if ext:
        ext = "." + ext

    return cls.with_suffix(ext)


# ----------------------- #
# -- FORMATTING A PATH -- #
# ----------------------- #

@property
def _ppath_normpath(cls):                   # DOC OK !!
    """
prototype::
    type   = property ;
             a hack is used so as to transform this function into a property
             method ``normpath`` of the class ``PPath`` (uggly but functional)
    see    = PPath
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``normpath`` of the class ``PPath``
    return = PPath ;
             a new path obtained from the current path by interpreting the
             leading shortcut path::``~``, and the shortcuts path::``/../``
             used to go higher in the tree structure


Here is an example made on the ¨mac of the author of ¨mistool where the user's
folder is path::``/Users/projetmbc``. The ``PosixPath`` refers to the Unix
version of ``PPath``.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path = PPath("~/dir_1/dir_2/dir_3/../../file.txt")
    >>> path.normpath
    PosixPath('/Users/projetmbc/dir_1/file.txt')
    """
    return PPath(
        os.path.normpath(
            os.path.expanduser(str(cls))
        )
    )


@property
def _ppath_shortpath(cls):                  # DOC OK !!
    """
prototype::
    type   = property ;
             a hack is used so as to transform this function into a property
             method ``shortpath`` of the class ``PPath`` (uggly but functional)
    see    = PPath
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``shortpath`` of the class ``PPath``
    return = PPath ;
             a new path obtained from the current path by trying to use the
             leading shortcut path::``~``, and by intepreting the shortcuts
             path::``/../`` used to go higher in the tree structure


Here is an example made on the Mac of the author of ¨mistool. In that case
path::``/Users/projetmbc`` is the user's folder. The ``PosixPath`` refers to
the Unix version of ``PPath``.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path = PPath("/Users/projetmbc/dir_1/dir_2/dir_3/../../file.txt")
    >>> path.shortpath
    PosixPath('~/dir_1/file.txt')
    """
    path     = os.path.normpath(os.path.expanduser(str(cls)))
    userpath = os.path.expanduser("~") + cls._flavour.sep

    if path.startswith(userpath):
        path = "~" + cls._flavour.sep + path[len(userpath):]

    return PPath(path)


# --------------------- #
# -- COMPARING PATHS -- #
# --------------------- #

def _ppath_common_with(cls, *args):         # DOC OK !!
    """
prototype::
    type   = method ;
             a hack is used so as to transform this function into a method
             ``common_with`` of the class ``PPath`` (uggly but functional)
    see    = PPath , _ppath___and__
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``common_with`` of the class ``PPath``
    args   = PPath ;
             the arguments can be given separated by comas, or in list, or in
             a tuple
    return = PPath ;
             a new path which corresponds to the "smaller common folder" of
             the current path and the other ones given in arguments


In the following example, the two last calls to ``common_with`` show that you
can either use a list or a tuple of paths, or instead several arguments for the
different paths.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path        = PPath("/Users/projects/source/doc")
    >>> path_1      = PPath("/Users/projects/README")
    >>> path_2      = PPath("/Users/projects/source/misTool/os_use.py")
    >>> path_danger = PPath("/NoUser/projects")
    >>> path.common_with(path_1)
    PosixPath('/Users/projects')
    >>> path.common_with(path_2)
    PosixPath('/Users/projects/source')
    >>> path.common_with(path_danger)
    PosixPath('/')
    >>> path.common_with(path_1, path_2)
    PosixPath('/Users/projects')
    >>> path.common_with([path_1, path_2])
    PosixPath('/Users/projects')


You can also use the magic method ``&`` as a shortcut to ``common_with``. Some
of the preceding examples becomes then the following ones.

pyterm::
    >>> path & path_1
    PosixPath('/Users/projects')
    >>> path & path_1 & path_2
    PosixPath('/Users/projects')
    >>> path & [path_1, path_2]
    PosixPath('/Users/projects')


info::
    The use of ``&`` was inspired by the analogy between the logical "AND" and
    the intersection of sets.
    """
    commonparts = list(cls.parts)

    paths = []

    for onearg in args:
        if isinstance(onearg, list):
            paths += onearg

        elif isinstance(onearg, tuple):
            paths += list(onearg)

        else:
            paths.append(onearg)

    for path in paths:
        i = 0

        for common, current in zip(commonparts, path.parts):
            if common == current:
                i += 1
            else:
                break

        commonparts = commonparts[:i]

        if not commonparts:
            break

    commonpath = pathlib.Path("")

    for part in commonparts:
        commonpath /= part

    return commonpath


def _ppath___and__(cls, paths):             # DOC OK !!
    """
prototype::
    type   = method ;
             a hack is used so as to transform this function into the magic
             method ``__and__`` of the class ``PPath`` (uggly but functional)
    see    = PPath , _ppath_common_with
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             magic method ``__and__`` of the class ``PPath``
    arg    = PPath | list(PPath) | tuple(PPath): paths
    return = PPath ;
             a new path which corresponds to the "smaller common folder" of
             the current path and the other ones given in arguments


This magic method allows to use ``path & paths`` instead of the long version
``path.common_with(paths)`` where ``paths`` can be either a single path, or
a list or a tuple of paths.
    """
    return cls.common_with(paths)


def _ppath___sub__(cls, path):              # DOC OK !!
    """
prototype::
    type   = method ;
             a hack is used so as to transform this function into the magic
             method ``__sub__`` of the class ``PPath`` (uggly but functional)
    see    = PPath , relative_to (pathlib.Path)
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             magic method ``__sub__`` of the class ``PPath``
    arg    = PPath: path
    return = PPath ;
             a new path which corresponds to the relative path of the current
             one regarding to the path given in the argument ``path``


This magic method allows to use ``path - anotherpath`` instead of the long
version ``path.relative_to(anotherpath)`` given by ``pathlib.Path``.
    """
    return cls.relative_to(path)


def _ppath_depth_in(cls, path):             # DOC OK !!
    """
prototype::
    type   = method ;
             a hack is used so as to transform this function into a method
             ``depth_in`` of the class ``PPath`` (uggly but functional)
    see    = PPath
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``depth_in`` of the class ``PPath``
    arg    = PPath: path
    return = PPath ;
             the depth of the current path regarding to the one given in the
             argument ``path``


Here are some examples of use.

pyterm::
    >>> from mistool.os_use import PPath
    >>> main    = PPath("/Users/projects")
    >>> path_1  = PPath("/Users/projects/README")
    >>> path_2  = PPath("/Users/projects/source/misTool/os_use.py")
    >>> path_pb = PPath("/NoUser/projects")
    >>> print(path_1.depth_in(main))
    0
    >>> print(path_2.depth_in(main))
    2
    >>> print(path_pb.depth_in(main))
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/anaconda/lib/python3.4/pathlib.py", line 802, in relative_to
        .format(str(self), str(formatted)))
    ValueError: '/NoUser/projects' does not start with '/Users/projects'
    """
    return len(cls.relative_to(path).parts) - 1


@property
def _ppath_depth(cls):                  # DOC OK !!
    """
prototype::
    type   = property ;
             a hack is used so as to transform this function into a property
             method ``depth`` of the class ``PPath`` (uggly but functional)
    see    = PPath
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``parent`` of the class ``PPath``
    return = int ;
             the absolute depth of a path


Here is an example of use.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path = PPath("/Users/projects/source/misTool/os_use.py")
    >>> print(path.depth)
    4
    """
    return len(cls.parents) - 1


# -------------- #
# -- REGPATHS -- #
# -------------- #

# Sources for the regex:
#
#     * http://stackoverflow.com/a/430781/4589608
#     * http://stackoverflow.com/a/30439865/4589608
#     * http://stackoverflow.com/a/817117/4589608
#     * http://stackoverflow.com/questions/20294704/which-pattern-has-been-found/20294987

_ALL, _DIR, _ELLIPSIS, _FILE, _RELSEARCH \
= "all", "dir", "ellipsis", "file", "relative"

_PATH_QUERIES      = set([_ALL, _DIR, _ELLIPSIS, _FILE, _RELSEARCH])
_LONG_PATH_QUERIES = {x[0]: x for x in _PATH_QUERIES}
_FILE_DIR_QUERIES  = set([_DIR, _FILE])
_ALL_QUERY         = set([_ALL])

_RE_SPECIAL_CHARS = pattern = re.compile(
    r"(?<!\\)((?:\\\\)*)((\*+)|(@)|(×)|(\.))"
)

_REPLACEMENTS = {
    '**': ".+",
    '.' : r"\.",
    '@' : ".",
    '×' : "*",
}

_SPE_CHARS = list(_REPLACEMENTS) + ["*"]

_REPLACEMENTS['\\'] = "[^\\]+"
_REPLACEMENTS['/']  = "[^/]+"


def _ppath_regexit(cls, pattern):      # DOC OK !!
    """
prototype::
    type   = method ;
             a hack is used so as to transform this function into a method
             ``regexit`` of the class ``PPath`` (uggly but functional)
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``regpath2meta`` of the class ``PPath``
    arg    = str: pattern ;
             ``pattern`` is a pattern using the regpath syntax which tries to
             catch the best of the regex and the Unix-glob syntaxes (no special
             queries here)
    return = str ;
             a regex uncompiled version of ``pattern``.
    """
    onestar2regex = _REPLACEMENTS[cls._flavour.sep]

    newpattern = ""
    lastpos    = 0

    for m in _RE_SPECIAL_CHARS.finditer(pattern):
        spechar = m.group()

        if spechar not in _SPE_CHARS:
            raise ValueError("too much consecutive stars ''*''")

        spechar     = _REPLACEMENTS.get(spechar, onestar2regex)
        newpattern += pattern[lastpos:m.start()] + spechar
        lastpos     = m.end()

    newpattern += pattern[lastpos:]

    return newpattern


def _ppath_regpath2meta(cls, regpath, regexit = True):      # DOC OK !!
    """
prototype::
    type   = method ;
             a hack is used so as to transform this function into a method
             ``regpath2meta`` of the class ``PPath`` (uggly but functional)
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``regpath2meta`` of the class ``PPath``
    arg    = str: regpath ;
             ``regpath`` uses a syntax trying to catch the best of the regex and
             the Unix-glob syntaxes with some little extra features
    arg    = bool: regexit = True ;
             ``regexit`` allows to have the regex version of ``regpath``
    return = tuple(set(str): queries, str: pattern) ;
             ``queries`` give extra infos about the kind of objects to "search",
             and ``pattern`` is a "searching pattern" which is in regex
             uncompiled version if ``regexit = True``.


=====================
What is a "regpath" ?
=====================

A "regpath" allows to use all the power of regexes with the easy to use special
characters of the Unix-glob syntax, and it offers also some additional query
features.

The syntax can be either "regex_glob_part" or "query_part::regex_glob_part"
where "query_part" and "regex_glob_part" must follow some rules explained in
the following sections.


Here are some exemples on a ¨unix system.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path = PPath("")

    >>> print(path.regpath2meta("*.(py|txt)"))
    ({'dir', 'file'}, '[^/]+\\.(py|txt)')

    >>> print(path.regpath2meta("*.(py|txt)", regexit = False))
    ({'dir', 'file'}, '*.(py|txt)')

    >>> print(path.regpath2meta("all file::**.py"))
    ({'all', 'file'}, '.+\\.py')


In the outputs printed, `{'dir', 'file'}` indicates to look only for visible
files and directories, whereas `{'all', 'file'}` asks to keep also invisible
files, i.e. files having a name starting with a point.


=================================
The regex and Unix-glob like part
=================================

Here are the only differences between the syntax for ``regpath``, the Unix-glob
syntax and the traditional regexes.

    1) ``*`` indicates one ore more characters except the separator of the OS.
    This corresponds to the regex regex::``[^\\]+`` or regex::``[^/]+``
    regarding to the OS is Windows or Unix.

    2) ``**`` indicates one ore more characters even the separator of the OS.
    This corresponds to the regex regex::``.+``.

    3) ``.`` is not a special character, this is just a point. This corresponds
    to regex::``\.`` in regexes.

    4) The multiplication symbol ``×`` is the equivalent of regex::``*`` in
    regexes. This allows to indicate zero or more repetitions.

    5) ``@`` is the equivalent of regex::``.`` in regexes. This allows to
    indicate any single character except a newline.

    6) ``\`` is an escaping for special character. For example, you have to use
    a double backslash ``\\`` to indicate the Windows separator ``\``.


With this syntax you can do easily things like indicated a file or a directory
not in a folder and also tahs ends with either path::``.py`` or path::``.txt``.
To do that, just use the pattern ``*.(py|txt)``.

The regex version of this pattern is regex::``[^\\]+\.(py|txt)`` for a ¨unix
¨os. This is a little less user friendly as you can see.


==============
The query part
==============

Before two double points, you can use the following queries that will be used
by the method ``walk``.

    a) ``file`` asks to keep only files. You can use the shortcut ``f``.

    b) ``dir`` asks to keep only folders. You can use the shortcut ``d``.

    c) ``all`` asks to keep also the unvisible files and folders. This ones
    have a name begining with ``.``.

    d) ``all file`` and ``all dir`` ask to respectively keep only visible
    files, or only visible directories.

    e) ``relative`` indicates that the pattern is relatively to the current
    directory and not to a full path.

    f) ``ellipsis`` add respectively special names path::``::...files...::``
    and path::``::...empty...::`` whenever some files have been found but not
    kept or a folder is empty (this feature is used by the class ``DirView``).


For example, to keep only the Python files, in a folder or not, just use
``"file::**.py"``. This is not the same that ``"**.py"`` which will also catch
folders with a name finishing by path::``.py`` (that is legal).


info::
    For each query, you can only use the initial letter of the query. For
    example, ``f`` is a shortcut for ``file``, and ``a-f`` is the same that
    ``all-file``.
    """
    queries, *pattern = regpath.split("::")

    if len(pattern) > 1:
        raise ValueError("too much \"::\" in the regpath.")

# Two pieces
    if pattern:
        pattern = pattern[0]

        queries = set(
            _LONG_PATH_QUERIES.get(x.strip(), x.strip())
            for x in queries.split(" ")
        )

        if not queries <= _PATH_QUERIES:
            raise ValueError("illegal filter in the regpath.")

# One single piece
    else:
        queries, pattern = _FILE_DIR_QUERIES, queries

# The qeries "file" and "dir" are not used.
    if _FILE not in queries and _DIR not in queries:
        queries |= _FILE_DIR_QUERIES

# The regex uncompiled version : we just do replacing by taking care of
# the escaping character. We play with regexes to do that.
#
# << Warning : >> ***, ****, ... are not allowed !

    if regexit:
        pattern = cls.regexit(pattern)

    return queries, pattern


# ------------------ #
# -- WALK AND SEE -- #
# ------------------ #

OTHER_FILES     = "::...files...::"
EMPTY_OTHER_DIR = "::...empty...::"

_ELLIPSIS_NAMES = [EMPTY_OTHER_DIR, OTHER_FILES]

def _ppath_walk(cls, regpath = "relative::**"):               # DOC OK !!
    """
prototype::
    type  = method ;
            a hack is used so as to transform this function into a method
            ``depth_in`` of the class ``PPath`` (uggly but functional)
    see   = PPath , _ppath_regpath2meta
    arg   = PPath: cls ;
            this argument nearly refers to the ``self`` used by the associated
            method ``depth_in`` of the class ``PPath``
    arg   = str: regpath = "relative::**" ;
            this is a string that follows some rules named regpath rules (see
            the documentation of the function ``_ppath_regpath2meta``)
    yield = PPath ;
            files and subdirectories matching ``regpath`` are yield (for each
            folder, the files are yield before the subdirectories)


Let's suppose that we have the following directory having the full path
path::``/Users/projects/dir`` in a ¨unix system.

dir::
    + dir
        * code_1.py
        * code_2.py
        * file_1.txt
        * file_2.txt
        + emptydir
        + subdir
            * slide_A.pdf
            * slide_B.pdf
            * subcode_A.py
            * subcode_B.py
            + subsubdir
                * doc.pdf

Here are three examples of use where you can see that the repaths ``"*"`` and
``"**"`` don't do the same thing : there are two much files with ``"**"``. Just
go to the documentation of the function ``_ppath_regpath2meta`` so as to know
why (you have to remember that by default the search is relative).

pyterm::
    >>> from mistool.os_use import PPath
    >>> folder = PPath("/Users/projects/dir")
    >>> for p in folder.walk("dir::**"):
    ...     print("+", p)
    ...
    + emptydir
    + subdir
    + subdir/subsubdir
    >>> for p in folder.walk("**.py"):
    ...     print("+", p)
    ...
    + /Users/projects/dir/code_1.py
    + /Users/projects/dir/code_2.py
    + /Users/projects/dir/subdir/code_A.py
    + /Users/projects/dir/subdir/code_B.py
    >>> for p in folder.walk("relative file::*.py"):
    ...     print("+", p)
    ...
    + /Users/projects/dir/code_1.py
    + /Users/projects/dir/code_2.py


If you want to see the existing files that do not match the regpath and also
the empty folders, you will have to the query ``ellipsis`` (this feature is
used  by the class ``DirView``).
In the example above, that uses the same directory as before, you can see that
there are special names ``::...files...::`` and ``::...empty...::`` which
indicate the extra informations.


pyterm::
    >>> from mistool.os_use import PPath
    >>> folder = PPath("/Users/projects/dir")
    >>> for p in folder.walk("ellipsis file::**.py"):
    ...     print("+", p)
    ...
    + /Users/projects/dir/code_1.py
    + /Users/projects/dir/code_2.py
    + /Users/projects/dir/::...files...::
    + /Users/projects/dir/emptydir/::...empty...::
    + /Users/projects/dir/subdir/subcode_A.py
    + /Users/projects/dir/subdir/subcode_B.py
    + /Users/projects/dir/subdir/::...files...::
    + /Users/projects/dir/subdir/subsubdir/::...files...::


info::
    The special names are stored in the global variables ``OTHER_FILES`` and
    ``EMPTY_OTHER_DIR`` which are strings. This can be useful to avoid mistypings
    if you want to use the query ``ellipsis``.
    """
# Do we have an existing directory ?
    if not cls.is_dir():
        raise OSError("the path doesn't point to a directory.")

# metadatas and the normal regex
    queries, pattern = cls.regpath2meta(regpath)

    maindir     = str(cls)
    keepdir     = _DIR in queries
    keepfile    = _FILE in queries
    keepall     = _ALL in queries
    relsearch   = _RELSEARCH in queries
    addellipsis = _ELLIPSIS in queries

    regex_obj = re.compile("^{0}$".format(pattern))

# Let's walk
    for root, dirs, files in os.walk(str(cls)):
# Empty folders and unkept files
        isdirempty       = not(bool(dirs) or bool(files))
        unkeptfilesfound = False

# Do the current directory must be added ?
        addthisdir = False
        root_ppath = PPath(root)

        if keepdir \
        and root != maindir \
        and regex_obj.match(root):
            if keepall \
            or not any(
                x.startswith('.')
                for x in root_ppath.relative_to(cls).parts
            ):
                addthisdir = True

# A new file ?
        if keepfile:
            for file in files:
                if not keepall and file.startswith('.'):
                    continue

                full_file = os.path.join(root, file)

                if relsearch:
                    ppath_full_file = PPath(full_file)
                    rel_file = str(ppath_full_file.relative_to(cls))

                    if regex_obj.match(rel_file):
                        yield ppath_full_file

                    else:
                        unkeptfilesfound = True

                elif regex_obj.match(full_file):
                    yield PPath(full_file)

                else:
                    unkeptfilesfound = True

# A new directory ?
        if addthisdir:
            yield root_ppath

        elif addellipsis:
            if isdirempty:
                yield root_ppath / PPath(EMPTY_OTHER_DIR)

            elif unkeptfilesfound:
                yield root_ppath / PPath(OTHER_FILES)


def _ppath_see(cls):                        # DOC OK !!
    """
prototype::
    type   = method ;
             a hack is used so as to transform this function into a method
             ``see`` of the class ``PPath`` (uggly but functional)
    see    = PPath
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``see`` of the class ``PPath``
    action = this method shows one directory or one file in the OS environment
             by trying to call an associated application
    """
# Nothing to open...
    if not cls.is_file() and not cls.is_dir():
        raise OSError("the path points nowhere.")

# We need the **string** long normalized version of the path.
    strpath = str(cls.normpath)

# Each OS has its own method.
    osname = system()

# Windows
    if osname == "windows":
        if cls.is_file():
            os.startfile(strpath)
        else:
            check_call(args = ['explorer', strpath])

# Mac
    elif osname == "mac":
        check_call(args = ['open', strpath])

# Linux
#
# Source :
#     * http://forum.ubuntu-fr.org/viewtopic.php?pid=3952590#p3952590
    elif osname == "linux":
        check_call(args = ['xdg-open', strpath])

# Unknown method...
    else:
        raise OSError(
            "the opening of the file in the OS "
            "<< {0} >> is not supported.".format(osname)
        )


# ------------ #
# -- CREATE -- #
# ------------ #

_ALL_CREATE_KINDS  = set([_FILE, _DIR])
_LONG_CREATE_KINDS = {x[0]: x for x in _ALL_CREATE_KINDS}

def _ppath_create(cls, kind):               # DOC OK !!
    """
prototype::
    type   = method ;
             a hack is used so as to transform this function into a method
             ``create`` of the class ``PPath`` (uggly but functional)
    see    = PPath
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``create`` of the class ``PPath``
    arg    = str: kind in _FILE, _DIR
    action = this method creates the file or the directory having the current
             path except if this path points to an existing directory or file
             respectively.


Here is an example of creations relatively to a current directory having path
path::``/Users/projetmbc``. You can see that some exceptions can be raised.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path_1 = PPath("test/README")
    >>> path.is_file()
    False
    >>> path_1.create("file")
    >>> path.is_file()
    True
    >>> path_2 = PPath("test/README")
    >>> path_2.create("dir")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/anaconda/lib/python3.4/site-packages/mistool/os_use.py", line 330, in _ppath_create
        raise ValueError("path points to an existing file.")
    ValueError: path points to an existing file.


info::
    All the parent directories that don't yet exist are automatically created.
    """
# Good kind.
    kind = _LONG_CREATE_KINDS.get(kind, kind)

    if kind not in _ALL_CREATE_KINDS:
        raise ValueError("illegal kind.")

# A new directory.
    if kind == _DIR:
        if cls.is_file():
            raise ValueError("path points to an existing file.")

        elif not cls.is_dir():
            os.makedirs(str(cls))

# A new file.
    elif cls.is_dir():
        raise ValueError("path points to an existing directory.")

    elif not cls.is_file():
        cls.parent().create(_DIR)

        with cls.open(mode = "w") as file:
            ...


# ------------ #
# -- REMOVE -- #
# ------------ #

def _ppath_remove(cls):                     # DOC OK !!
    """
prototype::
    type   = method ;
             a hack is used so as to transform this function into a method
             ``create`` of the class ``PPath`` (uggly but functional)
    see    = PPath
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``create`` of the class ``PPath``
    action = this method removes the directory or the file corresponding to
             the current path


warning::
    Removing a directory will destroy anything within it using a recursive
    destruction of all subfolders and subfiles.
    """
    if cls.is_dir():
        shutil.rmtree(str(cls))

    elif cls.is_file():
        os.remove(str(cls))

    else:
        raise OSError("path points nowhere.")


def _ppath_clean(cls, regpath):                         # DOC OK !!
    """
prototype::
    type   = method ;
             a hack is used so as to transform this function into a method
             ``depth_in`` of the class ``PPath`` (uggly but functional)
    see    = PPath , _ppath_regpath2meta , _ppath_walk
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``depth_in`` of the class ``PPath``
    arg    = str: regpath ;
             this is a string that follows some rules named regpath rules (see
             the documentation of the function ``_ppath_regpath2meta``)
    action = every files and directories matching ``regpath`` are removed
    """
# We have to play with the queries and the pattern in ``regpath``.
    queries, pattern = cls.regpath2meta(regpath, regexit = False)

    if _ALL in queries:
        prefix = "all-"

    else:
        prefix = ""

# We must first remove the files. This is in case of folders to destroy.
    if _FILE in queries:
        filepattern = "{0}file::{1}".format(prefix, pattern)

        for path in cls.walk(filepattern):
            path.remove()

# Now, we can destroy folders but we can use an iterator (because of sub
# directories).
    if _DIR in queries:
        dirpattern = "{0}dir::{1}".format(prefix, pattern)

        sortedpaths = sorted(list(p for p in cls.walk(dirpattern)))

        for path in sortedpaths:
            path.remove()


# ----------------- #
# -- MOVE & COPY -- #
# ----------------- #

def _ppath_copy_to(cls, path):              # DOC OK !!
    """
prototype::
    type   = method ;
             a hack is used so as to transform this function into a method
             ``create`` of the class ``PPath`` (uggly but functional)
    see    = PPath
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``create`` of the class ``PPath``
    arg    = PPath: path
    action = this method copies the current file to the destination given by
             the argument ``path``


warning::
    The current path is not changed and the copy of a directory is not yet
    supported.
    """
    if cls.is_file():
        parent = path.parent

        if not parent.is_dir():
            parent.create(_DIR)

        shutil.copy(str(cls), str(path))

    elif cls.is_dir():
        raise ValueError("copying a directory is not yet supported.")

    else:
        raise OSError("path points nowhere.")


def _ppath_move_to(cls, path):              # DOC OK !!
    """
prototype::
    type   = method ;
             a hack is used so as to transform this function into a method
             ``create`` of the class ``PPath`` (uggly but functional)
    see    = PPath
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``create`` of the class ``PPath``
    arg    = PPath: path
    action = this method moves the current file to the destination given by
             the argument ``path``


info::
    If the source and the destination have the same parent directory, then the
    final result will be at the end a renaming of the file or the directory.


warning::
    The current path is not changed and moving a directory is not yet supported.
    """
    if cls.is_file():
        cls.copy_to(path)

# Let's be cautious...
        if path.is_file():
            cls.remove()

        else:
            raise OSError("moving the file has failed.")

    elif cls.is_dir():
        raise ValueError("moving directories is not yet supported.")

    else:
        raise OSError("current path points nowhere.")


# ------------------------ #
# -- OUR ENHANCED CLASS -- #
# ------------------------ #

_SPECIAL_FUNCS = [
    (x[len("_ppath_"):], x)
    for x in dir()
    if x.startswith("_ppath_")
]

class PPath(pathlib.Path):          # DOC OK !!
    """
prototype::
    type = cls ;
           a hack is used so as to mimic subclassing of the standard class
           ``pathlib.Path``
    see  = pathlib.Path
    """

    def __new__(cls, *args):
        if cls is PPath:
            cls = pathlib.WindowsPath if os.name == 'nt' else pathlib.PosixPath

# We have to add our additional methods using a short dirty way.
        for specialname, specialfunc in _SPECIAL_FUNCS:
            setattr(cls, specialname, globals()[specialfunc])

        return cls._from_parts(args)


# ----------------------- #
# -- VIEWS OF A FOLDER -- #
# ----------------------- #

class DirView:                      # DOC OK !!
    r"""
prototype::
    type = cls ;
           this class allows to display in different formats the tree
           structure of one directory with the extra possibility to keep and
           show only some informations, and also to set a little the format of
           the output
    see  = _ppath_regpath2meta, _ppath_walk

    arg  = PPath: ppath ;
           this argument is the path of the directory to analyze
    arg  = str: regpath = "**" ;
           this argument follows some rules named "regpath" rules (see the
           documentation of ``_ppath_regpath2meta``)
    arg  = str: display = "main short" in self._FORMATS;
           this argument gives informations about the output to produce (you
           can just use the initials of the options)
    arg  = str: sorting = "alpha" in [x[0] for x in cls.LAMBDA_SORT]
                                  or in [x[1] for x in cls.LAMBDA_SORT];
           this argument inidcates the way to sort the paths found

    clsattr = dict((str, str): (lambda, x)): LAMBDA_SORT ;
              this attribut of class, and not of one of its instance, defines
              how to sort the paths (see the end of the documentation above)


===================================
The directory used for the examples
===================================

All of the following examples will use a folder with the structure above and
having the whole path path::``/Users/projetmbc/dir``.

dir::
    + dir
        * code_1.py
        * code_2.py
        * file_1.txt
        * file_2.txt
        + emptydir
        + subdir
            * slide_A.pdf
            * slide_B.pdf
            * subcode_A.py
            * subcode_B.py
            + subsubdir
                * doc.pdf


==============
The ascii tree
==============

Let's start with the default output for the ¨ascii tree. Here is a code to be
launched in the terminal.

python::
    from mistool import os_use

    DirView = os_use.DirView("/Users/projetmbc/dir")

    print(DirView.ascii)


This code will print the following text (indeed this is the syntax used to
generate the documentation that you are reading). You can see that files and
folders are sorting regarding their names.

term::
    + dir
        * code_1.py
        * code_2.py
        + doc
            * code_A.py
            * code_B.py
            + licence
                * doc.pdf
            * slide_A.pdf
            * slide_B.pdf
        + emptydir
        * file_1.txt
        * file_2.txt


You can ask to have the files before the folders and also to have the relative
paths instead of the names. This needs to use the arguments ``display`` and
``sorting``. We have to add the option ``"main"`` for ``display`` if we also
want to see the main folder.

python::
    from mistool import os_use

    DirView = os_use.DirView(
        path    = "/Users/projetmbc/dir",
        display = "main relative",
        sorting = "filefirst"
    )

    print(DirView.ascii)


This will give the following output that is what we are looking for.

term::
    + dir
        * code_1.py
        * code_2.py
        * file_1.txt
        * file_2.txt
        + doc
            * doc/code_A.py
            * doc/code_B.py
            * doc/slide_A.pdf
            * doc/slide_B.pdf
            + doc/licence
                * doc/licence/doc.pdf
        + emptydir


info::
    All the available formattings are given later in this section of the
    documentation.


Let's see a last example using the argument ``regpath``. The following code
asks to keep only the files with the extension path::``py``, and also to
display the names of the files and the folders, see ``"short"``.

python::
    from mistool import os_use

    DirView = os_use.DirView(
        path    = "/Users/projetmbc/dir",
        regpath = "f::**.py",
        display = "main short",
    )

    print(DirView.ascii)


Here is the output given by the class ``DirView``. You can see that the empty
files are given, and that the other files than the ones wanted are indicated
by ellipisis, this ellipsis being always sorted at the end of the files.

term::
    + dir
        * code_1.py
        * code_2.py
        * ...
        + doc
            * code_A.py
            * code_B.py
            * ...
            + licence
                * ...
        + emptydir


If you use instead the option ``display = "main short found"``, then the
output will only show the files found as above, and the empty folders are not
given.

term::
    + dir
        * code_1.py
        * code_2.py
        + doc
            * code_A.py
            * code_B.py


info::
    The documentation of the function ``_ppath_regpath2meta`` gives all the
    ¨infos needed to use the regpaths.


=======================
The "ruled" tree output
=======================

By default, ``DirView.tree`` give a tree view using rules similar to the ones
you can see in ¨gui applications displaying tree structure of a folder (we
can't reproduce the output here because of font problems).


=====================
The "toc" like output
=====================

Using ``DirView.toc`` with the sorting option ``sorting = "namefilefirst"``,
this is the better sorting option here, you will obtain the following output
which looks like a kind of table of contents with sections for folders, and
subsections for files.

term::
    + dir
        * code_1.py
        * code_2.py
        * file_1.txt
        * file_2.txt

    + dir/doc
        * code_A.py
        * code_B.py

    + dir/doc/licence
        * doc.pdf
        * slide_A.pdf
        * slide_B.pdf

    + dir/emptydir


warning::
    Here all the paths for the folders will be always displayed as relative
    ones to the parent directory of the folder analyzed, and not to the folder
    analyzed.


===================================================
A ¨latex version for the package latex::``dirtree``
===================================================

By default, using ``DirView.latex`` you will have the following ¨latex code
than can be formated by the ¨latex package latex::``dirtree``.

latex::
    \dirtree{%
      .1 {dir}.
        .2 {code\_1.py}.
        .2 {code\_2.py}.
        .2 {doc}.
          .3 {code\_A.py}.
          .3 {code\_B.py}.
          .3 {licence}.
            .4 {doc.pdf}.
          .3 {slide\_A.pdf}.
          .3 {slide\_B.pdf}.
        .2 {emptydir}.
        .2 {file\_1.txt}.
        .2 {file\_2.txt}.
    }


info::
    As you can see, special ¨latex characters are managed by the class
    ``DirView``. In our example, ``_`` becomes latex::``\_``.


=======================
All the display options
=======================

The optional string argument ``display`` uses the following rules.

    a) ``long`` or ``l`` asks to display the whole paths of the files and
    directories found.

    b) ``relative`` or ``r`` asks to display relative paths comparing to the
    main directory analysed.

    c) ``short`` or ``s`` asks to only display names of directories found, and
    of the files found with their extensions.

    d) ``main`` or ``m`` asks to display the main directory which is analyzed.

    e) ``found`` or ``f`` asks to only display directories and files with a
    path matching the pattern ``regpath``, and to not give the empty
    directories.
    If this value is not given, then ellipsis will be used to indicate
    unmatching files and the empty directory will be always given.


=======================
All the sorting options
=======================

The optional string argument ``sorting`` can have one of the following values.

    a) ``alpha`` or ``a`` is the alphabetic sorting on the strings representing
    the paths.

    b) ``filefirst`` or ``f`` gathers first the files and then the folders,
    and in each of this category an alphabetic sorting is applied.

    c) ``namefilefirst`` or ``nf`` first sorts the objects regarding their
    name without the extension, and if a file and a folder have the same
    position, then the file will be put before the directory.

    d) ``date`` or ``d`` simply used the date of the last physical changes.


info::
    For all the options above, the unmatching files indicated with "..." are
    always sorted at the end.


info::
    You can add sortings by redefining the attribut of class ``LAMBDA_SORT``
    which by default is the following dictionary.

    python::
        LAMBDA_SORT = {
            ("alpha", "a"): [
                lambda x: str(x['ppath']),
                'z'*500
            ],
            ("namefilefirst", "nf"): [
                lambda x: (
                    str(x['ppath'].stem),
                    int("dir" in x['kind'])
                ),
                ('z'*500, 0)
            ],
            ("filefirst", "f"): [
                lambda x: (
                    int("dir" in x['kind']),
                    str(x['ppath'])
                ),
                (0, 'z'*500)
            ],
            ("date", "d"): [
                lambda x: -x['ppath'].stat().st_mtime,
                float('inf')
            ],
        }

     This dictionary uses the following conventions.

        1) The keys are tuples ``(longname, shortname)`` of two strings.

        2) The values are lists of two elements.

            a) The ¨1ST element is a lambda function that will do the sorting.
            Here ``x`` is a dictionary stored in ``self.listview`` (see the
            documentation of the method ``self.build``).

            b) The ¨2ND element is the alias to use instead of the ellipsis
            ``"..."`` to sort this kind of special paths.
    """
    FILE_KINDS = ['file', 'other_files']
    DIR_KINDS  = ['dir', 'content_dir', 'empty_dir']

    ASCII_DECOS = {
        k: v
        for v, keys in {
            "+"  : DIR_KINDS,
            "*"  : FILE_KINDS,
            " "*4: ['tab'],
        }.items()
        for k in keys
    }

# Source for the rules:
#     * http://en.wikipedia.org/wiki/Box-drawing_character#Unicode

    UTF8_DECOS = {
# Horizontal and vertical rules
        'hrule': "\u2501", #--->  ━
        'vrule': "\u2503", #--->  ┃
# First, last, horizontal and vertical nodes
        'fnode': "\u250F", #--->  ┏
        'lnode': "\u2517", #--->  ┗
        'vnode': "\u2523", #--->  ┣
# Decorations
        'deco': "\u2578",  #--->  ╸
    }

    LAMBDA_SORT = {
        ("alpha", "a"): [
            lambda x: str(x['ppath']),
            'z'*500
        ],
        ("namefilefirst", "nf"): [
            lambda x: (
                str(x['ppath'].stem),
                int("dir" in x['kind'])
            ),
            ('z'*500, 0)
        ],
        ("filefirst", "f"): [
            lambda x: (
                int("dir" in x['kind']),
                str(x['ppath'])
            ),
            (0, 'z'*500)
        ],
        ("date", "d"): [
            lambda x: -x['ppath'].stat().st_mtime,
            float('inf')
        ],
    }

# Additional paths
    _ONLY_FOUND_PATHS, _MAIN_PATH = "found", "main"

# Formattings of the paths
    _LONG_PATH, _REL_PATH, _SHORT_PATH = "long", "relative", "short"
    _FORMATS = set([
        _LONG_PATH, _MAIN_PATH, _ONLY_FOUND_PATHS, _REL_PATH, _SHORT_PATH
    ])
    _PATH_FORMATS = set([_LONG_PATH, _REL_PATH, _SHORT_PATH])

# Special query
    _INTERNAL_QUERIES = set([_ELLIPSIS, _FILE, _DIR])


    def __init__(
        self,
        ppath,
        regpath = "**",
        display = "main short",
        sorting = "alpha"
    ):
# Verifications are done by the build method !
        self.ppath   = ppath
        self.regpath = regpath
        self.display = display
        self.sorting = sorting

# The internal representations of the folder.
        self.build()


# -------------------- #
# -- INTERNAL VIEWS -- #
# -------------------- #

    def build(self):                    # DOC OK !!
        """
prototype::
    see    = self.ascii , self.latex , self.toc , self.tree , self.sort
    action = this method builds one flat list ``self.listview`` of dictionaries
             which stores all the informations about the directory even the
             empty folders and the unmatching files,
             and also ``self.treeview`` a list of dictionaries which is like
             the natural tree structure of the folder analyzed
             (both of this object are sorted regarding to the value of the
             attribut ``self.sorting``)


======================================
Dictionaries used in ``self.listview``
======================================

The dictionaries look like the following one. You must know this structure if
you want to define your own kind of sorting for the output.

python::
    {
        'kind' : "dir" or "file",
        'depth': relative depth,
        'ppath': the whole path of one directory or file found
                 (this can also be an ellipsis path)
    }


info::
    The property like method ``self.ascii`` works iteratively with the
    argument ``self.listview``.


==================================
The structure of ``self.treeview``
==================================

This list contains the dictionnaries of the only first level object but for
folder a key ``'content'`` is added whose value is a list of dictionnaries
associated to its content and so on...


info::
    The property like method ``self.tree`` works recursively with the argument
    ``self.treeview``.
        """
# Do we have a folder ?
        if not self.ppath.is_dir():
            raise ValueError(
                "the argument ``ppath`` doesn't point to a directory."
            )

# Regpath infos
        queries, pattern = self.ppath.regpath2meta(
            self.regpath,
            regexit = False
        )

# Sorting: long names
        self._LAMBDA_SORT_LONGNAMES = {
            k[0]: v for k, v in self.LAMBDA_SORT.items()
        }

        _long_names = {x[1]: x[0] for x in self.LAMBDA_SORT}

        self.sorting = _long_names.get(self.sorting, self.sorting)

        if self.sorting not in self._LAMBDA_SORT_LONGNAMES:
            raise ValueError("unknown sorting rule.")

# Displaying
        _long_names = {x[0]: x for x in self._FORMATS}

        self.display = set(
            _long_names.get(x.strip(), x.strip())
            for x in self.display.split(" ") if x.strip()
        )

        if not self.display <= self._FORMATS:
            raise ValueError("illegal formatting rule (see ``display``).")

        nb_path_formats = len(self.display & self._PATH_FORMATS)

        if nb_path_formats == 0:
            self.display.add(_SHORT_PATH)

        elif nb_path_formats != 1:
            raise ValueError(
                "several path formatting rules (see ``display``)."
            )

# All the infos using ellipsis.
        allqueries = queries | self._INTERNAL_QUERIES
        allregpath = "{0}::{1}".format(" ".join(allqueries), pattern)

        self._extradepth = int(self._MAIN_PATH in self.display)

        self._all_listview = [
            self._metadatas(x)
            for x in self.ppath.walk(allregpath)
        ]

# We can know clean the list so as to only keep what the user wants.
        self._filedir_queries = queries & _FILE_DIR_QUERIES

        self._build_listview()
        self._build_treeview()

        self.sort()


    def _metadatas(self, ppath):        # DOC OK !!
        """
prototype::
    return = dict ;
             the dictionnary stores the path, its depth and the kind of object
             pointed by the path
             (this is for the elements in ``self.listview`` and partially for
             ``self.treeview``)
        """
        if ppath.name == EMPTY_OTHER_DIR:
            kind  = "empty_dir"
            ppath = ppath.parent

        elif ppath.name == OTHER_FILES:
            kind  = "other_files"
            ppath = ppath.parent / "..."

        elif ppath.is_dir():
            kind = "dir"

        else:
            kind = "file"

        metadatas = {
            'kind' : kind,
            'depth': ppath.depth_in(self.ppath) + self._extradepth,
            'ppath': ppath
        }

        return metadatas


    def _build_listview(self):          # DOC OK !!
        """
prototype::
    see    = self.build
    action = the attribut ``self.listview`` is build using the attribut
             ``self._all_listview``
        """
# Sub fles and folders found
        addall    = bool(self._ONLY_FOUND_PATHS not in self.display)
        _listview = []

        for metadatas in self._all_listview:
            if metadatas['kind'] in ["empty_dir", "other_files"]:
                if addall:
                    _listview.append(metadatas)

            elif metadatas['kind'] in self._filedir_queries:
                _listview.append(metadatas)

        _listview.sort(key = lambda x: str(x['ppath']))

# We have to find folders with only unmacthing files or with matching and
# unmacthing files, and also all the parent directories.
        self.listview = []
        lastreldirs   = []

        for i, metadatas in enumerate(_listview):
            relpath = metadatas['ppath'].relative_to(self.ppath)
            parents = relpath.parents

# We have to add all the parent directories !
            if "dir" in metadatas['kind']:
                lastreldirs.append(metadatas['ppath'].relative_to(self.ppath))

            else:
                for parent in reversed(parents):
                    if parent not in lastreldirs:
                        ppath = self.ppath / parent

                        self.listview.append({
                            'kind' : 'content_dir',
                            'depth': ppath.depth_in(self.ppath) \
                                     + self._extradepth,
                            'ppath': ppath
                        })

                        lastreldirs.append(parent)

            self.listview.append(metadatas)

# Main or not main, that is the question.
        if self._MAIN_PATH not in self.display:
            self.listview.pop(0)


    def _build_treeview(self):                  # DOC OK !!
        """
prototype::
    see    = self.build , self._rbuild_treeview
    action = this method returns the attribut ``self.treeview`` but all the
             job is done recursively by the method ``self._rbuild_treeview``
        """
        self.treeview = self._rbuild_treeview(self.listview)


    def _rbuild_treeview(self, listview):       # DOC OK !!
        """
prototype::
    action = the attribut ``self.treeview`` is build recursively using first
             the attribut ``self.listview``
        """
        i    = 0
        imax = len(listview)

        treeview = []

        while(i < imax):
            metadatas = listview[i]

# Simply a file.
            if 'file' in metadatas['kind']:
                treeview.append(metadatas)
                i += 1

# For a directory, we have to catch its content that will be analyzed
# recursively.
            else:
                depth   = metadatas['depth']
                content = []
                i += 1

                while(i < imax):
                    submetadatas = listview[i]
                    subdepth     = submetadatas['depth']

                    if subdepth > depth:
                        content.append(submetadatas)
                        i += 1

                    else:
                        break

                if content:
                    metadatas['content'] = self._rbuild_treeview(content)

                treeview.append(metadatas)

        return treeview


# ------------- #
# -- SORTING -- #
# ------------- #

    def _ellipsis_sort(self, metadatas):            # DOC OK !!
        """
prototype::
    arg    = dict: metadatas
    see    = self.build , self._metadatas
    return = str ;
             the value to use for the sorting
        """
        if metadatas['ppath'].name == "...":
            return self._ellipsi_sort_value

        else:
            return self._lambda_sort(metadatas)


    def sort(self):                     # DOC OK !!
        """
prototype::
    see    = self._rsort
    action = this method sorts the attribut ``self.treeview`` regarding to the
             value of the attribut ``self.sorting``, this job being done
             recursively by the method ``self._rsort``, and then the list
             ``self.listview`` is rebuild using the new ``self.treeview``
             (this is uggly but this allows to easily defined the methods of
             sorting, and this is easy to code)
        """
        self._lambda_sort        = self._LAMBDA_SORT_LONGNAMES[self.sorting][0]
        self._ellipsi_sort_value = self._LAMBDA_SORT_LONGNAMES[self.sorting][1]

# Each new sorting
        self.outputs = {}

# We sort ifirst the treeview (that allows to define natural sorintgs).
        self.treeview = self._rsort(self.treeview)

# We have to go back to ``self.listview`` !
        self.listview = self._rtree_to_list_view(self.treeview)


    def _rsort(self, treeview):                 # DOC OK !!
        """
prototype::
    arg    = list(dict): treeview
    see    = self.build , self._metadatas , self._ellipsis_sort
    return = list(dict) ;
             the treeview sorting regarding to the value of ``self.sorting``
             (the job is done recursively)
        """
        treeview.sort(key = self._ellipsis_sort)

        for i, metadatas in enumerate(treeview):
            if 'content' in metadatas:
                metadatas['content'] = self._rsort(metadatas['content'])
                treeview[i] = metadatas

        return treeview


    def _rtree_to_list_view(self, treeview):         # DOC OK !!
        """
prototype::
    see    = self.sort
    arg    = list(dict): treeview
    return = list(dict) ;
             the listview associated to ``self.treeview`` (the job is done
             recursively)
        """
        listview = []

        for metadatas in treeview:
            if 'content' in metadatas:
                content = metadatas['content']

# << Warning ! >> We can't use ``del metadatas['content']`` because this will
# always change self.treeview (we could have used a deepcopy but this  would
# be not efficient).
                newmetadatas = {}

                for k, v in metadatas.items():
                    if k != "content":
                        newmetadatas[k] = v

                listview.append(newmetadatas)
                listview += self._tree_to_list_view(content)

            else:
                listview.append(metadatas)

        return listview


# ------------ #
# -- OUPUTS -- #
# ------------ #

    def pathtoprint(self, metadatas):       # DOC OK !!
        """
prototype::
    arg    = dict: metadatas
    return = str ;
             the string to print for a path
        """
# << Warning ! >> The paths are whole ones by default !
        kind  = metadatas["kind"]
        ppath = metadatas["ppath"]
        name  = ppath.name

        if name == "..." or self._SHORT_PATH in self.display:
            strpath = name

        elif self._REL_PATH in self.display:
            if ppath == self.ppath:
                strpath = name

            else:
                strpath = str(ppath.relative_to(self.ppath))

        else:
            strpath = str(ppath)

        return strpath


    @property
    def toc(self):          # DOC OK !!
        """
prototype::
    type   = property
    return = str ;
             the content only shows files and their direct parent folder like
             a kind of table of content where the section are always relative
             paths of parent directories and subsection are pathe of files
             (empty flders are never displayed)
        """
# Source: http://en.wikipedia.org/wiki/Box-drawing_character

# The job has to be done.
        if 'toc' not in self.outputs:
            text     = []
            lastdir  = None
            tab      = self.ASCII_DECOS["tab"]
            decodir  = self.ASCII_DECOS["dir"]
            decofile = self.ASCII_DECOS["file"]
            mainname = self.ppath.name

            for metadatas in self.listview:
                if "file" in metadatas["kind"]:
                    pathtoprint = self.pathtoprint(metadatas)

                    if lastdir:
                        dirpath \
                        = mainname / lastdir["ppath"].relative_to(self.ppath)

                        text.append("")
                        text.append("{0} {1}".format(decodir, dirpath))

                        lastdir = None

                    text.append(
                        "{0}{1} {2}".format(tab, decofile, pathtoprint)
                    )

                else:
                    lastdir = metadatas

            if "dir" in metadatas["kind"]:
                dirpath \
                = mainname / metadatas["ppath"].relative_to(self.ppath)

                text.append("")
                text.append("{0} {1}".format(decodir, dirpath))

            self.outputs['toc'] = '\n'.join(text[1:])


# The job has been done.
        return self.outputs['toc']


    @property
    def ascii(self):                # DOC OK !!
        """
prototype::
    type   = property
    return = str ;
             a basic tree using only ¨ascii characters
        """
# The job has to be done.
        if 'ascii' not in self.outputs:
            text = []

            for metadatas in self.listview:
                depth = metadatas["depth"]
                tab   = self.ASCII_DECOS['tab']*depth

                decokind    = self.ASCII_DECOS[metadatas["kind"]]
                pathtoprint = self.pathtoprint(metadatas)

                text.append(
                    "{0}{1} {2}".format(tab, decokind, pathtoprint)
                )

            self.outputs['ascii'] = '\n'.join(text)

# The job has been done.
        return self.outputs['ascii']


    @property
    def tree(self):                 # DOC OK !!
        """
prototype::
    see    = self._rtree
    type   = property
    return = str ;
             a tree using special ¨unicode characters such as to draw some
             additional rules
        """
# The job has to be done.
        if 'tree' not in self.outputs:
# One dir or file alone (extra prossibilty)
            if len(self.listview) == 1:
                self.outputs['tree'] = "{0} {1}".format(
                    self.UTF8_DECOS['hrule'],
                    self.pathtoprint(self.listview[0])
                )

            else:
# Ugly patch !!!
                self.outputs['tree'] = "\n".join([
                    x[4:]
                    for x in self._rtree(self.treeview)
                ])

# The job has been done.
        return self.outputs['tree']


    def _rtree(self, treeview):             # DOC OK !!
        """
prototype::
    return = str ;
             the lines of the tree that uses ¨unicode characters to draw some
             additional rules
        """
        lines       = []
        imax        = len(treeview) - 1
        thisdepth   = treeview[0]['depth']

        if thisdepth <= 3:
            subtabdepth = 0

        else:
            subtabdepth = thisdepth - 2

        for i, metadatas in enumerate(treeview):
# Rule regarding the kind of object.
            isdir = 'dir' in metadatas['kind']

# Rule before any kind of rule.
            if thisdepth == 0:
                addvrule = False
# Ugly patch !!!
                before   = "  "

            elif i == imax:
                addvrule = False
                before   = " " + self.UTF8_DECOS['lnode']

            else:
                addvrule = True
                before   = " " + self.UTF8_DECOS['vnode']

# Just add the object.
            lines.append(
                "{0}{1} {2}{3}".format(
                    before,
                    self.UTF8_DECOS['hrule'],
                    self.UTF8_DECOS['deco'],
                    self.pathtoprint(metadatas)
                )
            )

# A new not empty directory
            if isdir and metadatas['content']:
                subbefore = " "*subtabdepth

                if addvrule:
                    subbefore += " " + self.UTF8_DECOS['vrule'] + "  "

                else:
                    subbefore += "    "

                lines += [
                    subbefore + x
                    for x in self._rtree(metadatas['content'])
                ]

        return lines


    @property
    def latex(self):                # DOC OK !!
        """
prototype::
    type   = property
    return = str ;
             a ¨latex code that can be used by the ¨latex package 
             ¨latex::``dirtree``
        """
# The job has to be done.
        if 'latex' not in self.outputs:
            text = []

            for metadatas in self.listview:
                depth = metadatas["depth"] + 1
                pathtoprint = latex_escape(self.pathtoprint(metadatas))

                text.append(
                    "{0}.{1} <{2}>.".format(
                        "  "* depth,
                        depth,
                        pathtoprint
                    ).replace('<', '{').replace('>', '}')
                )

            self.outputs['latex'] = "\dirtree{%\n" + '\n'.join(text) + "\n}"

# The job has been done.
        return self.outputs['latex']
