#!/usr/bin/env python3

"""
prototype::
    date = 2016-02-15


The main feature of this module is the class ``PPath`` which is an enhanced
version of the standard class ``pathlib.Path`` that allows to manipulate easily
paths and as a consequence files and folders.

There are also other small useful functions like ``runthis`` that really
simplify the use of a command line from ¨python codes.
"""

import os
import pathlib
import platform
from random import randint
import re
import shlex
import shutil
from subprocess import check_call, check_output


# ------------------- #
# -- GENERAL INFOS -- #
# ------------------- #

SEP = os.sep

def pathenv():
    """
prototype::
    return = str ;
             the variable ``PATH`` that contains paths of some executables
             known by your OS
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
        return "mac"

    else:
        return osname.lower()


# -------------------------------- #
# -- CHANGING CURRENT DIRECTORY -- #
# -------------------------------- #

class cd:
    """
prototype::
    type = self ;
           this class i a context manager that allows to easily change the
           current directory as this can be done using term::``cd`` in a ¨unix
           system, or term::``chdir`` in a ¨win sytem

    arg-attr = PPath: ppath ;
               this gives the path where to go


Let's suppose that we have the following directory having the full path
path::``/Users/projects/basic_dir`` in a ¨unix system.

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
    >>> with cd("/Users/projects/basic_dir"):
    ...     subprocess.call("ls")
    empty_dir	python_1.py	python_4.py	text_2.txt
    latex_1.tex	python_2.py	sub_dir		text_3.txt
    latex_2.tex	python_3.py	text_1.txt
    >>> with cd("/Users/projects/basic_dir/sub_dir"):
    ...     subprocess.call("ls")
    code_A.py	slide_A.pdf	sub_sub_dir
    code_B.py	slide_B.pdf


info::
    All the code comes from cf::``this post ; http://stackoverflow.com/a/13197763/4589608``.
"""
    def __init__(self, ppath):
        self._newstrpath = str(ppath.normpath)

    def __enter__(self):
        self._savedpath = os.getcwd()
        os.chdir(self._newstrpath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self._savedpath)


# ------------------------ #
# -- OUR ENHANCED CLASS -- #
# ------------------------ #

# Sublcassing ``pathlib.Path`` is not straightforward ! The following post gives
# the less ugly way to do that.
#
# Source :
#     * http://stackoverflow.com/a/34116756/4589608

class PPath(type(pathlib.Path())):
    """
prototype::
    type = self ;
           this class adds some functionalities to the standard class
           ``pathlib.Path``

    see = pathlib.Path
    """
# -- CONSTANTS FOR REGPATHS -- #

# Sources for the regex:
#
#     * http://stackoverflow.com/a/430781/4589608
#     * http://stackoverflow.com/a/30439865/4589608
#     * http://stackoverflow.com/a/817117/4589608
#     * http://stackoverflow.com/questions/20294704/which-pattern-has-been-found/20294987

    _FILE, _DIR, _EMPTY, _OTHER_FILES \
    = "file", "dir", "empty_dir", "dir_other_files"

    _ALL, _NOT, _RELSEARCH, _XTRA \
    = "all", "not", "relative", "xtra"

    _PATH_QUERIES = set([_DIR, _EMPTY, _FILE, _ALL, _NOT, _RELSEARCH, _XTRA])

    _LONG_PATH_QUERIES = {x[0]: x for x in _PATH_QUERIES}
    _FILE_DIR_QUERIES  = set([_DIR, _FILE])

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

# -- CONSTANTS FOR CREATION -- #

    _ALL_CREATE_KINDS  = set([_FILE, _DIR])
    _LONG_CREATE_KINDS = {x[0]: x for x in _ALL_CREATE_KINDS}


# -- ABOUT -- #

    def is_empty(self):
        """
prototype::
    return = bool ;
             if ``PPath`` is not an existing directory an error is raised, but
             if the ``PPath`` points to an empty directory, ``False`` is
             returned, otherwise that is ``True`` that is returned
         """
        if not self.is_dir():
            raise OSError("the path does not point to an existing directory")

        for onepath in self.walk():
            return False

        return True


    @property
    def parent(self):
        """
prototype::
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
        return self.parents[0]


    @property
    def depth(self):
        """
prototype::
    return = int ;
             the absolute depth of a path


Here is an example of use.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path = PPath("/Users/projects/source/misTool/os_use.py")
    >>> print(path.depth)
    4
        """
        return len(self.parents) - 1


    @property
    def ext(self):
        """
prototype::
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


# -- MODIFYING A PATH -- #

    def with_ext(self, ext):
        """
