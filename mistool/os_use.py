#!/usr/bin/env python3

"""
prototype::
    date = 2016-04-06


The main feature of this module is the class ``PPath`` which is an enhanced
version of the standard class ``pathlib.Path`` that allows to manipulate easily
paths and as a consequence files and folders.

There are also other small useful functions like ``runthis`` that really
simplify the use of a command line from ¨python codes.
"""

import os
import pathlib
import platform
import re
import shlex
import shutil
from subprocess import (
    check_call,
    check_output
)


# -------------------- #
# -- SAFE CONSTANTS -- #
# -------------------- #

OS_MAC   = "mac"
OS_LINUX = "linux"
OS_WIN   = "windows"

# Sources for the regex:
#     * http://stackoverflow.com/a/430781/4589608
#     * http://stackoverflow.com/a/30439865/4589608
#     * http://stackoverflow.com/a/817117/4589608
#     * http://stackoverflow.com/a/20294987/4589608

ALL_DIR_TAGS = DIR_TAG, DIR_OTHERS_TAG \
             = "dir",   "dir_others"

ALL_FILE_TAGS = FILE_TAG, FILE_OTHERS_TAG \
              = "file",   "file_others"

FILE_DIR_OTHERS_NAME = "..."


NOT_QUERY      = "not"
FILE_DIR_QUERY = set([FILE_TAG, DIR_TAG])


ALL_DISPLAY, XTRA_DISPLAY = "all", "xtra"


REGPATH_QUERIES = set([
    DIR_TAG, FILE_TAG,
    NOT_QUERY,
    ALL_DISPLAY, XTRA_DISPLAY
])

LONG_REGPATH_QUERIES = {x[0]: x for x in REGPATH_QUERIES}


RE_SPECIAL_CHARS = re.compile(
    r"(?<!\\)((?:\\\\)*)((\*+)|(@)|(×)|(\.))"
)

REGPATH_TO_REGEX = {
    '**': ".+",
    '.' : r"\.",
    '@' : ".",
    '×' : "*",
}

REGPATH_SPE_CHARS = list(REGPATH_TO_REGEX) + ["*"]

REGPATH_TO_REGEX['\\'] = "[^\\]+"
REGPATH_TO_REGEX['/']  = "[^/]+"


# ------------------- #
# -- GENERAL INFOS -- #
# ------------------- #

SEP = os.sep

def pathenv():
    """
prototype::
    return = str ;
             the variable ``PATH`` that contains paths of executables known
             by your OS
    """
    return os.getenv('PATH')


def system():
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
        return OS_MAC

    else:
        return osname.lower()


# -------------------------------- #
# -- CHANGING CURRENT DIRECTORY -- #
# -------------------------------- #

class cd:
    """
prototype::
    type = cls ;
           this class i a context manager that allows to easily change the
           current directory as this can be done using term::``cd`` in a ¨unix
           system, or term::``chdir`` in a ¨win sytem

    arg-attr = PPath: ppath ;
               this gives the path where to go

Let's suppose that we have the following directory having the absolute path
path::``/Users/projetmbc/basic_dir`` in a ¨unix system.

dir::
    + basic_dir
        * latex_1.tex
        * latex_2.tex
        * python_1.py
        * python_2.py
        * python_3.py
        * python_4.py
        * text_1.txt
        * text_2.txt
        * text_3.txt
        + empty_dir
        + sub_dir
            * code_A.py
            * code_B.py
            * slide_A.pdf
            * slide_B.pdf
            + sub_sub_dir
                * doc.pdf


In the following ¨unix example, the use of ``subprocess.call("ls")`` is similar
to use term::``ls`` directly in a ¨unix terminal so as to have the list of all
files and directories directly contained in a the current folder. As you can
see, the lists of files and folders correspond to the current directory choosen
with the class ``cd``.

pyterm::
    >>> import subprocess
    >>> from mistool.os_use import cd
    >>> with cd("/Users/projetmbc/basic_dir"):
    ...     subprocess.call("ls")
    empty_dir	python_1.py	python_4.py	text_2.txt
    latex_1.tex	python_2.py	sub_dir		text_3.txt
    latex_2.tex	python_3.py	text_1.txt
    >>> with cd("/Users/projetmbc/basic_dir/sub_dir"):
    ...     subprocess.call("ls")
    code_A.py	slide_A.pdf	sub_sub_dir
    code_B.py	slide_B.pdf


info::
    All the code comes from
    cf::``this post ; http://stackoverflow.com/a/13197763/4589608``.
"""
    def __init__(self, ppath):
        self._newstrpath = str(ppath.normpath)
        self._tag        = ""

    def __enter__(self):
        self._savedpath = os.getcwd()
        os.chdir(self._newstrpath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self._savedpath)


