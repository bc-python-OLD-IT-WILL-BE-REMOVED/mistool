#!/usr/bin/env python3

"""
Directory : mistool
Name      : os_use
Version   : 2014.08
Author    : Christophe BAL
Mail      : projetmbc@gmail.com

This module contains functions to manipulate easily files, directories and also
to have informations about the system.
"""

import os
import shutil
import platform
from subprocess import check_call


# ------------------------- #
# -- FOR ERRORS TO RAISE -- #
# ------------------------- #

class OsUseError(ValueError):
    """
Base class for errors in the ``os_use`` module of the package ``mistool``.
    """
    pass


# ----------- #
# -- TESTS -- #
# ----------- #

def isfile(path):
    """
This function simply tests if the path ``path`` points to an existing file.
    """
    return os.path.isfile(path)

def isdir(path):
    """
This function simply tests if the path ``path`` points to an existing directory.
    """
    return os.path.isdir(path)

def hasextin(
    path,
    exts
):
    """
This function tests if the path ``path`` finishes by one of the extensions given
in the list of extensions ``exts``.
    """
    if '.' in path:
        for ext in exts:
            if path.endswith('.' + ext):
                return True

    return False


# ----------------------- #
# -- INFOS ABOUT PATHS -- #
# ----------------------- #

SEP = os.sep

def realpath(path):
    """
This function interprets the shortcut path::``~`` for the default user's
directory and the relative path using path::``/../`` to go higher in the tree
structure of a directory. For example, on a Mac the following code will give
the path path::``/Users/login/dir_1/file.txt`` where ``login`` is the os login
of the user.

python::
    from mistool import os_use

    print(
        os_use.realpath("~/dir_1/dir_2/dir_3/../../file.txt")
    )
    """
    return os.path.normpath(
        os.path.expanduser(path)
    )

def name(path):
    """
This function extracts from the path ``path`` the name of the file with its
extension or simply the name of one directory.
    """
    i = path.rfind(SEP)

    return path[i+1:]

def filename(path):
    """
This function extracts from the path ``path`` the name of the file without its
extension.
    """
    return os.path.splitext(name(path))[0]

def ext(path):
    """
This function extracts from the path ``path`` the extension of the file.
    """
    return os.path.splitext(path)[1][1:]

def noext(path):
    """
This function removes from the path ``path`` the extension of the file.
    """
    i = len(ext(path))

    if i != 0:
        i += 1

        return path[:-i]

    return path

def parentdir(path):
    """
This function returns the path of the directory that contains the file or the
directory corresponding to the path ``path``.
    """
    return os.path.dirname(path)

def relativepath(
    main,
    sub,
):
    """
Suppose that we have the following paths where ``main`` is the path of the main
directory and ``sub`` the one of a sub directory or a file contained in the main
directory.

python::
    main = "/Users/projects/source_dev"
    sub  = "/Users/projects/source_dev/misTool/os_use.py"

The function will return in that case the following string which always begin
with one slash ``/``.

python::
    "/misTool/os_use.py"
    """
# Special case of the same path !
    if main == sub:
        raise OsUseError("The main path and the sub-path are equal.")

# We clean the path in case of they contain things like ``../``.
    main = realpath(main)
    sub  = realpath(sub)

# The main path must finish by one backslash because
#     "python/misTool/source_dev/misTool/os_use.py"
# is not one sub path of
#     "python/misTool/source".

    if main[-1] != SEP:
        main += SEP

# Is the sub path contained in the main one ?
    if not sub.startswith(main):
        raise OsUseError(
            "The sub-path\n\t+ {0}\nis not contained in the main path\n\t+ {1}\n" \
                .format(sub, main) \
            + "so it is not possible to have one relative path."
        )

# Everything seems ok...
    i = len(main) - 1

    return sub[i:]

