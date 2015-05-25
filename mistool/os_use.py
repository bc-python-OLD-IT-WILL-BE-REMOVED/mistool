#!/usr/bin/env python3

"""
prototype::
    date = 2015-05-25


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


# ------------------------------------- #
# -- SPECIAL FUNCTIONS FOR OUR CLASS -- #
# ------------------------------------- #

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


# -------------- #
# -- REGPATHS -- #
# -------------- #

# Sources for the regex:
#
#     * http://stackoverflow.com/a/430781/4589608
#     * http://stackoverflow.com/a/30439865/4589608
#     * http://stackoverflow.com/a/817117/4589608
#     * http://stackoverflow.com/questions/20294704/which-pattern-has-been-found/20294987

_VISIBLE, _DIR, _FILE, _RELATIVE = "visible", "dir", "file", "relative"

_PATH_QUERIES      = set([_VISIBLE, _DIR, _FILE, _RELATIVE])
_LONG_PATH_QUERIES = {x[0]: x for x in _PATH_QUERIES}
_FILE_DIR_QUERIES  = _PATH_QUERIES - set([_VISIBLE])
_VISIBLE_QUERY     = set([_VISIBLE])

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

    >>> print(path.regpath2meta("file-visible::**.py"))
    ({'visible', 'file'}, '.+\\.py')


In the outputs printed, `{'file', 'dir'}` indicates to look for any kind of
files and directories, whereas `{'file', 'visible'}` asks to only keep visible
files, i.e. files without a name starting with a point.


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


==================
An addiitonal rule
==================

A regpath starting with the ¨os separator indicates that the search must be
done relatively to the current directory.


==============
The query part
==============

Before two double points, you can use the following queries.

    a) ``file`` asks to keep only files. You can use the shortcut ``f``.

    b) ``dir`` asks to keep only folders. You can use the shortcut ``d``.

    c) ``visible`` asks to keep only visible files and folders. This ones have
    a name begining with ``.``.

    d) ``visible-file`` and ``visible-dir`` ask to respectively keep
    only visible files, or only visible directories.

    e) ``relative`` simply allows to do searches relatively to the current
    directory if ``PPath`` points to a folder.


For example, to keep only the Python files, in a folder or not, just use
``"file::**.py"``. This is not the same that ``"**.py"`` which will also catch
folders with a name finishing by path::``.py``.


info::
    For each query, you can only use the initial letter of the query. For
    example, ``f`` is a shortcut for ``file``, and ``v-f`` is the same that
    ``visible-file``.
    """
    queries, *pattern = regpath.split("::")

    if len(pattern) > 1:
        raise ValueError("too much \"::\" in the regpath.")

# Two pieces
    if pattern:
        pattern = pattern[0]
        queries = set(_LONG_PATH_QUERIES.get(x, x) for x in queries.split("-"))

        if not queries <= _PATH_QUERIES:
            raise ValueError("illegal filter in the regpath.")

# One single piece
    else:
        queries, pattern = _FILE_DIR_QUERIES, queries

# Just visible objects ?
    if queries == _VISIBLE_QUERY:
        queries |= _FILE_DIR_QUERIES

# The regex uncompiled version : we just do replacing by taking care of
# the escaping character. We play with regexes to do that.
#
# << Warning : >> ***, ****, ... are not allowed !

    if regexit:
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
        pattern     = newpattern

    return queries, pattern


# ------------------ #
# -- WALK AND SEE -- #
# ------------------ #

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
        + subdir
            * slide_A.pdf
            * slide_B.pdf
            * subcode_A.py
            * subcode_B.py

Here is two examples of use where you can see that the repaths ``"*"`` and
``"**"`` don't do the same thing : there are two much files with ``"**"``. Just
go to the documentation of the function ``_ppath_regpath2meta`` so as to know
why (you have to remember that by default the search is relative).