prototype::
    arg = str: ext ;
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
folder is path::``/Users/projects``. The ``PosixPath`` refers to the Unix
version of ``PPath``.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path = PPath("~/dir_1/dir_2/dir_3/../../file.txt")
    >>> path.normpath
    PosixPath('/Users/projects/dir_1/file.txt')
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
path::``/Users/projects`` is the user's folder. The ``PosixPath`` refers to
the Unix version of ``PPath``.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path = PPath("/Users/projetmbc/dir_1/dir_2/dir_3/../../file.txt")
    >>> path.shortpath
    PosixPath('~/dir_1/file.txt')
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
version ``path.relative_to(anotherpath)`` given by ``pathlib.Path``.
        """
        return self.relative_to(path)


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
    [...]
    ValueError: '/NoUser/projects' does not start with '/Users/projects'
        """
        return len(self.relative_to(path).parts) - 1


# -- FOR THE REGPATHS -- #

    def regexit(self, pattern):
        """
prototype::
    arg = str: pattern ;
          ``pattern`` is a pattern using the regpath syntax which tries to
          catch the best of the regex and the Unix-glob syntaxes (no special
          queries here)

    return = str ;
             a regex uncompiled version of ``pattern``.
    """
        onestar2regex = self._REPLACEMENTS[self._flavour.sep]

        newpattern = ""
        lastpos    = 0

        for m in self._RE_SPECIAL_CHARS.finditer(pattern):
            spechar = m.group()

            if spechar not in self._SPE_CHARS:
                raise ValueError("too much consecutive stars ''*''")

            spechar     = self._REPLACEMENTS.get(spechar, onestar2regex)
            newpattern += pattern[lastpos:m.start()] + spechar
            lastpos     = m.end()

        newpattern += pattern[lastpos:]

        return newpattern


    def regpath2meta(self, regpath, regexit = True):
        """
prototype::
    arg = str: regpath ;
          ``regpath`` uses a syntax trying to catch the best of the regex and
          the Unix-glob syntaxes with some little extra features
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

Before two double points, you can use the following queries separated by
spaces.

    1) ``not`` is very useful because it allows simply to look for something
    that does not match the pattern (you have to know that negation with regexes
    can be a little messy).

    2) ``file`` asks to keep only files.

    3) ``dir`` asks to keep only folders.

    4) ``all`` asks to keep also the hidden files and folders. This ones have
    a name begining with a point.

    5) ``all file`` asks to keep only files even the hidden ones. You can also
    use ``all dir``.

    6) ``empty`` allows to only look for empty folders which are by default the
    ones with no visible content (this can be useful for some cleaning).

    By cons, you can target your research via ``all empty`` so that folders
    containing only invisible objects are not considered empty.

    7) ``relative`` indicates that the pattern after ``::`` is relatively to
    the current directory and not to a full path.

    8) ``xtra`` add respectively special names path::``::...files...::``
    and path::``::...empty...::`` whenever some files have been found but not
    kept or a folder is empty (this feature is used by the class ``DirView``).


For example, to keep only the Python files, in a folder or not, just use
``"file::**.py"``. This is not the same that ``"**.py"`` which will also catch
folders with a name finishing by path::``.py`` (that is legal).


info::
    For each query, you can only use its initial letter. For example, ``f`` is
    a shortcut for ``file``, and ``a f`` is the same that ``all file``.
    """
        queries, *pattern = regpath.split("::")

        if len(pattern) > 1:
            raise ValueError("too much \"::\" in the regpath.")

# Two pieces
        if pattern:
            pattern = pattern[0]

            queries = set(
                self._LONG_PATH_QUERIES.get(x.strip(), x.strip())
                for x in queries.split(" ")
            )

            if not queries <= self._PATH_QUERIES:
                raise ValueError("illegal filter(s) in the regpath.")

# One single piece
        else:
            queries, pattern = self._FILE_DIR_QUERIES, queries

# The query "empty" is used.
        if self._EMPTY in queries:
            if self._FILE in queries:
                raise ValueError(
                    'filters "empty" and "file" can\'t be used together.'
                )

            queries.add(self._DIR)

# The queries "file" and "dir" are not used.
        elif self._FILE not in queries and self._DIR not in queries:
            queries |= self._FILE_DIR_QUERIES

# The regex uncompiled version : we just do replacing by taking care of
# the escaping character. We play with regexes to do that.
#
# << Warning : >> ***, ****, ... are not allowed !

        if regexit:
            pattern = "^{0}$".format(self.regexit(pattern))

        return queries, pattern


