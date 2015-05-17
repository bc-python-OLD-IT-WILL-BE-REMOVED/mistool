#!/usr/bin/env python3

"""
Directory : mistool
Name      : os_use
Version   : 2015.05
Author    : Christophe BAL
Mail      : projetmbc@gmail.com

This module contains an enhanced version of the classes in ``pathlib`` to
manipulate easily files, directories and so on, and it also contains functions
which give informations about the system.
"""

import os
import pathlib
import shutil
import platform
from subprocess import check_call

from mistool.config.pattern import regpat


# ------------------------------------- #
# -- SPECIAL FUNCTIONS FOR OUR CLASS -- #
# ------------------------------------- #

# << Warning ! >>
#
# Sublcassing ``pathlib.Path`` is not easy ! We have to dirty a little
# our hands. Hints are hidden in the source and especially in the source
# of ``pathlib.PurePath``.
#
# Sources:
#     * http://stackoverflow.com/a/29851079/4589608
#     * https://hg.python.org/cpython/file/151cab576cab/Lib/pathlib.py
#
# Extra methods added to ``PPath`` must be defined using function. We choose to
# use names which all start with ``_ppath_somename`` where ``somename`` will be
# the name in the class ``PPath``.


# ----------- #
# -- ABOUT -- #
# ----------- #

@property
def _ppath_parent(cls):                     # DOC OK !!
    """
This attribut like method returns a path of the first depth folder "containing"
the file or the directory corresponding to the actual path.


Here is ane example with a ¨mac. The ``PosixPath`` refers to the Unix version
of ``PPath``.

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
This attribut like method returns the extension of a path, that is the value of
the attribut ``suffix`` of ``pathlib.Path`` without the leading point. Here is
an example.

pyterm::
    >>> from mistool.os_use import PPath
    >>> path = PPath("dir/subdir/file.txt")
    >>> print(path.ext)
    'txt'
    """
# An extension is a suffix without the leading point.
    return cls.suffix[1:]


def _ppath_with_ext(cls, ext):              # DOC OK !!
    """
This method changes the extension of a path to the one given in the variable
``ext``. It is similar to the method ``with_suffix`` of ``pathlib.Path`` but
without the leading point. Here is ane example with a ¨mac. The ``PosixPath``
refers to the Unix version of ``PPath``.

pyterm::
    >>> from mistool.os_use import PPath
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
This attribut like method changes the leading shortcut path::``~``
corresponding to the whole name of the default user's directory, and it also
reduces the path::``/../`` used to go higher in the tree structure of a
directory. Then an instance of the class ``PPath`` using this new path is
returned.


Here is an example made on the Mac of the author of ¨mistool. In that case
path::``/Users/projetmbc`` is the user's folder. The ``PosixPath`` refers to
the Unix version of ``PPath``.

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
This attribut like method builds the shorstest version of a path by using the
leading shortcut path::``~`` corresponding to the complete name of the default
user's directory, and by reducing all path::``/../`` used to go higher in the
tree structure of a directory. Then an instance of the class ``PPath`` using
this new path is returned.


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
This method returns the path of the smaller common "folder" of the current path
and at least one paths.


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

        for common, actual in zip(commonparts, path.parts):
            if common == actual:
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


def _ppath___and__(cls, *args):             # DOC OK !!
    """
This magic method allows to use ``path & paths`` instead of the long version
``path.common_with(paths)`` when paths is either a single path, or a list or
a tuple of paths.
    """
    return cls.common_with(*args)


def _ppath___sub__(cls, path):              # DOC OK !!
    """
This magic method allows to use ``path - anotherpath`` instead of the long
version ``path.relative_to(anotherpath)`` given by ``pathlib.Path``.
    """
    return cls.relative_to(path)


def _ppath_depth_in(cls, path):             # DOC OK !!
    """
This method returns the depth of the actual path regarding to another path.


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


# ------------------ #
# -- WALK AND SEE -- #                  # DOC OK !!
# ------------------ #

def _ppath_walk(cls, regpattern = "**"):
    """
This method walks inside a directory using the regpattern to select the paths
of the files and directories to keep.




Here is an example showing of the have only ?????







info::
    When walking in a given folder, the files are always yield before the
    subfolders.


warning::
    You have to see the documentation of the function ``regpat2meta`` in the
    submodule ``config.pattern`` so as to have informations on regpatterns
    (an homemade concept).
    """
# Do we have an existing directory ?
    if not cls.is_dir():
        raise OSError("the path points nowhere.")

# Metadatas and the normal regex
    queries, pattern = regpat2meta(regpattern)

    keepdir     = bool(set(["dir", "d"]) & queries)
    keepfile    = bool(set(["file", "f"]) & queries)
    keepvisible = bool(set(["visible", "v"]) & queries)

    regex_obj = re.compile(pattern)

# Let's walk
    for root, dirs, files in os.walk(str(cls)):