# ------------------------ #
# -- OUR ENHANCED CLASS -- #
# ------------------------ #

# -- FOR THE REGPATHS -- #

def regexify(pattern, sep = "/"):
    """
prototype::
    arg = str: pattern ;
          ``pattern`` is a regpath pattern using a syntax which tries to catch
          the best of the regex and the Unix-glob syntaxes
    arg = str: sep = "/" ;
          this indicates an ¨os like separator

    return = str ;
             a regex uncompiled version of ``pattern``.


====================
Some examples of use
====================

The next section gives all the difference between the regpath patterns and the
regexes of ¨python.


Let suppose fisrt that we want to find paths without any ``/`` the default
value of the argument ``sep`` that finish with either path::``.py`` or
path::``.txt``. The code below shows how ``regexify`` gives easily an
uncompiled regex pattern to do such searches.

pyterm::
    >>> from mistool.os_use import regexify
    >>> print(regexify("*.(py|txt)"))
    [^/]+\.(py|txt)


Let suppose now that we want to find paths that finish with either
path::``.py`` or path::``.txt``, and that can also be virtually or really
found recursivly when walking in a directory. Here is how to use ``regexify``.

pyterm::
    >>> from mistool.os_use import regexify
    >>> print(regexify("**.(py|txt)"))
    .+\.(py|txt)


=============================
A Unix-glob like regex syntax
=============================

Here are the only differences between the Unix-glob like regex syntax with the
Unix-glob syntax and the traditional regexes.

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
    """
    onestar2regex = REGPATH_TO_REGEX[sep]

    newpattern = ""
    lastpos    = 0

    for m in RE_SPECIAL_CHARS.finditer(pattern):
        spechar = m.group()

        if spechar not in REGPATH_SPE_CHARS:
            raise ValueError("too much consecutive stars ''*''")

        spechar     = REGPATH_TO_REGEX.get(spechar, onestar2regex)
        newpattern += pattern[lastpos:m.start()] + spechar
        lastpos     = m.end()

    newpattern += pattern[lastpos:]

    return newpattern


def regpath2meta(regpath, sep = "/", regexit = True):
    """
prototype::
    see = regexify

    arg = str: regpath ;
          ``regpath`` uses a syntax trying to catch the best of the regex and
          the Unix-glob syntaxes with also some little extra queries
    arg = str: sep = "/" ;
          this indicates an ¨os like separator
    arg = bool: regexit = True ;
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
    >>> print(path.regpath2meta(regpath = "*.(py|txt)", regexit = False))
    ({'dir', 'file'}, '*.(py|txt)')
    >>> print(path.regpath2meta("all file::**.py"))
    ({'all', 'file'}, '.+\\.py')


In the outputs printed, `{'dir', 'file'}` indicates to look only for visible
files and directories, whereas `{'all', 'file'}` asks to keep also invisible
files, i.e. files having a name starting with a point.


=================================
The regex and Unix-glob like part
=================================

See the documentation of the function ``regexify``.


==============
The query part
==============

Before two double points, you can use the following queries separated by
spaces.

    1) ``not`` is very useful because it allows simply to look for something
    that does not match the pattern (you have to know that direct negation with
    regexes can be messy).

    2) ``file`` asks to keep only files.

    3) ``dir`` asks to keep only folders.

    4) ``all`` asks to keep also the hidden files and folders. This ones have
    a name begining with a point.

    5) ``all file`` asks to only keep files even the hidden ones. You can also
    use ``all dir``.

    6) ``relative`` indicates that the pattern after ``::`` is relatively to
    the current directory and not to a absolute path.

    7) ``xtra`` asks to keep folder with some files not matching a regpath.
    Extra informations are given by the hidden attribut ``_tag`` (this feature
    is used by the class ``term_use.DirView``).


For example, to keep only the ¨python files, in a folder or not, just use
``"file::**.py"``. This is not the same that ``"**.py"`` which will also catch
folders with a name finishing by path::``.py`` (that is legal).


info::
    For each query, you can use just its initial letter. For example, ``f`` is
    a shortcut for ``file``, and ``a f`` is the same as ``all file``.
    """
    queries, *pattern = regpath.split("::")

    if len(pattern) > 1:
        raise ValueError("too much \"::\" in the regpath.")