pyterm::
    >>> from mistool.os_use import PPath
    >>> folder = PPath("/Users/projects/dir")
    >>> for p in folder.walk("*.py"):
    ...     print("+", p)
    ...
    + /Users/projects/dir/code_1.py
    + /Users/projects/dir/code_2.py
    >>> for p in folder.walk("**.py"):
    ...     print("+", p)
    ...
    + /Users/projects/dir/code_1.py
    + /Users/projects/dir/code_2.py
    + /Users/projects/dir/subdir/code_A.py
    + /Users/projects/dir/subdir/code_B.py
    """
# Do we have an existing directory ?
    if not cls.is_dir():
        raise OSError("the path doesn't point to a directory.")

# Metadatas and the normal regex
    queries, pattern = cls.regpath2meta(regpath)

    keepdir     = _DIR in queries
    keepfile    = _FILE in queries
    keepvisible = _VISIBLE in queries
    relsearch   = _RELATIVE in queries

    regex_obj = re.compile("^{0}$".format(pattern))

# Let's walk
    for root, dirs, files in os.walk(str(cls)):

# Do the current directory must be added ?
        addthisdir = False

        if keepdir \
        and root != str(cls) \
        and regex_obj.match(root):
            root_ppath = PPath(root)

            if not keepvisible \
            or not any(
                x.startswith('.')
                for x in root_ppath.relative_to(cls).parts
            ):
                addthisdir = True

# A new file ?
        if keepfile:
            for file in files:
                if keepvisible and file.startswith('.'):
                    continue

                full_file = os.path.join(root, file)

                if relsearch:
                    ppath_full_file = PPath(full_file)
                    rel_file = str(ppath_full_file.relative_to(cls))

                    if regex_obj.match(rel_file):
                        yield ppath_full_file

                elif regex_obj.match(full_file):
                    yield PPath(full_file)

# A new directory ?
        if addthisdir:
            yield root_ppath


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
    >>> path_1.create(_FILE)
    >>> path.is_file()
    True
    >>> path_2 = PPath("test/README")
    >>> path_2.create(_DIR)
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
    see    = PPath , _ppath_regpath2meta
    arg    = PPath: cls ;
             this argument nearly refers to the ``self`` used by the associated
             method ``depth_in`` of the class ``PPath``
    arg    = str: regpath ;
             this is a string that follows some rules named regpath rules (see
             the documentation of the function ``_ppath_regpath2meta``)
    action = every files and directories matching ``regpath`` are removed
    """
# We have to play with the queries and the pattern in ``regpath``.
    queries, pattern = regpath2meta(regpath, regexit = False)

    if _VISIBLE in queries:
        prefix = "visible-"

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
        raise ValueError("copy of directories is not yet supported.")

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
    type = class ;
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
# -- VIEWS OF A FOLDER -- #                                    # DOC OK !!
# ----------------------- #

ELLIPSIS_PPATH = PPath('...')

# Source: https://hg.python.org/cpython/file/default/Lib/functools.py#l210
class K(object):
    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        return mycmp(self.obj, other.obj) < 0

    def __gt__(self, other):
        return mycmp(self.obj, other.obj) > 0

    def __eq__(self, other):
        return mycmp(self.obj, other.obj) == 0

    def __le__(self, other):
        return mycmp(self.obj, other.obj) <= 0

    def __ge__(self, other):
        return mycmp(self.obj, other.obj) >= 0