# Do the actual directory must be added ?
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

                file = os.path.join(root, file)

                if regex_obj.match(file):
                    yield PPath(file)

# A new directory ?
        if addthisdir:
            yield root_ppath


def _ppath_see(cls):                        # DOC OK !!
    """
This method shows one directory or one file in the OS environment by trying to
call an associated application.
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

_ALL_KINDS   = set(["file", "dir"])
_SHORT_KINDS = {x[0]: x for x in _ALL_KINDS}

def _ppath_create(cls, kind):               # DOC OK !!
    """
This method creates the file or the directory having the actual path except
if this path points to an existing directory or file respectively.


Here is an example of creations relatively to the current directory showing
that some exceptions can be raised.

pyterm::
    >>> from mistool.os_use import PPath
    >>> file = PPath("test/README")
    >>> file.create("file")
    >>> dir = PPath("test/README")
    >>> dir.create("dir")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/Users/projetmbc/Google Drive/git/python/tools/misTool/mistool/os_use.py", line 317, in _ppath_create
        raise ValueError("path points to an existing file.")
    ValueError: path points to an existing file.


info::
    All the parent directories are automatically created.
    """
# Good kind.
    kind = _SHORT_KINDS.get(kind, kind)

    if kind not in _ALL_KINDS:
        raise ValueError("illegal kind.")

# A new directory.
    if kind == "dir":
        if cls.is_file():
            raise ValueError("path points to an existing file.")

        elif not cls.is_dir():
            os.makedirs(str(cls))

# A new file.
    elif cls.is_dir():
        raise ValueError("path points to an existing directory.")

    elif not cls.is_file():
        cls.parent().create("dir")

        with cls.open(mode = "w") as file:
            ...


# ------------ #
# -- REMOVE -- #
# ------------ #

def _ppath_remove(cls):                     # DOC OK !!
    """
This method removes the directory or the file corresponding to the actual path.


warning::
    Removing a directory will destroy anything within it using a recusrive
    destruction of all subfolders and subfiles.
    """
    if cls.is_dir():
        shutil.rmtree(str(cls))

    elif cls.is_file():
        os.remove(str(cls))

    else:
        raise OSError("path points nowhere.")








# DOC OK !!

def _ppath_clean(cls, regpattern):
    """
This method cleans a directory regarding the value of ``regpattern`` which must
be an almost regex pattern: you have to see the documentation of the function
``regpat2meta`` in the submodule ``config.pattern``.

warning::
    You have to see the documentation of the function ``regpat2meta`` in the
    submodule ``config.pattern`` so as to have informations on regpatterns
    (an homemade concept).
    """
# We have to play with the queries and the pattern in ``regpattern``.
    queries, pattern = regpat2meta(regpattern, regexit = False)

    if "visible" in queries:
        prefix = "visible-"

    else:
        prefix = ""

# We must first remove the files. This is in case of folders to destroy.
    if "file" in queries:
        filepattern = "{0}file::{1}".format(prefix, pattern)

        for path in cls.walk(filepattern):
            path.remove()


# We can destroy folders but we can use an iterator (because of sub directories).
    if "dir" in queries:
        dirpattern = "{0}dir::{1}".format(prefix, pattern)

        sortedpaths = sorted(list(p for p in cls.walk(dirpattern)))

        for path in sortedpaths:
            path.remove()


# ----------------- #
# -- MOVE & COPY -- #
# ----------------- #

def _ppath_copy_to(cls, path):              # DOC OK !!
    """
This method copies the actual file to the destination ``path``. This last path
must be an instance of the class ``pathlib.Path`` or ``PPath``.


info::
    The actual path is not changed.


warning::
    Copy of a directory is not yet supported.
    """
    if cls.is_file():
        parent = path.parent

        if not parent.is_dir():
            parent.create("dir")

        shutil.copy(str(cls), str(path))

    elif cls.is_dir():
        raise ValueError("copy of directories is not yet supported.")

    else:
        raise OSError("path points nowhere.")


def _ppath_move_to(cls, path):              # DOC OK !!
    """
This method moves the actual file to the destination ``path``. This last path
must be an instance of the class ``pathlib.Path`` or ``PPath``.


info::
    If the source and the destination have the same parent directory, then the
    final result will just be a renaming of the file or the directory.


warning::
    The actual path is not changed and moving a directory is not yet supported.
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
        raise OSError("actual path is not a real one.")















# ------------------------ #
# -- OUR ENHANCED CLASS -- #
# ------------------------ #

_SPECIAL_FUNCS = [
    (x[len("_ppath_"):], x)
    for x in dir()
    if x.startswith("_ppath_")
]

class PPath(pathlib.Path):
    """
    hhhh
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

# Source: https://hg.python.org/cpython/file/default/Lib/functools.py#l210
class K(object):
    __slots__ = ['obj']

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

    __hash__ = None

class DirView:
    """