# Two pieces
    if pattern:
        pattern = pattern[0]

        queries = set(
            LONG_REGPATH_QUERIES.get(x.strip(), x.strip())
            for x in queries.split(" ")
            if x.strip()
        )

        if not queries <= REGPATH_QUERIES:
            raise ValueError("illegal filter(s) in the regpath.")

# One single piece
    else:
        queries, pattern = FILE_DIR_QUERY, queries

# The queries "file" and "dir" are not used.
    if FILE_TAG not in queries and DIR_TAG not in queries:
        queries |= FILE_DIR_QUERY

# The regex uncompiled version : we just do replacing by taking care of
# the escaping character. We play with regexes to do that.
#
# << Warning : >> ***, ****, ... are not allowed !

    if regexit:
        pattern = "^{0}$".format(
            regexify(
                pattern = pattern,
                sep     =sep
            )
        )

    return queries, pattern


# Sublcassing ``pathlib.Path`` is not straightforward ! The following post gives
# the less ugly way to do that :
#     * http://stackoverflow.com/a/34116756/4589608

class PPath(type(pathlib.Path())):
    """
prototype::
    see = pathlib.Path

    type = cls ;
           this class adds some functionalities to the standard class
           ``pathlib.Path``


warning::
    The method ``walk`` of this class uses an hidden attribut ``_tag`` which has
    no meaning outside the scope of the method ``walk``.
    """

# -- ABOUT -- #

    def is_empty(self):
        """
prototype::
    return = bool ;
             if ``PPath`` is not an existing directory an error is raised, but
             if the ``PPath`` points to an empty directory, ``False`` is
             returned, otherwise that is ``True`` which is returned
        """
        if not self.is_dir():
            raise NotADirectoryError(
                "the following path does not point to an existing directory :"
                "\n    + {0}".format(self)
            )

        for onepath in self.walk():
            return False

        return True

    def is_protected(self):
        """
prototype::
    return = bool ;
             if the path doe not point to an existing file or folder, an
             ``OSError`` error is raised,
             if the path is the one of a folder, the answer returned is
             ``True`` for a modifiable directory and ``False`` othrewise,
             and finally if the path points to a file, then that is its
             parent folder which is tested
        """
        if self.is_file():
            ppath = self.parent

        elif self.is_dir():
            ppath = self

        else:
            raise FileNotFoundError(
                "the following path doesn't point to something inside an "
                "existing directory :\n    + {0}".format(self)
            )

# Source :
#     * http://stackoverflow.com/q/2113427/4589608
        return not os.access(
            path = str(ppath),
            mode = os.W_OK | os.X_OK
        )

    @property
    def depth(self):
        """
prototype::
    see = self.depth_in

    return = int ;
             the absolute depth of a path


Here is an example of use.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path = PPath("/Users/projetmbc/source/misTool/os_use.py")
    >>> print(path.depth)
    4
        """
        return len(self.parents) - 1

    @property
    def ext(self):
        """
prototype::
    see = self.with_ext

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
        return self.suffix[1:]

# -- CHANGING A PATH -- #

    def with_ext(self, ext):
        """
prototype::
    arg = str: ext ;
          value of the extension

    return = PPath ;
             a new path obtained from the current path by adding or changing
             the extension using the value of ``ext``


Here are two examples.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path = PPath("dir/subdir")
    >>> path.with_ext("ext")
    PPath('dir/subdir.ext')
    >>> path = PPath("dir/subdir/file.txt")
    >>> path.with_ext("ext")
    PPath('dir/subdir/file.ext')
        """
        if ext:
            ext = "." + ext

        return self.with_suffix(ext)

    @property
    def normpath(self):
        """
prototype::
    return = PPath ;
             a new path obtained from the current path by interpreting the
             leading shortcut path::``~``, and the shortcuts for relative
             paths like path::``/../`` that are used to go higher in the tree
             structure