# -- WALK AND SEE -- #

    def __tagsreturnedbywalk(self, ppath, tag, givetags):
        if givetags:
            return ppath, tag
        else:
            return ppath


    def walk(
        self,
        regpath  = "relative::**",
        givetags = False
    ):
        """
prototype::
    arg = str: regpath = "relative::**" ;
          this is a string that follows some rules named regpath rules (see
          the documentation of the function ``_ppath_regpath2meta``)
    arg = bool: givetags = False ;
          by default, the walk yields only ``PPath``, but if you use ``givetags
          = True``, then the walk yields a couple made of a ``PPath`` and an
          additional tag to know which kind of ``PPath`` has been yield

    yield = if givetags == False then PPath else (PPath, str);
            the ``PPath`` are whole path of files and directories matching the
            "regpath" pattern (in each folder, the files are always yield before
            the sub folders), and the strings are tags that can be "file",
            "dir", "empty_dir" or "dir_other_files" (this is an additional
            information that is used by the class ``term_use.DirView``)


Let's suppose that we have the following directory having the full path
path::``/Users/projects/basic_dir`` in a ¨unix system.

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


Here are three examples of use where you can see that the regpaths ``"*"`` and
``"**"`` don't do the same thing : there are two much files with ``"**"``. Just
go to the documentation of the function ``_ppath_regpath2meta`` so as to know
why (you have to remember that by default the search is relative).

pyterm::
    >>> from mistool.os_use import PPath
    >>> folder = PPath("/Users/projects/dir")
    >>> for p in folder.walk("dir::**"):
    ...     print("+", p)
    ...
    + /Users/projects/basic_dir/empty_dir
    + /Users/projects/basic_dir/sub_dir
    + /Users/projects/basic_dir/sub_dir/sub_sub_dir
    >>> for p in folder.walk("**.py"):
    ...     print("+", p)
    ...
    + /Users/projects/basic_dir/python_1.py
    + /Users/projects/basic_dir/python_2.py
    + /Users/projects/basic_dir/python_3.py
    + /Users/projects/basic_dir/python_4.py
    + /Users/projects/basic_dir/sub_dir/code_A.py
    + /Users/projects/basic_dir/sub_dir/code_B.py
    >>> for p in folder.walk("relative file::*.py"):
    ...     print("+", p)
    ...
    + /Users/projects/basic_dir/python_1.py
    + /Users/projects/basic_dir/python_2.py
    + /Users/projects/basic_dir/python_3.py
    + /Users/projects/basic_dir/python_4.py


info::
    If you want to see the existing files that do not match the regpath and also
    the empty folders, you will have to use the query ``xtra`` together with
    ``givetags = True`` (this feature is used  by the class ``DirView``). Here
    is an example.

    pyterm::
        >>> from mistool.os_use import PPath
        >>> folder = PPath("/Users/projects/dir")
        >>> for p, tag in folder.walk(
        ...     regpath = "xtra file::**.py",
        ...     givetags = True
        ... ):
        ...     print("+", tag, ">>>", p)
        ...
        + file >>> /Users/projects/basic_dir/python_1.py
        + file >>> /Users/projects/basic_dir/python_2.py
        + file >>> /Users/projects/basic_dir/python_3.py
        + file >>> /Users/projects/basic_dir/python_4.py
        + dir_other_files >>> /Users/projects/basic_dir
        + empty_dir >>> /Users/projects/basic_dir/empty_dir
        + file >>> /Users/projects/basic_dir/sub_dir/code_A.py
        + file >>> /Users/projects/basic_dir/sub_dir/code_B.py
        + dir_other_files >>> /Users/projects/basic_dir/sub_dir
        + dir_other_files >>> /Users/projects/basic_dir/sub_dir/sub_sub_dir

    The special names are stored in the global variables ``self._FILE``, ``self._DIR``,
    ``self._EMPTY`` and ``self._OTHER_FILES`` which are strings.
    This is useful to avoid typing errors if you want to use the query ``xtra``
    together with ``givetags = True`` as the class ``DirView`` does.
        """
# Do we have an existing directory ?
        if not self.is_dir():
            raise OSError("the path doesn't point to a directory.")

# metadatas and the normal regex
        queries, pattern = self.regpath2meta(regpath)

        maindir   = str(self)
        keepdir   = self._DIR in queries
        keepfile  = self._FILE in queries
        keepempty = self._EMPTY in queries
        keepall   = self._ALL in queries
        relsearch = self._RELSEARCH in queries
        addextra  = self._XTRA in queries

        regex_obj = re.compile(pattern)

# Matching or unmatching, that is the question !
        if self._NOT in queries:
            match = lambda x: not regex_obj.match(x)

        else:
            match = lambda x: regex_obj.match(x)