class DirView:
    """
prototype::
    type = class ;
           this class allows to display the tree structure of one directory
           with the extra possibility to keep and show only some informations
    see  = _ppath_regpath2meta
    arg  = PPath: ppath ;
           this argument is the path of the directory to analyze
    arg  = str: regpath ;
           this is a string that follows some rules named regpath rules (see
           the documentation of the function ``_ppath_regpath2meta``)
    arg  = str: display = "main short" in "long", "relative",
                                          "short", "main", "found" ;
           this string allows to give informations about the output to produce








-----------------
Small description
-----------------

example !

code::
    + mistool_old
        * __init__.py
        * latex_use.py
        * LICENCE.txt
        * os_use.py
        * README.md
        * ...
        + change_log
            + 2012
                * 07.pdf
                * 08.pdf
                * 09.pdf
        + debug
            * debug_latex_use.py
            * debug_os_use.py
            + debug_latex_use
                * latex_test.pdf
                * latex_test.tex
                * latex_test_builder.py
                * ...
        + to_use
            + latex
                * ...


ou bien possible

code::
    + mistool_old
        * __init__.py
        * latex_use.py
        * LICENCE.txt
        * os_use.py
        * README.md
        * ...

    + mistool_old/change_log/2012
        * 07.pdf
        * 08.pdf
        * 09.pdf

    + mistool_old/debug
        * debug_latex_use.py
        * debug_os_use.py

    + mistool_old/debug/debug_latex_use
        * latex_test.pdf
        * latex_test.tex
        * latex_test_builder.py
        * ...

    + to_use/latex
        * ...



In this output no invisible directory or file has been printed, and ellipsis
indicates visible files that do not match to a given pattern for the paths.
All of this has been obtained with the following code.

pyterm::
    from mistool.os_use import PPath

    DirView = os_use.DirView(
        ppath      = "/Users/projetmbc/python/mistool",
        regpath = "visible::*.(py|txt|tex|pdf)",
        display    = "main short"
    )

    print(DirView.ascii)






warning::
    You have to see the documentation of the function ``regpath2meta`` in the
    submodule ``config.pattern`` so as to have informations on regpaths
    (an homemade concept).




-------------
The arguments
-------------

This class uses the following variables.

    3) ``display`` is an optional string which can contains the following
    options separated by spaces. By default, ``format = "main short"``.

        a) ``long`` asks to display the whole paths of the
        files and directories found. You can use the shortcut ``l``.

        b) ``relative`` asks to display relative paths comparing to the main
        directory analysed. You can use the shortcut ``r``.

        c) ``short`` asks to only display names of directories found, and
        names, with its extensions, of the files found. You can use the
        shortcut ``s``.

        d) ``main`` asks to display the main directory which is analyzed. You
        can use the shortcut ``m``.

        e) ``found`` asks to only display directories and files which path
        matches the pattern ``regpath``. You can use the shortcut ``f``.
    """
    ASCII_DECOS = {
        'dir' : "+",
        'file': "*",
        'tab' : " "*4
    }

    _FORMATTERS = set(["found", "main", "long", _RELATIVE, "short"])
    _PATH_FORMATTERS = set(["long", _RELATIVE, "short"])
    _LONG_FORMATTERS = {x[0]: x for x in _FORMATTERS}

    def __init__(
        self,
        ppath,
        regpath = "**",
        display = "main short"
    ):
        if not ppath.is_dir():
            raise ValueError(
                "the argument ``ppath`` doesn't point to a directory"
            )

        self.ppath   = ppath
        self.regpath = regpath
        self.display = display

        self.build()


    def build(self):
        """
This method builds first one flat list ``self.listview`` of dictionaries of the
following kind that will ease the making of the tree view. This list is sorted
in alphabetic order with a depth walk.

pyterm::
    {
        'kind'   : _DIR or _FILE,
        'depth'  : the depth level regarding to the main directory,
        'relpath': the relative path of one directory or file found
    }
        """
# Reset all things !
        self.listview = []
        self.options  = set()
        self.output   = {}

        self.queries, _ = regpath2meta(
            self.regpath,
            regexit = False
        )

# What have to be displayed ?
        for opt in self.display.split(" "):
            opt = opt.strip()
            opt = self._LONG_FORMATTERS.get(opt, opt)

            if opt not in self._FORMATTERS:
                raise ValueError("unknown option for displaying.")

            self.options.add(opt)

        if len(self._PATH_FORMATTERS & self.options) > 1:
            raise ValueError("ambiguous option for printing the paths.")

# We must add all the folders except if the option "found" has been used.
        if "found" not in self.options:
            if _VISIBLE in self.queries:
                prefix = "visible-"

            else:
                prefix = ""

            self.listview = [
                {
                    'kind'   : _DIR,
                    'depth'  : p.depth_in(self.ppath),
                    'relpath': p.relative_to(self.ppath)
                }
                for p in self.ppath.walk(prefix + "dir::**")
            ]

# Unsorted flat version of the tree view.
        for path in self.ppath.walk(self.regpath):
            kind = _FILE if path.is_file() else _DIR

            infos = {
                'kind'   : kind,
                'depth'  : path.depth_in(self.ppath),
                'relpath': path.relative_to(self.ppath)
            }

# We do not want to see twice a folder !
            if kind == _FILE or infos not in self.listview:
                self.listview.append(infos)

# If the option "found" has been used, we must add folders of files found.
        if "found" in self.options:
            self._add_parentdir()








        self.listview.sort(key = K)
        return None


# We build the alphabetic sorted version. This works because ``PPath`` does
# better comparisons than the ones of ``pathlib``.
        self.listview.sort(key = lambda x: x['relpath'])

# If the option "found" has not been used, we must take care of folder with no
# winning files so as to display ellipsis ``...``.
        if "found" not in self.options:
            self._add_ellipsis()