Here is an example made on the ¨mac of the author of ¨mistool where the user's
folder is path::``/Users/projetmbc``.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path = PPath("~/dir_1/dir_2/dir_3/../../file.txt")
    >>> path.normpath
    PPath('/Users/projetmbc/dir_1/file.txt')
    """
        return PPath(
            os.path.normpath(
                os.path.expanduser(str(self))
            )
        )

    @property
    def shortpath(self):
        """
prototype::
    return = PPath ;
             a new path obtained from the current path by trying to use the
             leading shortcut path::``~``, and by intepreting the shortcuts
             path::``/../`` used to go higher in the tree structure


Here is an example made on the Mac of the author of ¨mistool. In that case
path::``/Users/projetmbc`` is the user's folder.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path = PPath("/Users/projetmbc/dir_1/dir_2/dir_3/../../file.txt")
    >>> path.shortpath
    PPath('~/dir_1/file.txt')
        """
        path     = os.path.normpath(os.path.expanduser(str(self)))
        userpath = os.path.expanduser("~") + self._flavour.sep

        if path.startswith(userpath):
            path = "~" + self._flavour.sep + path[len(userpath):]

        return PPath(path)

# -- COMPARING PATHS -- #

    def common_with(self, *args):
        """
prototype::
    see = self.__and__

    args = PPath ;
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
    >>> path        = PPath("/Users/projetmbc/source/doc")
    >>> path_1      = PPath("/Users/projetmbc/README")
    >>> path_2      = PPath("/Users/projetmbc/source/misTool/os_use.py")
    >>> path_danger = PPath("/NoUser/projects")
    >>> path.common_with(path_1)
    PPath('/Users/projetmbc')
    >>> path.common_with(path_2)
    PPath('/Users/projetmbc/source')
    >>> path.common_with(path_danger)
    PPath('/')
    >>> path.common_with(path_1, path_2)
    PPath('/Users/projetmbc')
    >>> path.common_with([path_1, path_2])
    PPath('/Users/projetmbc')


You can also use the magic method ``&`` as a shortcut to ``common_with``. Some
of the preceding examples becomes then the following ones.

pyterm::
    >>> path & path_1
    PPath('/Users/projetmbc')
    >>> path & path_1 & path_2
    PPath('/Users/projetmbc')
    >>> path & [path_1, path_2]
    PPath('/Users/projetmbc')


info::
    The use of ``&`` was inspired by the analogy between the logical "AND" and
    the intersection of sets.
        """
        commonparts = list(self.parts)

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

    def __and__(self, paths):
        """
prototype::
    see = self.common_with

    arg = PPath , list(PPath) , tuple(PPath): paths

    return = PPath ;
             a new path which corresponds to the "smaller common folder" of
             the current path and the other ones given in arguments


This magic method allows to use ``path & paths`` instead of the long version
``path.common_with(paths)`` where ``paths`` can be either a single path, or
a list or a tuple of paths.
        """
        return self.common_with(paths)

    def __sub__(self, path):
        """
prototype::
    arg = PPath: path

    return = PPath ;
             a new path which corresponds to the relative path of the current
             one regarding to the path given in the argument ``path``


This magic method allows to use ``path - anotherpath`` instead of the long
version ``path.relative_to(anotherpath)`` given by ``pathlib.Path``. Here are
some examples of use.

pyterm::
    >>> from mistool.os_use import PPath
    >>> main    = PPath("/Users/projetmbc")
    >>> path_1  = PPath("/Users/projetmbc/README")
    >>> path_2  = PPath("/Users/projetmbc/source/misTool/os_use.py")
    >>> path_1 - main
    PPath('README')
    >>> path_2 - main
    PPath('source/misTool/os_use.py')
    >>> path_2 - path_1
    Traceback (most recent call last):
    [...]
    ValueError: '/Users/projetmbc/source/misTool/os_use.py' does not start with
    '/Users/projetmbc/README'
        """
        return self.relative_to(path.normpath)

    def depth_in(self, path):
        """
prototype::
    arg = PPath: path

    return = PPath ;
             the depth of the current path regarding to the one given in the
             argument ``path``


Here are some examples of use.