def relativedepth(
    main,
    sub
):
    """
Suppose that we have the following paths where ``main`` is the path of the main
directory and ``sub`` the one of a sub directory or a file contained in the main
directory. Here are some examples.

    1) The function will return ``1`` in the following case.

    python::
        main = "/Users/projects/source_dev"
        sub  = "/Users/projects/source_dev/misTool/os_use.py"

    This means that the file path::``os_use.py`` is contained in one simple sub
    directory of the main directory.

    2) In the following case, the function will return ``2``.

    python::
        main = "/Users/projects/source_dev"
        sub  = "/Users/projects/source_dev/misTool/os/os_use.py"

    3) For the last example just after, the value returned will be ``0``.

    python::
        main = "/Users/projects/source_dev"
        sub  = "/Users/projects/source_dev/os_use.py"
    """
    return relativepath(
        main        = main,
        sub         = sub
    ).count(SEP) - 1

def commonpath(paths):
    """
This function returns the smaller directory that contains the objects having the
paths given in the list ``paths``.
    """
    if len(paths) < 2:
        raise OsUseError(
            "You must give at least two paths."
        )

    if len(paths) == 2:
        answer = []

        pieces_1 = paths[0].split(SEP)
        pieces_2 = paths[1].split(SEP)

        for i in range(min(len(pieces_1), len(pieces_2))):
            if pieces_1[i] == pieces_2[i]:
                answer.append(pieces_1[i])
            else:
                break

        return SEP.join(answer)

    else:
        return commonpath([
            commonpath(paths[:-1]), paths[-1]
        ])


# ------------------------------------- #
# -- OPENING WITH ASSOCIATED PROGRAM -- #
# ------------------------------------- #

def watch(path):
    """
This function tries to open one directory, or one file. Indeed, files are opened
within their associated applications, if this last ones exist.
    """
# Nothing to open...
    isonefile = isfile(path)

    if not isonefile and not isdir(path):
        raise OsUseError(
            "The following path does not point to one existing file " \
            "or directory.\n\t<< {0} >>".format(path)
        )

# Each OS has its own method.
    osname = system()

# Windows
    if osname == "windows":
        if isonefile:
            os.startfile(path)
        else:
            check_call(args = ['explorer', path])

# Mac
    elif osname == "mac":
        check_call(args = ['open', path])

# Linux
#
# Source :
#     * http://forum.ubuntu-fr.org/viewtopic.php?pid=3952590#p3952590
    elif osname == "linux":
        check_call(args = ['xdg-open', path])

# Unknown method...
    else:
        raise OsUseError(
            "The opening of file on << {0} >> OS is not "
            "supported.".format(osname)
        )


# ------------- #
# -- READING -- #
# ------------- #

def readtxtfile(
    path,
    encoding = "utf-8"
):
    """
This function returns the text like content of one file given by its path.

You can indicate the encoding of the file with the optional argument
``encoding`` whose dfault value is ``"utf-8"``. The available encodings are the
same as the ones for the standard ¨python function ``open``.
    """
    with open(
        file     = path,
        mode     = "r",
        encoding = encoding
    ) as f:
        return f.read()


# ----------------------------------- #
# -- CREATION, DELETION AND MOVING -- #
# ----------------------------------- #

def makedir(path):
    """
This function build the directory with the given path ``path``. If one parent
directory must be build, the function will do the job.
    """
    if not isdir(path):
        os.makedirs(path)

def maketxtfile(
    path,
    text     = '',
    encoding = 'utf-8'
):
    """
This function build the file with the given path ``path`` and the text like
content ``text``.

You can indicate the encoding of the file with the optional argument ``encoding``
whose dfault value is ``"utf-8"``. The available encodings are the same as the
ones for the standard ¨python function ``open``.
    """
    makedir(parentdir(path))

    with open(
        file     = path,
        mode     = "w",
        encoding = encoding
    ) as f:
        f.write(text)

def move(
    source,
    destination
):
    """
This function moves the file or the directory from the path ``source`` to the
path ``destination``. If the source and the destination have the same parent
directory, then the final result is just a renaming of the file or directory.
    """
    if isdir(path):
        os.renames(source, destination)

    elif isfile(source):
        copy(source, destination)

        if isfile(destination):
            destroy(source)