# Let's walk
        for root, dirs, files in os.walk(maindir):
# Empty folders and unkept files
            isdirempty         = not(bool(dirs) or bool(files))
            nomatch_files_found = False

# Do the current directory must be added ?
            addthisdir = False
            root_ppath = PPath(root)

            if keepempty:
                if isdirempty:
                    addthisdir = True

            elif keepdir and root != maindir and match(root):
                if keepall \
                or not any(
                    x.startswith('.')
                    for x in root_ppath.relative_to(self).parts
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
                        rel_file = str(ppath_full_file.relative_to(self))

                        if match(rel_file):
                            yield self.__tagsreturnedbywalk(
                                ppath    = ppath_full_file,
                                tag      = self._FILE,
                                givetags = givetags
                            )

                        else:
                            nomatch_files_found = True

                    elif match(full_file):
                        yield self.__tagsreturnedbywalk(
                            ppath    = PPath(full_file),
                            tag      = self._FILE,
                            givetags = givetags
                        )

                    else:
                        nomatch_files_found = True

# A new directory ?
            if addthisdir:
                if isdirempty:
                    tag = self._EMPTY

                else:
                    tag = self._DIR

                yield self.__tagsreturnedbywalk(
                    ppath    = root_ppath,
                    tag      = tag,
                    givetags = givetags
                )

            elif addextra:
                if isdirempty:
                    tag = self._EMPTY

                elif nomatch_files_found:
                    tag = self._OTHER_FILES

                else:
                    tag = self._DIR

                yield self.__tagsreturnedbywalk(
                    ppath    = root_ppath,
                    tag      = tag,
                    givetags = givetags
                )


    def see(self):
        """
prototype::
    action = this method shows one directory or one file in the OS environment
             by trying to call an associated application
    """
# Nothing to open...
        if not self.is_file() and not self.is_dir():
            raise OSError("the path points nowhere.")

# We need the **string** long normalized version of the path.
        strpath = str(self.normpath)

# Each OS has its own method.
        osname = system()

# Windows
        if osname == "windows":
            if self.is_file():
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


# -- CREATE -- #

    def create(self, kind):
        """
prototype::
    arg = str: kind in [self._FILE, self._DIR]

    action = this method creates the file or the directory having the current
             path except if this path points to an existing directory or file
             respectively.


Here is an example of creations relatively to a current directory having path
path::``/Users/projects``. You can see that some exceptions can be raised.

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
        kind = self._LONG_CREATE_KINDS.get(kind, kind)

        if kind not in self._ALL_CREATE_KINDS:
            raise ValueError("illegal kind.")

# A new directory.
        if kind == self._DIR:
            if self.is_file():
                raise ValueError("path points to an existing file.")

            elif not self.is_dir():
                os.makedirs(str(self))

# A new file.
        elif self.is_dir():
            raise ValueError("path points to an existing directory.")

        elif not self.is_file():
            self.parent.create(self._DIR)

            with self.open(mode = "w") as file:
                ...


# -- REMOVE -- #

    def can_be_removed(self, safemode):
        """
prototype::
    arg = bool: safemode ;
          using ``safemode = True`` protects any existing file or directory
          whereas ``safemode = True`` makes any file or directory removable

    action = if the file or the directory can't be removed regarding to the
    value of ``safemode``, an OS error is raised.
        """
        if safemode:
            if self.is_file():
                raise OSError(
                    "impossible to remove the file (use ``safemode = False`` "
                    "to force the erasing)"
                )

            elif self.is_dir():
                raise OSError(
                    "impossible to remove the directory (use ``safemode = False`` "
                    "to force the erasing)"
                )


    def remove(self):
        """
prototype::
    action = this method removes the directory or the file corresponding to
             the current path


warning::
    Removing a directory will destroy anything within it using a recursive
    destruction of all subfolders and subfiles.
        """
        if self.is_dir():
            shutil.rmtree(str(self))

        elif self.is_file():
            os.remove(str(self))

        else:
            raise OSError("path points nowhere.")


    def clean(self, regpath):
        """
prototype::
    arg = str: regpath ;
          this is a string that follows some rules named regpath rules (see
          the documentation of the function ``_ppath_regpath2meta``)

    action = every files and directories matching ``regpath`` are removed
        """
# We have to play with the queries and the pattern in ``regpath``.
        queries, pattern = self.regpath2meta(regpath, regexit = False)

        if self._ALL in queries:
            prefix = "all"

        elif self._EMPTY in queries:
            prefix = "empty"

        else:
            prefix = ""

# We must first remove the files. This is in case of folders to destroy.
        if self._FILE in queries:
            filepattern = "{0} file::{1}".format(prefix, pattern)

            for path in self.walk(filepattern):
                path.remove()

# Now, we can destroy folders but we can use an iterator (because of sub
# directories).
        if self._DIR in queries:
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
          or directory. This allows the savvy developer to erase file or
          directory during a copy by using ``safemode = False``

    action = if the current ``PPath`` is an existing file or directory, the
             method will copy it to the destination given by the argument
             ``path``


warning::
     The use of ``safemode = False`` will erase **everything** at the destination
     path.
     """
# Is the copy allowed ?
        dest.can_be_removed(safemode)

# We have to use a clean way !
        try:
# Copy of a file.
            if self.is_file():
                dest.parent.create(self._DIR)

                shutil.copy(str(self), str(dest))

# Copy of a directory.
#
# WARNING !!! We can't call the method ``create`` during the recursive walk !
            elif self.is_dir():
                print("self & dest", self & dest)
                if self == self & dest:
                    raise OSError(
                        "copy of a directory inside one of its sub directory "
                        "is not supported (be aware of recursive copying)"
                    )

                dest.parent.create(self._DIR)

                for onepath in self.walk():
                    relpath  = onepath - self
                    destpath = dest / relpath

                    if onepath.is_file():
                        onepath.copy_to(
                            dest     = destpath,
                            safemode = safemode
                        )

                    elif onepath.is_empty():
                        destpath.create(self._DIR)

# Path points nowhere !
            else:
                raise OSError("destination path points nowhere.")

# Erase anything in case of any OS problem...
        except OSError as e:
            if dest.is_file() or dest.is_dir():
                dest.remove()

            raise OSError(e)


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
            raise OSError("current path points nowhere.")


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
    ppath      = None,
    showoutput = False
):
    """
prototype::
    arg = str: cmd ;
          a single string that can contain several commands separated by
          spaces as in a terminal
    arg = None, PPath: ppath = None ;
          this argument can be either ``None`` for standalone commands, or
          one path of a directory or a file on which the command ``cmd`` acts
    arg = bool: showoutput ;
          by default, ``showoutput = False`` asks to not show what the script
          launched by the command prints

    return = str ;
             this function runs the commands indicated in ``cmd`` to the file or
             directory indicated via ``ppath`` and also returns either an empty
             string if ``showoutput = False``, or the output of the process (a
             string that we encode in ¨utf8)


For our example, let's consider the basic following script which has the path
path::``/Users/projects/script.py``.

python::
    print("Everything is ok.")


Then we can launch this program like in the following lines. You can see that by
default, nothing is printed, so you have to use ``showoutput = True`` if you
want to see what the script launched prints.

pyterm::
    >>> from mistool.os_use import PPath, runthis
    >>> pyfile = PPath("/Users/projects/script.py")
    >>> runthis(cmd = "python3", ppath = pyfile)
    >>> runthis(cmd = "python3", ppath = pyfile, showoutput = True)
    Everything is ok.


info::
    For arguments containing spaces you can either escape the spaces using
    ``\ ``, or put this arguments inside quotes.
    """