pyterm::
    >>> from mistool.os_use import PPath
    >>> main    = PPath("/Users/projetmbc")
    >>> path_1  = PPath("/Users/projetmbc/README")
    >>> path_2  = PPath("/Users/projetmbc/source/misTool/os_use.py")
    >>> path_pb = PPath("/NoUser/projects")
    >>> print(path_1.depth_in(main))
    0
    >>> print(path_2.depth_in(main))
    2
    >>> print(path_pb.depth_in(main))
    Traceback (most recent call last):
    [...]
    ValueError: '/NoUser/projects' does not start with '/Users/projetmbc'
        """
        return len(self.relative_to(path.normpath).parts) - 1

# -- WALK AND SEE -- #

    def see(self):
        """
prototype::
    action = this method shows one directory or one file in the OS environment
             by trying to call an associated application
    """
# Nothing to open...
        if not self.is_file() and not self.is_dir():
            raise FileNotFoundError(
                "the following path points nowhere:"
                "\n    + {0}".format(self)
            )

# We need the **string** long normalized version of the path.
        strpath = str(self.normpath)

# Each OS has its own method.
        osname = system()

# Windows
        if osname == OS_WIN:
            if self.is_file():
                os.startfile(strpath)
            else:
                check_call(args = ['explorer', strpath])

# Mac
        elif osname == OS_MAC:
            check_call(args = ['open', strpath])

# Linux
#
# Source :
#     * http://forum.ubuntu-fr.org/viewtopic.php?pid=3952590#p3952590
        elif osname == OS_LINUX:
            check_call(args = ['xdg-open', strpath])

# Unknown method...
        else:
            raise OSError(
                "the opening of the following file in the OS "
                "<< {0} >> is not supported \n    + {0}".format(
                    osname,
                    self
                )
            )

    def walk(self, regpath = "**"):
        """
prototype::
    see = regpath2meta

    arg = str: regpath = "**" ;
          this is a string that follows some rules named regpath rules

    yield = PPath;
            the ``PPath`` are absolute paths of files and directories matching
            the "regpath" pattern (in each folder, the files are always yield
            before the sub folders and the search is always relative)


Let's suppose that we have the following directory having the absolute path
path::``/Users/projetmbc/basic_dir`` in a ¨unix system.

dir::
    + basic_dir
        * latex_1.tex
        * latex_2.tex
        * python_1.py
        * python_2.py
        * python_3.py
        * python_4.py
        * text_1.txt
        * text_2.txt
        * text_3.txt
        + empty_dir
        + sub_dir
            * code_A.py
            * code_B.py
            * slide_A.pdf
            * slide_B.pdf
            + sub_sub_dir
                * doc.pdf


By default, you will have from lower depth to higher files following by folders.
Let's see this in action.

pyterm::
    >>> from mistool.os_use import PPath
    >>> folder = PPath("/Users/projetmbc/basic_dir")
    >>> for p in folder.walk():
    ...     print("+", p)
    ...
    + /Users/projetmbc/basic_dir/latex_1.tex
    + /Users/projetmbc/basic_dir/latex_2.tex
    + /Users/projetmbc/basic_dir/python_1.py
    + /Users/projetmbc/basic_dir/python_2.py
    + /Users/projetmbc/basic_dir/python_3.py
    + /Users/projetmbc/basic_dir/python_4.py
    + /Users/projetmbc/basic_dir/text_1.txt
    + /Users/projetmbc/basic_dir/text_2.txt
    + /Users/projetmbc/basic_dir/text_3.txt
    + /Users/projetmbc/basic_dir/empty_dir
    + /Users/projetmbc/basic_dir/sub_dir
    + /Users/projetmbc/basic_dir/sub_dir/code_A.py
    + /Users/projetmbc/basic_dir/sub_dir/code_B.py
    + /Users/projetmbc/basic_dir/sub_dir/slide_A.pdf
    + /Users/projetmbc/basic_dir/sub_dir/slide_B.pdf
    + /Users/projetmbc/basic_dir/sub_dir/sub_sub_dir
    + /Users/projetmbc/basic_dir/sub_dir/sub_sub_dir/doc.pdf


Here are others easy examples where the regpath ``"*"`` is for a non-recursive
search contrary to the regpath ``"**"`` which is the default value (see the
preceding example). Just take a look at the documentation of the method
``regpath2meta`` for more ¨infos about regpaths.