def copy(
    source,
    destination
):
    """
This function copy the file having the path ``source`` to the destination path
``destination``.
    """
    if isfile(source):
        dir = parentdir(destination)

        if not isdir(dir):
            makedir(dir)

        shutil.copy(source, destination)

    elif isdir(source):
        raise OsUseError(
            "The copy of one directory is not yet supported."
        )

    else:
        raise OsUseError(
            "The following path points nowhere.\n\t<< {0} >>".format(source)
        )

def destroy(path):
    """
This function removes the directory or the file given by its path ``path``.
    """
    if isdir(path):
        shutil.rmtree(path)

    elif isfile(path):
        os.remove(path)

def clean(
    path,
    cleanall = False,
    exts      = [],
    depth     = 0
):
    """
-----------------
Small description
-----------------

This function removes things in a directory. There is two ways of use.

    1) Using something like ``clean(path = mydirpath, cleanall = True)``, you
    will remove anything that is in the directory having the path ``mydirpath``.

    2) If you don't use ``cleanall``, which default value is ``False``, then the
    function will only remove files regarding to the values of the arguments
    ``exts`` and ``depth`` which have the same meaning that for the function
    ``nextfile``.


-------------
The arguments
-------------

This functions uses the following variables.

    1) ``path`` is simply the path of the directory to clean.

    2) ``cleanall`` is a boolean variable to clean all sub files and sub
    directories. By default, ``cleanall = False`` which asks do not clean all.
    In that case, the function uses the variables ``exts`` and ``depth``.

    3) ``exts`` is the list of the extensions of the files to remove. By default,
    ``ext = []`` which asks to remove every kind of files.

    4) ``depth`` is the maximal depth for the research of the files to remove.
    The very special value ``(-1)`` indicates that there is no maximum. The
    default value is ``0`` which asks to only look for in the direct content of
    the main directory to analyse.
    """
    if cleanall:
# We remove the files directly in the directory.
        for onefile in nextfile(main = path):
            destroy(onefile)

# << Warning ! >> We can't use the iterator.
        for onedir in listdir(main = path):
            destroy(onedir)

    else:
        for onefile in nextfile(
            main  = path,
            exts  = {'keep': exts},
            depth = depth
        ):
            destroy(onefile)


# ------------------- #
# -- LIST OF FILES -- #
# ------------------- #

def _issubdepthgood(
    main,
    sub,
    depth
):
    """
This small function is used by ``nextfile`` so as to know if one directory must
be inspected or not.
    """
    if depth == -1:
        return True

    elif depth == 0:
        return bool(main == sub)

# ``relativedepth`` sends logically one error if the two directories are equal,
# so we have to take care of this very special case.
    elif main == sub:
        return True

    else:
# The use of ``... + 1`` in the test comes from the fact we work with files
# contained in the sub directory, and the depth of this file is equal to the
# one of the sub directory plus one.
        return bool(
            relativedepth(main = main, sub = sub) + 1 <= depth
        )

def _isfilegood(
    path,
    exts,
    prefixes
):
    """
This small function is used by ``nextfile`` so as to know if the file found
matches the search criteria about extensions, prefixes and hiddeness.
    """
    path = name(path)

    tokeep = True

    if exts['discard'] and hasextin(path, exts['discard']):
        tokeep = False

    if tokeep:
        if exts['keep'] and not hasextin(path, exts['keep']):
            tokeep = False

    if tokeep:
        for prefix in prefixes['discard']:
            if path.startswith(prefix):
                tokeep = False
                break

    if tokeep and prefixes['keep']:
        tokeep = False

        for prefix in prefixes['keep']:
            if path.startswith(prefix):
                tokeep = True
                break

    return tokeep

def _tokeepdiscard(extorprefixs):
    """
This small function is used by ``nextfile`` so as to produce one normalized
dictionary of the variables ``exts`` and ``prefix``.
    """
#    if extorprefixs == None:
#        extorprefixs = {'keep': "..."}

    if isinstance(extorprefixs, str) \
    or isinstance(extorprefixs, list):
        extorprefixs = {'keep': extorprefixs}

    tokeep = extorprefixs.get('keep', [])

    if isinstance(tokeep, str):
        tokeep = [tokeep]

    todiscard = extorprefixs.get('discard', [])

    if isinstance(todiscard, str):
        todiscard = [todiscard]

    return {
        'keep'   : tokeep,
        'discard': todiscard
    }