-----------------
Small description
-----------------

This class displays the tree structure of one directory with the possibility to
keep only some relevant informations like in the following example.

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


In this output no invisible directory or file has been printed, and ellipsis
indicates visible files that do not match to a given pattern for the paths.
All of this has been obtained with the following code.

pyterm::
    from mistool.os_use import PPath

    DirView = os_use.DirView(
        ppath      = "/Users/projetmbc/python/mistool",
        regpattern = "visible::*.(py|txt|tex|pdf)",
        display    = "main short"
    )

    print(DirView.ascii)






warning::
    You have to see the documentation of the function ``regpat2meta`` in the
    submodule ``config.pattern`` so as to have informations on regpatterns
    (an homemade concept).




-------------
The arguments
-------------

This class uses the following variables.

    1) ``ppath`` is a path defined using the class ``PPath``.

    2) ``regpattern`` is an optional string which is an almost regex pattern.
    See the documentation of the method ``walk`` of the class ``PPath``. By
    default, ``regpattern = "**"`` which indicates to look for anything.

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
        matches the pattern ``regpattern``. You can use the shortcut ``f``.
    """
    ASCII_DECOS = {
        'dir' : "+",
        'file': "*",
        'tab' : " "*4
    }

    _FORMATTERS = set(["found", "main", "long", "relative", "short"])
    _PATH_FORMATTERS = set(["long", "relative", "short"])
    _SHORT_FORMATTERS = {x[0]: x for x in _FORMATTERS}

    def __init__(
        self,
        ppath,
        regpattern = "**",
        display    = "main short"
    ):
        self.ppath      = ppath
        self.regpattern = regpattern
        self.display    = display

        self._ellipsis = PPath('...')

        self.build()


    def build(self):
        """
This method builds first one flat list ``self.listview`` of dictionaries of the
following kind that will ease the making of the tree view. This list is sorted
in alphabetic order with a depth walk.

pyterm::
    {
        'kind'   : "dir" or "file",
        'depth'  : the depth level regarding to the main directory,
        'relpath': the relative path of one directory or file found
    }
        """
# Reset all things !
        self.listview = []
        self.options  = set()
        self.output   = {}

        self.queries, _ = regpat2meta(
            self.regpattern,
            regexit = False
        )

# What have to be displayed ?
        for opt in self.display.split(" "):
            opt = opt.strip()
            opt = self._SHORT_FORMATTERS.get(opt, opt)

            if opt not in self._FORMATTERS:
                raise ValueError("unknown option for displaying.")

            self.options.add(opt)

        if len(self._PATH_FORMATTERS & self.options) > 1:
            raise ValueError("ambiguous option for printing the paths.")

# We must add all the folders except if the option "found" has been used.
        if "found" not in self.options:
            if "visible" in self.queries:
                prefix = "visible-"

            else:
                prefix = ""

            self.listview = [
                {
                    'kind'   : "dir",
                    'depth'  : p.depth_in(self.ppath),
                    'relpath': p.relative_to(self.ppath)
                }
                for p in self.ppath.walk(prefix + "dir::**")
            ]

# Unsorted flat version of the tree view.
        for path in self.ppath.walk(self.regpattern):
            kind = "file" if path.is_file() else "dir"

            infos = {
                'kind'   : kind,
                'depth'  : path.depth_in(self.ppath),
                'relpath': path.relative_to(self.ppath)
            }

# We do not want to see twice a folder !
            if kind == "file" or infos not in self.listview:
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
                    if infos['kind'] == "file":
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
                        'kind'   : "dir",
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
            if infos['kind'] == "dir":
                for p in (self.ppath / infos['relpath']).iterdir():
                    if p.is_file() \
                    and (
                        "visible" not in self.queries
                        or not p.name.startswith('.')
                    ) \
                    and {
                        'kind'   : "file",
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
                    'kind'   : "file",
                    'depth'  : depth,
                    'relpath': self._ellipsis
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
                    "{0} {1}".format(self.ASCII_DECOS["dir"], mainpath)
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
        if path == self._ellipsis or  "relative" in self.options:
            return str(path)

# We have to rebuild the while path.
        if "long" in self.options:
            return str(self.ppath / path)

# "short" is the default option for printing the paths.
        return str(path.name)


# ------------------- #
# -- GENERAL INFOS -- #
# ------------------- #

def pathenv():
    """
This function simply returns the variable ``PATH`` that contains paths of some
executables known by your OS.
    """
    return os.getenv('PATH')

def system():
    """
The purpose of this function is to give the name, in lower case, of the OS used.
Possible names can be "windows", "mac", "linux" and also "java".
    """
    osname = platform.system()

    if not osname:
        raise SystemError("the operating sytem can not be found.")

    if osname == 'Darwin':
        return "mac"

    else:
        return osname.lower()