pyterm::
    >>> from mistool.os_use import PPath
    >>> folder = PPath("/Users/projetmbc/basic_dir")
    >>> for p in folder.walk("dir::**"):
    ...     print("+", p)
    ...
    + /Users/projetmbc/basic_dir/empty_dir
    + /Users/projetmbc/basic_dir/sub_dir
    + /Users/projetmbc/basic_dir/sub_dir/sub_sub_dir
    >>> for p in folder.walk("file::**.py"):
    ...     print("+", p)
    ...
    + /Users/projetmbc/basic_dir/python_1.py
    + /Users/projetmbc/basic_dir/python_2.py
    + /Users/projetmbc/basic_dir/python_3.py
    + /Users/projetmbc/basic_dir/python_4.py
    + /Users/projetmbc/basic_dir/sub_dir/code_A.py
    + /Users/projetmbc/basic_dir/sub_dir/code_B.py
    >>> for p in folder.walk("file::*.py"):
    ...     print("+", p)
    ...
    + /Users/projetmbc/basic_dir/python_1.py
    + /Users/projetmbc/basic_dir/python_2.py
    + /Users/projetmbc/basic_dir/python_3.py
    + /Users/projetmbc/basic_dir/python_4.py


info::
    If you want to see the existing files and/or folders that do not match the
    regpath, you will have to use the query ``xtra`` together with the "hidden"
    attribut ``_tag`` (the class ``DirView`` of the module ``term_use`` uses
    this). Here is an example of use.

    pyterm::
        >>> from mistool.os_use import PPath
        >>> folder = PPath("/Users/projetmbc/dir")
        >>> for p in folder.walk("xtra file::**.py"):
        ...     print("+", p._tag, ">>>", p)
        ...
        + file >>> /Users/projetmbc/basic_dir/python_1.py
        + file >>> /Users/projetmbc/basic_dir/python_2.py
        + file >>> /Users/projetmbc/basic_dir/python_3.py
        + file >>> /Users/projetmbc/basic_dir/python_4.py
        + file_others >>> /Users/projetmbc/basic_dir/...
        + file >>> /Users/projetmbc/basic_dir/sub_dir/code_A.py
        + file >>> /Users/projetmbc/basic_dir/sub_dir/code_B.py
        + file_others >>> /Users/projetmbc/basic_dir/sub_dir/...
        + file_others >>> /Users/projetmbc/basic_dir/sub_dir/sub_sub_dir/...

    The special names are stored in the following global string variables to be
    used so as to avoid typing errors.

        * ``FILE_TAG``
        * ``FILE_OTHERS_TAG``
        * ``DIR_TAG``
        * ``DIR_OTHERS_TAG``
        """
# Do we have an existing directory ?
        if not self.is_dir():
            raise NotADirectoryError(
                "the following path doesn't point to a directory :"
                "\n    + {0}".format(self)
            )

# Metadatas and the normal regex
        queries, pattern = regpath2meta(
            regpath = regpath,
            sep     = self._flavour.sep
        )

        maindir = str(self)

        notkeepdir  = DIR_TAG not in queries
        notkeepfile = FILE_TAG not in queries
        notkeepall  = ALL_DISPLAY not in queries
        addextra    = XTRA_DISPLAY in queries

        regex_obj = re.compile(pattern)

# Matching or non-matching, that is the question !
        if NOT_QUERY in queries:
            match = lambda x: not regex_obj.match(x)

        else:
            match = lambda x: regex_obj.match(x)

# Let's walk
        for root, dirs, files in os.walk(maindir):
# The matching paths
            for tag, strpaths in [
                (FILE_TAG, files),
                (DIR_TAG,  dirs)
            ]:
                if tag == FILE_TAG and notkeepfile:
                    continue

                if tag == DIR_TAG and notkeepdir:
                    continue

                nomatchingfiles_found = False

                for strpath in strpaths:
                    if strpath.startswith('.') and notkeepall:
                        continue

                    absppath = os.path.join(root, strpath)
                    absppath = PPath(absppath)

                    absppath._tag = tag

                    strrelpath = str(absppath.relative_to(self))

                    if match(strrelpath):
                        yield absppath

                    elif tag == FILE_TAG:
                        nomatchingfiles_found = True

                    else:
                        absppath._tag = DIR_OTHERS_TAG

                        yield absppath

# No matching files founds
                if addextra and nomatchingfiles_found:
                    absppath = os.path.join(root, FILE_DIR_OTHERS_NAME)
                    absppath = PPath(absppath)

                    absppath._tag = FILE_OTHERS_TAG

                    yield absppath

# -- CREATE -- #

    def create(self, kind):
        """