def nextfile(
    main,
    exts         = {},
    prefixes     = {},
    depth        = 0,
    unkeephidden = True,
    keepdir      = None
):
    """
-----------------
Small description
-----------------

This function is an iterator that sends path of files in a directory with the
possibility to use some criteria of research.


Suppose for example that we have the following directory structure.

directory::
    + mistool
        * __init__.py
        * description.rst
        * latex_use.py
        * os_use.py
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
                * latexTest.pdf
                * latexTest.tex
                * latexTestBuilder.py
                * ...
        + toUse
            + latex
                * ...


Let's consider the following code.

python::
    from mistool import os_use

    for path in os_use.nextfile(
        main  = "/Users/mistool",
        exts  = "py",
        depth = -1
    ):
        print(path)


If we launch the preceding code in a terminal, then we obtain the following
outputs.

terminal::
    /Users/mistool/__init__.py
    /Users/mistool/latex_use.py
    /Users/mistool/os_use.py
    /Users/mistool/debug/debug_latex_use.py
    /Users/mistool/debug/debug_os_use.py
    /Users/mistool/debug/debug_latex_use/latexTestBuilder.py


You can also have files with different extensions like in the following code.

python::
    from mistool import os_use

    for path in os_use.nextfile(
        main  = "/Users/mistool",
        exts  = ["tex", "pdf"]
        depth = -1
    ):
        print(path)


If we launch the preceding code in a terminal, then we obtain the following
outputs.

terminal::
    /Users/mistool/change_log/2012/07.pdf
    /Users/mistool/change_log/2012/08.pdf
    /Users/mistool/change_log/2012/09.pdf
    /Users/mistool/debug/debug_latex_use/latexTest.pdf
    /Users/mistool/debug/debug_latex_use/latexTest.tex


info::
    You can also exclude extensions and use some other tuning. See the
    presentation of the arguments.


It is also possible to use criteria of search regarding to the prefixes of the
names of the files. For example, the following code will only return the path of
the file which name starts with "latexTest".

python::
    from mistool import os_use

    for path in os_use.nextfile(
        main     = "/Users/mistool",
        prefixes = "latex",
        depth    = -1
    ):
        print(path)


The preceding code will product the following output in a terminal.

terminal::
    /Users/mistool/debug/debug_latex_use/latexTest.pdf
    /Users/mistool/debug/debug_latex_use/latexTest.tex
    /Users/mistool/debug/debug_latex_use/latexTestBuilder.py


-------------
The arguments
-------------

This function uses the following variables.

    1) ``main`` is simply the path of the main directory to analyse.

    2) ``exts`` gives informations about the extensions of the files wanted. It
    can be one of the following kinds.

        i) ``exts`` can be simply a string giving only one extension to keep.

        ii) ``exts`` can be a list of strings giving the list of extensions to
        keep.

        iii) ``exts`` can be a dictionary of the following kind which is used to
        keep or to discard some kinds of files.

        python::
            {
                'keep'   : the extensions of files to look for,
                'discard': the extensions of files to discard
            }


        The values giving the extensions can be either a single string, or a list
        of strings.

    By default, ``exts = {}`` which asks to send every kind of files.

    3) ``prefixes`` can be used in the same way that ``exts`` must be used. This
    variable indicates files to keep or discard regarding to the prefix of their
    name.

    4) ``depth`` is the maximal depth for the research. The very special value
    ``(-1)`` indicates that there is no maximum.

    The default value is ``0`` which asks to only look for in the direct content
    of the main directory to analyse.

    5) The variable ``unkeephidden`` is a boolean to keep or not hidden files, that is files with a name starting by a point.

    The default value is ``True`` so as to only list visible files.

    6) The variable ``keepdir`` has been added so as to be used by the class
    ``TreeDir``, but you can play with it if you want. The possible values are
    the following ones.

        a) The default value ``None`` indicates to unkeep any directory. This is
        what is expected when you call one function named ``nextfile``.

        b) ``"minimal"`` will make the function returns only the directories
        that contains at least one file from the ones searched.

        c) ``"all"`` will make the function returns any sub directories even if
        it doesn't contained one file from the ones searched.

        d) You can also use ``"Minimal"`` and ``"All"``, be carefull of the
        first uppercase letters, so as to also have idiomatic paths ended by
        path::"..." to indicate other files that the ones searched which also
        mustn't be discarded.
    """