# ``shlex.split`` takes care of escaped spaces and quotes.
    cmd_args = shlex.split(
        s     = cmd,
        posix = True
    )

# Commands that act one a file or a folder.
    if ppath != None:
        cmd_args.append('"{0}"'.format(ppath))

        fromprocess = _SUBPROCESS_METHOD[showoutput](
# We go in the directory of the file to compile.
            cwd = str(ppath.parent),
# We use the terminal actions.
            args = cmd_args
        )

# Standalone commands.
    else:
# We just use the terminal actions.
        fromprocess = _SUBPROCESS_METHOD[showoutput](args = cmd_args)

# ``check_output`` being a byte string, we have to use ``decode('utf8')`` so as
# to obtain an "utf-8" string.
    if showoutput:
        fromprocess = ""

    else:
        fromprocess = fromprocess.decode('utf8').strip()

    return fromprocess


def canmodify(ppath):
    """
prototype::
    arg = PPath; ppath;
          the path of a directory where we want to do some changes

    action = this function tests if the script can act on a folder
    """
    if ppath.is_file():
        ppath = ppath.parent

    tempfile = ppath / '0.t.e.m.p'

    while tempfile.is_file():
        tempfile = tempfile.parent / '{0}.t.e.m.p'.format(randint(500))

    try:
        tempfile.create("file")
        tempfile.remove()
        alterable = True

    except:
        alterable = False

    if tempfile.is_file():
        raise OSError(
            "ONE BIG PROBLEM ! You have to remove by yourself the file:" \
            + "\n    * {0}".format(tempfile)
        )

    return alterable