prototype::
    arg = str: kind in [FILE_TAG, DIR_TAG]

    action = this method creates the file or the directory having the current
             path except if this path points to an existing directory or file
             respectively.


Here is an example of creations relatively to a current directory having path
path::``/Users/projetmbc``, and containing no subfolder (you can see that some
exceptions can be raised).

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
    [...]
    ValueError: path points to an existing file.


info::
    All the parent directories that don't yet exist are automatically created.
        """
# Good kind.
        kind = LONG_REGPATH_QUERIES.get(kind, kind)

        if kind not in FILE_DIR_QUERY:
            raise ValueError("illegal kind.")

# A new directory.
        if kind == DIR_TAG:
            if self.is_file():
                raise FileExistsError("path points to an existing file.")

            elif not self.is_dir():
                self.mkdir(parents = True)

# A new file.
        elif self.is_dir():
            raise IsADirectoryError("path points to an existing directory.")

        elif not self.is_file():
            parent = self.parent

            if not parent.is_dir():
                parent.mkdir(parents = True)

            with self.open(mode = "w") as f:
                ...

# -- REMOVE -- #

    def can_be_removed(self, safemode = True):
        """
prototype::
    arg = bool: safemode = True ;
          using ``safemode = True`` protects any existing file or directory
          whereas ``safemode = True`` makes any file or directory removable

    action = if the file or the directory can't be removed regarding to the
    value of ``safemode``, an OS error is raised.
        """
        if safemode:
            if self.is_file():
                raise FileExistsError(
                    "existing file can't be removed with ``safemode = True`` "
                    "(use ``safemode = False`` to force the erasing)"
                )

            elif self.is_dir():
                raise IsADirectoryError(
                    "existing folder can't be removed with ``safemode = True`` "
                    "(use ``safemode = False`` to force the erasing)"
                )

    def remove(self):
        """
prototype::
    see = self.can_be_removed

    action = this method removes the directory or the file corresponding to
             the current path


warning::
    Removing a directory will destroy anything within it using a recursive
    destruction of all subfolders and subfiles.
        """
        if self.is_dir():
            shutil.rmtree(str(self))

        elif self.is_file():
            self.unlink()

        else:
            raise FileNotFoundError(
                "the following path points nowhere :"
                "\n    + {0}".format(self)
            )

    def clean(self, regpath):
        """
prototype::
    see = regpath2meta

    arg = str: regpath ;
          this is a string that follows some rules named regpath rules

    action = every files and directories matching ``regpath`` are removed
        """
# We have to play with the queries and the pattern in ``regpath``.
        queries, pattern = regpath2meta(
            regpath = regpath,
            sep     = self._flavour.sep,
            regexit = False)

        if ALL_DISPLAY in queries:
            prefix = ALL_DISPLAY

        else:
            prefix = ""

# We must first remove the files. This is in case of folders to destroy.
        if FILE_TAG in queries:
            filepattern = "{0} file::{1}".format(prefix, pattern)

            for path in self.walk(filepattern):
                path.remove()

# Now, we can destroy folders but we can use an iterator (because of sub
# directories).
        if DIR_TAG in queries:
            dirpattern = "{0} dir::{1}".format(prefix, pattern)

# << Warning ! >> We have to be carefull with directories and sub folders.
            sortedpaths = sorted(list(p for p in self.walk(dirpattern)))

# << Warning ! >> We have to be carefull with empty directories.
            for path in sortedpaths:
                path.remove()

# -- MOVE & COPY -- #

    def copy_to(self, dest, safemode = True):
        """
prototype::
    arg = PPath: dest
    arg = bool: safemode = True;
          this argument is a security to avoid the erasing of an existing file
          or directory. This allows the savy developer to erase file or
          directory during a copy by using ``safemode = False``

    action = if the current ``PPath`` is an existing file or directory, the
             method will copy it to the destination given by the argument
             ``path``