# Directories to keep ?
    if keepdir not in [None, "minimal", "Minimal", "all", "All"]:
        raise OsUseError("Illegal value of the variable << keepdir >>.")

    dirtokeep = bool(keepdir != None)

# Indicate or not the files not matching the search queries ?
    showallfiles = bool(keepdir in ["Minimal", "All"])

# Does the directory exist ?
    if not isdir(main):
        raise OsUseError(
            "The following path does not point to one existing directory." \
            "\n\t+ {0}".format(main)
        )

# Extensions and prefixes
    exts     = _tokeepdiscard(exts)
    prefixes = _tokeepdiscard(prefixes)

# It's time to walk in the directory...
    for root, dirs, files in os.walk(main):
        if _issubdepthgood(
            main  = main,
            sub   = root,
            depth = depth
        ):
# The following boolean are used for the directory views !
            nobadfilefound  = True
            nogoodfilefound = True

            for onefile in files:
                path = root + SEP + onefile

# Hidden file or directory must be ignored.
                if unkeephidden and onefile.startswith('.'):
                    ...

# Looking for good files.
                elif _isfilegood(path, exts, prefixes):
# Directory of the first good file found to display ?
                    if nogoodfilefound and dirtokeep:
                        nogoodfilefound = False
                        yield root

                    yield path

# One bad file found
                elif nobadfilefound:
                    nobadfilefound = False

# Directory without any good file
            if nogoodfilefound and keepdir in ["all", "All"] \
            and (not unkeephidden or not filename(root).startswith('.')):
                yield root

# Directory without some good files
            if showallfiles and not nobadfilefound:
                yield root + SEP + "..."

def listfile(*args, **kwargs):
    """
This function is similar to the function ``nextfile``, and it has the same
variables that the ones of ``nextfile``, but instead of sending infos about the
files found one at a time, this function directly sends the whole list of the
infos found sorted.

See the documentation of the function ``nextfile`` to have precisions about the
available variables and the structure of each single info that will be in the
list returned by ``listfile``.
    """
# The use of ``*args`` and ``**kwargs`` makes it very easy to implement the fact
# that ``listfile`` and ``nextfile`` have the same variables.
    return sorted([p for p in nextfile(*args, **kwargs)])


# ----------------------- #
# -- ABOUT DIRECTORIES -- #
# ----------------------- #

def nextdir(
    main,
    depth = 0
):
    """"
-----------------
Small description
-----------------

This function is an iterator that sends path of directories contained in a
directory.


Suppose for example that we have the following directory structure.

directory::
    + mistool
        * __init__.py
        * description.rst
        * latex_use.py
        * os_use.py
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
                * latexTest.pdf
                * latexTest.tex
                * latexTestBuilder.py
                * ...
        + toUse
            + latex
                * ...


Let's consider the following code.

python::
    from mistool import os_use

    for path in os_use.nextfile(
        main  = "/Users/mistool",
        depth = -1
    ):
        print(path)


If we launch the preceding code in a terminal, then we obtain the following
outputs.

terminal::
    /Users/mistool/change_log
    /Users/mistool/change_log/2012
    /Users/mistool/debug
    /Users/mistool/debug/debug_latex_use
    /Users/mistool/toUse
    /Users/mistool/toUse/latex


-------------
The arguments
-------------

This function uses the following variables.

    1) ``main`` is simply the path of the main directory to analyse.

    2) ``depth`` is the maximal depth for the research. The very special value
    ``(-1)`` indicates that there is no maximum.

    The default value is ``0`` which asks to only look for in the direct content
    of the main directory to analyse. In other word, ``depth = 0`` asks to find
    the directories directly contained in the main directory analysed.
    """
    if depth == -1:
        subdepth = - 1

    else:
        if depth == 0:
            subdepth = None

        else:
            subdepth = depth - 1

        depth += 1

    for pathdir in os.listdir(main):
        pathdir = main + SEP + pathdir

        if isdir(pathdir) \
        and _issubdepthgood(
            main  = main,
            sub   = pathdir,
            depth = depth
        ):
            yield pathdir

            if subdepth != None:
                for subpathdir in nextdir(
                    pathdir,
                    depth = subdepth
                ):
                    if _issubdepthgood(
                        main  = main,
                        sub   = subpathdir,
                        depth = depth
                    ):
                        yield subpathdir