# "Files first" sorting version of the flat version of the tree view.
        if "alpha" not in self.options:
            self._filefirst_sort()


    def _filefirst_sort(self):
        """
This method sorts the list view so as to first show the files and then the
directories contained in a folder.
        """
        maxdepth = 0
        depth    = 0

        while(depth <= maxdepth):
            firsts = []
            lasts  = []

            for infos in self.listview:
                if infos['depth'] < depth:
                    firsts += lasts
                    lasts = []
                    firsts.append(infos)

                elif infos['depth'] == depth:
                    if infos['kind'] == _FILE:
                        firsts.append(infos)

                    else:
                        lasts.append(infos)
                else:
                    if infos['depth'] > maxdepth:
                        maxdepth = infos['depth']

                    lasts.append(infos)

            self.listview = firsts + lasts

            depth += 1

    def _add_parentdir(self):
        """
When the option ``found`` is used, we only show files found but we also have to
add all their parent directories.
        """
        for x in self.listview:
            parts = x['relpath'].parts

            if len(parts) != 1:
                newdir = PPath("")
                depth  = -1

                for part in parts[:-1]:
                    newdir /= part
                    depth  += 1

                    infos = {
                        'kind'   : _DIR,
                        'depth'  : depth,
                        'relpath': newdir
                    }

                    if infos not in self.listview:
                        self.listview.append(infos)

    def _add_ellipsis(self):
        """
When the option ``found`` is not used, we have to add ellipsis ``...`` so as to
materiealize unshown files.
        """
        indexes = []

        for i, infos in enumerate(self.listview):
            if infos['kind'] == _DIR:
                for p in (self.ppath / infos['relpath']).iterdir():
                    if p.is_file() \
                    and (
                        _VISIBLE not in self.queries
                        or not p.name.startswith('.')
                    ) \
                    and {
                        'kind'   : _FILE,
                        'depth'  : infos['depth'] + 1,
                        'relpath': p.relative_to(self.ppath)
                    } not in self.listview:
                        indexes.append((i + 1, infos['depth'] + 1))
                        break

        delay = 0

        for i, depth in indexes:
            self.listview.insert(
                i + delay,
                {
                    'kind'   : _FILE,
                    'depth'  : depth,
                    'relpath': ELLIPSIS_PPATH
                }
            )

            delay += 1


    @property
    def ascii(self):
        """
This attribut like method returns an ASCCI view of the tree structure.
        """
        if 'ascii' not in self.output:
            seemain = "main" in self.options
            text    = []

            if seemain:
                if "long" in self.options:
                    mainpath = self._pathprinted(PPath(""))

                else:
                    mainpath = self.ppath.name

                text = [
                    "{0} {1}".format(self.ASCII_DECOS[_DIR], mainpath)
                ]

            for infos in self.listview:
                depth = infos["depth"]

# Does the main directory must be displayed ?
                if seemain:
                    depth += 1

                tab = self.ASCII_DECOS['tab']*depth

                decokind = self.ASCII_DECOS[infos["kind"]]

                pathtoshow = self._pathprinted(infos["relpath"])

                text.append(
                    "{0}{1} {2}".format(tab, decokind, pathtoshow)
                )

            self.output['ascii'] = '\n'.join(text)

        return self.output['ascii']


    def _pathprinted(self, path):
# The path are stored relatively by default !
        if path == ELLIPSIS_PPATH or  _RELATIVE in self.options:
            return str(path)

# We have to rebuild the while path.
        if "long" in self.options:
            return str(self.ppath / path)

# "short" is the default option for printing the paths.
        return str(path.name)


# ------------------- #
# -- GENERAL INFOS -- #
# ------------------- #

def pathenv():                        # DOC OK !!
    """
prototype::
    type   = function
    action = this function simply returns the variable ``PATH`` that contains
             paths of some executables known by your OS
    """
    return os.getenv('PATH')


def system():                        # DOC OK !!
    """
prototype::
    type   = function
    action = the purpose of this function is to give the name, in lower case,
             of the OS used (possible names can be "windows", "mac", "linux"
             and also "java")
    """
    osname = platform.system()

    if not osname:
        raise SystemError("the operating sytem can not be found.")

    if osname == 'Darwin':
        return "mac"

    else:
        return osname.lower()