warning::
     The use of ``safemode = False`` will erase **everything** at the
     destination path.
     """
# Is the copy allowed ?
        dest.can_be_removed(safemode)

# We have to use a clean way !
        try:
# Copy of a file.
            if self.is_file():
                dest.parent.create(DIR_TAG)

                shutil.copy(str(self), str(dest))

# Copy of a directory.
#
# WARNING !!! We can't call the method ``create`` during the recursive walk !
            elif self.is_dir():
                if self == self & dest:
                    oserror = True

                    raise OSError(
                        "copy of a directory inside one of its sub directory "
                        "is not supported (be aware of recursive copying)"
                    )

                dest.parent.create(DIR_TAG)

                for onepath in self.walk():
                    relpath  = onepath - self
                    destpath = dest / relpath

                    if onepath.is_file():
                        onepath.copy_to(
                            dest     = destpath,
                            safemode = safemode
                        )

                    elif onepath.is_empty():
                        destpath.create(DIR_TAG)

# Path points nowhere !
            else:
                oserror = False

                raise FileNotFoundError(
                    "the following path points nowhere:"
                    "\n    + {0}".format(self)
                )

# Erase anything in case of any OS problem...
        except (OSError, FileNotFoundError) as e:
            if dest.is_file() or dest.is_dir():
                dest.remove()

            if oserror:
                raise OSError(e)

            else:
                raise FileNotFoundError(e)

    def move_to(self, dest, safemode = True):
        """
prototype::
    arg = PPath: dest
    arg = bool: safemode = True;
          this argument is a security to avoid the erasing of an existing file
          or directory. This allows the savvy developer to erase file or
          directory during a move by using ``safemode = False``

    action = this method moves the current file to the destination given by
             the argument ``path``


info::
    If the source and the destination have the same parent directory, then the
    final result will be at the end a renaming of the file or the directory.


warning::
    The use of ``safemode = False`` will erase **everything** at the destination
    path.
        """
# Moving a file...
        if self.is_file():
            self.copy_to(
                dest     = dest,
                safemode = safemode
            )

# Let's be cautious...
            if dest.is_file():
                self.remove()

            else:
                raise OSError("moving the file has failed.")

# Moving a directory...
        elif self.is_dir():
            self.copy_to(
                dest     = dest,
                safemode = safemode
            )

# Let's be cautious...
            if dest.is_dir():
                self.remove()

            else:
                raise OSError("moving the diretory has failed.")

        else:
            raise FileNotFoundError(
                "the following path points nowhere."
                "\n    + {0}".format(self)
            )


# --------------- #
# -- LAUNCHING -- #
# --------------- #

# Source :
#    * http://docs.python.org/py3k/library/subprocess.html
_SUBPROCESS_METHOD = {
# ``check_call`` prints informations given during the compilation.
    True : check_call,
# ``check_output`` does not print informations given during the
# compilation. Indeed it returns all this stuff in one string.
    False: check_output
}

def runthis(
    cmd,
    showoutput = False
):
    """
prototype::
    see = cd, PPath.is_protected

    arg = str: cmd ;
          a single string that can contain several commands separated by
          spaces as in a ¨unix terminal
    arg = bool: showoutput ;
          by default, ``showoutput = False`` asks to not show what the script
          launched by the command prints

    return = str ;
             this function runs the commands indicated in ``cmd``, and then it
             returns either an empty string if ``showoutput = False``, or the
             output of the process (a string that we encode in ¨utf8)


For our example, let's consider the basic following script which has the path
path::``/Users/projetmbc/script.py``.

python::
    print("Everything is ok.")


Then we can launch this program like in the following lines. You can see that
by default nothing is printed, so you have to use ``showoutput = True`` if
you want to see what the script launched prints.

pyterm::
    >>> from mistool.os_use import PPath, runthis
    >>> pyfile = PPath("/Users/projetmbc/script.py")
    >>> runthis(cmd = "python3 {0}".format(ppath))
    >>> runthis(cmd = "python3 {0}".format(ppath), showoutput = True)
    Everything is ok.


info::
    For arguments containing spaces you can either escape the spaces using
    ``\ ``, or put this arguments inside quotes like on ¨unix systems. You
    can use ``python_use.quote`` to put easily a spaced command inside quotes.
    """
# ``shlex.split`` takes care of escaped spaces and quotes.
    cmd_args = shlex.split(
        s     = cmd,
        posix = True
    )

# We keep the current working directory and use the terminal actions.
    fromprocess = _SUBPROCESS_METHOD[showoutput](args = cmd_args)

# ``check_output`` being a byte string, we have to use ``decode('utf8')`` so as
# to obtain an "utf-8" string.
    if showoutput:
        fromprocess = ""

    else:
        fromprocess = fromprocess.decode('utf8').strip()

    return fromprocess