def listdir(*args, **kwargs):
    """
-----------------
Small description
-----------------

This function is similar to the function ``nextdir``, and it has the same
variables that the ones of ``nextdir``, but instead of sending infos about the
directories found one at a time, this function directly sends the whole list of
the infos found sorted.

See the documentation of the function ``nextdir`` to have precisions about the
available variables and the structure of each single info that will be in the
list returned by ``listdir``.
    """
# The use of ``*args`` and ``**kwargs`` makes it very easy to implement the fact
# that ``listfile`` and ``nextfile`` have the same variables.
    return sorted([p for p in nextdir(*args, **kwargs)])

class DirView:
    """
-----------------
Small description
-----------------

This class displays the tree structure of one directory with the possibility to
keep only some relevant informations like in the following example. Note that in
a given directory, the files are displayed before the directories.

code::
    + misTool
        * __init__.py
        * latexUse.py
        * os_use.py
        * ...
        + change_log
            + 2012
                * 07.pdf
                * 08.pdf
                * 09.pdf
        + debug
            * debug_latexUse.py
            * debug_os_use.py
            + debug_latexUse
                * latexTest.pdf
                * latexTest.tex
                * latexTestBuilder.py
                * ...
        + toUse
            + latex
                * ...


This output has been obtained with the following ¨python code.

python::
    from mistool import os_use

    dirView = os_use.dirView(
        main    = "/Users/misTool",
        ext     = {'keep': ["py", "txt", "tex", "pdf"]},
        depth   = -1,
        keepdir = "all",
        output  = "short",
        seemain = True
    )

    print(dirView.ascii)


-------------
The arguments
-------------

This class uses the following variables.

    1) The variables ``main``, ``exts``, ``depth``, ``sub``, ``unkeephidden`` and
    ``keepdir`` have exactly the same meaning and behavior that they have with
    the function ``nextfile``, except that here the default value of ``keepdir``
    is ``"minimal"`` and not ``None``.

    2) ``output`` is for the writings of the paths.

        a) The default value ``"all"`` asks to display the whole paths of the
        files and directories found.

        b) ``"relative"`` asks to display relative paths comparing to the main
        directory analysed.

        c) ``"short"`` asks to only display names of directories found, and
        names, with its extensions, of the files found.

    3) ``seemain`` is one boolean value to display or not the main directory
    which is analyzed. The default value is ``True``.
    """
    ASCII_DECOS = {
        'directory': "+",
        'file'     : "*",
        'tab'      : " "*4
    }

    def __init__(
        self,
        main,
        exts         = {},
        prefixes     = {},
        depth        = 0,
        unkeephidden = True,
        keepdir      = "minimal",
        output       = "All",
        seemain      = True
    ):
# Directories to keep ?
        if keepdir == None:
            raise OsUseError(
                "Illegal value of the variable << keepdir >>."
            )

        self.main          = main
        self.exts          = exts
        self.prefixes      = prefixes
        self.depth         = depth
        self.unkeephidden = unkeephidden
        self.keepdir       = keepdir
        self.output        = output
        self.seemain       = seemain

        self.build()

    def build(self):
        """
This method builds one list of dictionaries of the following kind.

python::
    {
        'kind' : "directory" or "file",
        'depth': the depth level regarding to the main directory,
        'path' : the path of one directory or file found
    }
        """
        self.format = {}
        listview    = []

        for path in nextfile(
            main         = self.main,
            exts         = self.exts,
            prefixes     = self.prefixes,
            depth        = self.depth,
            unkeephidden = self.unkeephidden,
            keepdir      = self.keepdir
        ):
            if path == self.main:
                listview.append({
                    'kind' : "directory",
                    'depth': -1,
                    'path' : path
                })

            else:
# Which kind of object ?
                if self._otherfiles(path) or isfile(path):
                    kind = "file"

                else:
                    kind = "directory"

# The depth
                depth = relativedepth(self.main, path)

# << WARNING ! >> We must take care of directories without any file which
# have the same depth of previous files.
                if kind == "directory" and listview:
                    if depth >= listview[-1]['depth']:
                        lastpardir = commonpath([
                            listview[-1]['path'],
                            path
                        ])

                        i = len(lastpardir) + 1

                        subdirnames = path[i:].split(SEP)
                        lastdepth   = depth - len(subdirnames)

                        for name in subdirnames[:-1]:
                            lastpardir += SEP + name
                            lastdepth     += 1

                            listview.append({
                                'kind' : "directory",
                                'depth': lastdepth,
                                'path' : lastpardir
                            })

# Let's store the infos found.
                listview.append({
                    'kind' : kind,
                    'depth': depth,
                    'path' : path
                })

# We have to sort the list by showing first files an then the directories.
# A recursive method is well adpated here even if it is not the clever way
# to do things !
        self.listview = self._sortlistview(listview)

    def _sortlistview(self, listview):
        """
This method sorts the list view so as to display in a given directory, the files
before the directories.
        """
# << Warning ! >> We know that the list view shows the structure but not in
# alphabetical order !

# fod = file or directory
# lof = list of files
# lod = list or directories
        minidepth = min(fod['depth'] for fod in listview)

        lof = []
        lod = []

        lastdir           = None
        subcontent        = []
        subdirs_listviews = {}

        for fod in listview:
            depth = fod['depth']

            if depth == minidepth:
                if fod['kind'] == "file":
                    lof.append(fod)

                else:
                    if subcontent and lastdir:
                        subdirs_listviews[lastdir] = self._sortlistview(subcontent)

                    lastdir                    = fod['path']
                    subcontent                 = []
                    subdirs_listviews[lastdir] = []

                    lod.append(fod)

            else:
                subcontent.append(fod)

        if subcontent and lastdir:
            subdirs_listviews[lastdir] = self._sortlistview(subcontent)

# We have to take care of "..." for other files.
        lof.sort(key = lambda obj: obj['path'])

        if lof \
        and lof[0]['path'].endswith('...'):
            lof.append(lof[0])
            lof.pop(0)

# We have merly finished...
        lod.sort(key = lambda obj: obj['path'])

        lod_and_content = []

        for directory in lod:
            lod_and_content.append(directory)
            lod_and_content += subdirs_listviews[directory['path']]

        return lof + lod_and_content

    def _otherfiles(self, path):
        """
This method displays text indicated that other files are in the directory.
        """
        return path.endswith("...")

    def pathtodisplay(
        self,
        path,
        kind
    ):
        if self._otherfiles(path):
            return "..."

        elif self.output == "relative":
            if self.main == path:
                return path[len(parentdir(path)) + 1:]
            else:
                return relativepath(self.main, path)

        elif self.output == "short":
            if kind == "file":
                return path[path.rfind(SEP)+1:]

            else:
                return path[len(parentdir(path))+1:]

        return path

    @property
    def ascii(self):
        """
This property like method returns a simple ASCCI tree view of the tree structure.
        """
        if 'ascii' not in self.format:
            text = []

            for info in self.listview:
                depth = info["depth"]

# Does the main directory must be displayed ?
                if self.seemain:
                    depth += 1

                tab = self.ASCII_DECOS['tab']*depth

                decokind = self.ASCII_DECOS[info["kind"]] + " "

                pathtoshow = self.pathtodisplay(
                    info["path"], info["kind"]
                )

                text.append(
                    "{0}{1}{2}".format(tab, decokind, pathtoshow)
                )

            self.format['ascii'] = '\n'.join(text)

        return self.format['ascii']


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
        raise OsUseError(
            "The operating sytem can not be found."
        )

    if osname == 'Darwin':
        return "mac"

    else:
        return osname.lower()
