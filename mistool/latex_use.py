#!/usr/bin/env python3

"""
prototype::
    date = 2015-06-04


This script gives a lot of useful functions in relation with the powerful langage
¨latex for typing scientific documents.
"""

from subprocess import CalledProcessError

from mistool.config import latex
from mistool.os_use import (
# Classes and functions
    cd,
    pathenv, PPath,
    runthis,
    system,
# Safe constants
    OS_MAC, OS_LINUX, OS_WIN
)


# -------------------- #
# -- SAFE CONSTANTS -- #
# -------------------- #

ACCCESS_ERROR, EXIST_ERROR, NOT_TEX_ERROR, SUPERUSER_ERROR = range(4)

TEXLIVE = "texlive"
MIKTEX  = "miktex"


# ------------------------- #
# -- FOR ERRORS TO RAISE -- #
# ------------------------- #

class LatexError(ValueError):
    """
prototype::
    type = cls ;
           base class for errors specific to ¨latex.
    """
    pass


def _raise_io_error(
    kind   = None,
    ppath  = None,
    action = None
):
    """
prototype::
    arg = str: kind
    arg = PPath: ppath
    arg = str: action in [ACCCESS_ERROR , EXIST_ERROR ,
                          NOT_TEX_ERROR, SUPERUSER_ERROR]

    return = str ;
             this function simply eases the raising of some specific IO errors.
    """
    if action == SUPERUSER_ERROR:
        raise PermissionError("you must be a super user")

    if action == ACCCESS_ERROR:
        ErrorToRaise = PermissionError
        action       = 'needs the "Super User\'s rights"'

    elif action == EXIST_ERROR:
        ErrorToRaise = FileNotFoundError
        action       = "doesn't exist"

    elif action == NOT_TEX_ERROR:
        ErrorToRaise = OSError
        action       = "is not a TeX one"

    raise ErrorToRaise(
        "the following {0} {1}.\n\t    + {2}".format(kind, action, ppath)
    )


# ---------------- #
# -- FORMATTING -- #
# ---------------- #

CHARS_TO_ESCAPE   = latex.CHARS_TO_ESCAPE
CHARS_TO_LATEXIFY = latex.CHARS_TO_LATEXIFY

def escape(
    text,
    mode = "text"
):
    """
prototype::
    arg = str: text ;
          the text to be escaped
    arg = str: mode = "text" in ["text" , "math"] ;
          the ¨latex mode where the text will be used

    return = str ;
             the text with all specific ¨latex characters escaped so as to be
             used verbatim in either a math formula or a text regarding ot the
             value of ``mode``


Here is an example of use.

pyterm::
    >>> from mistool.latex_use import escape
    >>> onetext = "\OH/ & ..."
    >>> print(escape(onetext))
    \textbackslash{}OH/ \& ...
    >>> print(escape(text = onetext, mode = "math"))
    \backslash{}OH/ \& ...


info::
    Two global dictionaries are used.

        1) ``CHARS_TO_ESCAPE`` indicates only characters that must be escaped
        with one backslash ``\``.

        2) ``CHARS_TO_LATEXIFY`` is for expressions that needs one ¨latex
        command.
    """
    if mode not in CHARS_TO_ESCAPE:
        raise ValueError("unknown mode.")

    tolatexify = CHARS_TO_LATEXIFY[mode].items()
    toescape   = CHARS_TO_ESCAPE[mode]

    answer = ''

    imax = len(text)
    i = 0

    while(i < imax):
        nothingfound = True

        for onechar in toescape:
            if text[i] == onechar:
                answer += '\\' + onechar
                i += 1
                nothingfound = False
                break

        if nothingfound:
            for onechar, latexcode in tolatexify:
                if text[i:].startswith(onechar):
                    answer += latexcode
                    i += len(onechar)
                    nothingfound = False
                    break

        if nothingfound:
            answer += text[i]
            i += 1

    return answer


# --------------- #
# -- COMPILING -- #
# --------------- #

class Build:
    """
prototype::
    arg-attr = PPath: ppath ;
               the path of the ¨latex file to compile.
    arg-attr = int: repeat = 1 ;
               the number of compilations to be done (for example, if the
               ¨latex document has one table of content, several compilations
               are needed).
    arg-attr = bool: showoutput = False ;
               by default, ``showoutput = False`` asks to not show the
               informations sent by ¨latex when it is compiling


This class gives methods for compilate a ¨latex document. Let's consider the
following ¨latex file with the path path::``/Users/projetmbc/latex/file.tex``.

latex::
    \documentclass[11pt, oneside]{article}

    \begin{document}

    \section{Un petit test}

    Une formule toute simple : $E = mc^2$.

    \end{document}


In the lines above, we have added call to the class ``term_use.DirView``
so as to show the new files made by ¨latex (the ellipsis terminal::``[...]``
indicates some lines not reproduced here).

pyterm::
    >>> from mistool.latex_use import Build, PPath
    >>> from mistool.term_use import DirView
    >>> latexdir = PPath("/Users/projetmbc/latex/file.tex")
    >>> print(DirView(latexdir.parent).ascii)
    + latex
        * file.tex
    >>> builder   = Build(latexdir)
    >>> builder.pdf()
    # -- Start of compilation Nb.1 -- #

    This is pdfTeX, Version 3.14159265-2.6-1.40.15 (TeX Live 2014) (preloaded
    format=pdflatex)
     restricted \write18 enabled.
    entering extended mode

    [...]

    Output written on file.pdf (1 page, 36666 bytes).
    Transcript written on file.log.

    # -- End of compilation Nb.1 -- #
    >>> print(DirView(latexdir.parent).ascii)
    + latex
        * file.aux
        * file.log
        * file.pdf
        * file.tex


info::
    Take a look at the function ``clean`` of this module which can automatically
    remove the extra files path::``file.aux`` et path::``file.log`` that ¨latex
    makes.
    """

    def __init__(
        self,
        ppath,
        repeat    = 1,
        showoutput = True
    ):
# Does the file to compile exist ?
        if not ppath.is_file():
            _raise_io_error(
                kind   = "file",
                path   = ppath,
                action = EXIST_ERROR
            )

# Do we have TEX file ?
        if ppath.ext != "tex":
            _raise_io_error(
                kind   = "file",
                path   = path,
                action = NOT_TEX_ERROR
            )

# Infos given by the user.
        self.ppath      = ppath
        self.repeat     = repeat
        self.showoutput = showoutput

        self.cmd = None


    def compile(self):
        """
prototype::
    action = this method launches the compilation defined via ``self.cmd``
             in verbose mode or not the number of times that is indicated
             in ``self.repeat``.
        """
        imax = self.repeat + 1

        if imax == 1:
            start_compile = '# -- Start of the compilation -- #\n'
            end_compile   = '\n# -- End of the compilation -- #'

        else:
            start_compile = '# -- Start of compilation Nb.{0} -- #\n'
            end_compile   = '\n# -- End of compilation Nb.{0} -- #'

        for i in range(1, imax):
            if self.showoutput:
                if i != 1:
                    print("")

                print(start_compile.format(i))

            with cd(self.ppath.parent):
                runthis(
                    cmd        = '{0} "{1}"'.format(self.cmd, self.ppath),
                    showoutput = self.showoutput
                )

            if self.showoutput:
                print(end_compile.format(i))

        self.cmd = None


    def pdf(self):
        """
prototype::
    action = this method calls ¨latex so as to build the ¨pdf output.
        """
# The option "-interaction=nonstopmode" don't stop the terminal even if there is
# an error found by ¨latex.
        self.cmd = 'pdflatex -interaction=nonstopmode'
        self.compile()


# -------------- #
# -- CLEANING -- #
# -------------- #

TEMP_EXTS     = latex.TEMP_EXTS
EXTS_TO_CLEAN = latex.EXTS_TO_CLEAN

def clean(
    ppath,
    exts       = EXTS_TO_CLEAN,
    showoutput = False
):
    """
prototype::
    arg = PPath: ppath ;
          the path of either one ¨latex file or a directory
    arg = list(str): exts = EXTS_TO_CLEAN ;
          the list of extensions of the special files made by ¨latex that
          have to be removed
    arg = bool: showoutput = False ;
          by default, ``showoutput = False`` asks to not show the informations
          about the cleaning

    action = this function removes extra files build during a ¨latex compilation
             that are associated to a file, or the ones corresponding to all the
             ¨latex files in a directory.


In the following example, we use the class ``term_use.DirView`` so as to show
the changes in the folder path::``/Users/projetmbc/latex`` of the ¨latex file
path::``file.tex`` for which we want to do some cleanings.

pyterm::
    >>> from mistool.latex_use import clean, PPath
    >>> from mistool.term_use import DirView
    >>> latexdir = PPath("/Users/projetmbc/latex")
    >>> print(DirView(latexdir.parent).ascii)
    + latex
        * file.aux
        * file.log
        * file.pdf
        * file.synctex.gz
        * file.tex
    >>> clean(ppath = latexdir, showoutput = True)
    * Cleaning for "/Users/projetmbc/latex/file.tex"
    >>> print(DirView(latexdir.parent).ascii)
    + latex
        * file.pdf
        * file.tex


info::
    If you want to build your own list of extensions you can take a look both at
    the list ``EXTS_TO_CLEAN`` and the dictionary ``TEMP_EXTS``.
    """
# One file
    if ppath.is_file():
        if ppath.ext != "tex":
            _raise_io_error(
                kind   = "file",
                path   = main,
                action = NOT_TEX_ERROR
            )

        texpaths = [ppath]

# One directory : we use an iterator so as to see changes in live.
    elif ppath.is_dir():
        texpaths = ppath.walk("file::**.tex")

# Nothing existing
    else:
        raise FileNotFoundError("path points to nowhere.")

# Clean now !
    for p in texpaths:
        if showoutput:
            print('* Cleaning for "{0}"'.format(p))

        for ext in exts:
            tempfile = p.with_ext(ext)

            if tempfile.is_file():
                tempfile.remove()


# ---------------------------------- #
# -- ABOUT THE LATEX DISTRIBUTION -- #
# ---------------------------------- #

# Sources :
#    * http://tex.stackexchange.com/a/68820/6880
#    * http://tex.stackexchange.com/a/69484/6880
#    * https://groups.google.com/forum/?hl=fr&fromgroups=#!topic/fr.comp.text.tex/ivuCnUlW7i8

# << Warning ! >> The following path is the recommended one for the folder to
# use for homemade packages.

MIKETEX_LOCALDIR = PPath('C:/texmf-local')

def _localdir_texlive(osname = ""):
    """
prototype::
    arg = str: osname = "" in [OS_WIN , OS_LINUX , OS_MAC];
          the name of the ¨os (logical, isn't it ?), that can be found
          automatically if you use the default value ``osname = ""``

    return = PPath ;
             the path of the ¨texlive directory where we have to put special
             ¨latex packages.
    """
    if osname == "":
        osname = system()

    if osname == OS_WIN:
        localdir = runthis("kpsexpand '$TEXMFLOCAL'")
        localdir = PPath(localdir.strip()).normpath

    elif osname in [OS_LINUX, OS_MAC]:
        localdir = runthis('kpsewhich --var-value=TEXMFLOCAL')
        localdir = PPath(localdir.strip()).normpath

    else:
        raise OSError("unsupported OS << {0} >>.".format(osname))

    return localdir


def about():
    """
prototype::
    return = dict ;
             this function gives informations needed by the function ``install`.


The dictionary returned looks like the following one. In this example, we are on
a ¨mac computer where ¨texlive has been installed by ¨mactex.

python::
    {
        'osname'    : 'mac',
        'latexname' : 'texlive',
        'latexfound': True,
        'localdir'  : PPath('/usr/local/texlive/texmf-local')
    }

The key ``'localdir'`` contains the path to use to install special packages.
    """
    osname = system()

    latexfound = False
    latexname  = ''
    localdir   = None

# Windows
    if osname == OS_WIN:
        winpath = pathenv()

# Is MiKTeX installed ?
        if '\\miktex\\' in winpath:
            latexfound = True
            latexname  = MIKTEX

            if MIKETEX_LOCALDIR.is_dir():
                localdir = MIKETEX_LOCALDIR

# Is TeX Live installed ?
        elif '\\texlive\\' in winpath:
            latexfound = True
            latexname  = TEXLIVE
            localdir   = _localdir_texlive(osname)

# Linux and Mac
    elif osname in [OS_LINUX, OS_MAC]:
# Is LaTeX installed ?
        try:
            if runthis('which pdftex'):
                latexfound = True
                latexname  = TEXLIVE
                localdir   = _localdir_texlive(osname)

        except CalledProcessError:
            ...

# Unknown method...
    else:
        raise OSError("unsupported OS << {0} >>.".format(osname))

# The job has been done...
    return {
        'osname'    : osname,
        'latexname' : latexname,
        'latexfound': latexfound,
        'localdir'  : localdir
    }


# ---------------- #
# -- INSTALLING -- #
# ---------------- #

# For the infos shown.
_TAB      = ' '*4
_DECO_1 = '{0}* '.format(_TAB)
_DECO_2 = '{0}+ '.format(_TAB*2)


def _must_be_su(aboutlatex):
    """
prototype::
    see = about

    arg = dict: aboutlatex = {} ;
          one dictionary similar to the one sent by the function ``about``

    action = this function tests if we have "Super User" permissions
    """
    if aboutlatex['localdir'].is_protected():
        _raise_io_error(action = SUPERUSER_ERROR)


def _can_install(aboutlatex):
    """
prototype::
    see = about

    arg = dict: aboutlatex = {} ;
          one dictionary similar to the one sent by the function ``about``

    action = this function tests if we have ¨latex local directory that we can
             act on it
    """
# We must have a local directory
    if aboutlatex['localdir'] == None:
        message = "no local directory for special packages has been found."

        if aboutlatex['latexname'] == MIKTEX:
            message += "You can use the function << make_miktex_localdir >>."

        raise LatexError(message)

# Installation suported only on Mac O$, Linux and Windows
    if aboutlatex['osname'] not in [OS_MAC, OS_LINUX, OS_WIN]:
        raise LatexError(
            'the installation of local packages is not yet supported '
            'with the OS << {0} >>.'.format(aboutlatex['osname'])
        )

# We must be a super user !
    _must_be_su(aboutlatex)


def refresh(aboutlatex = {}):
    """
prototype::
    see = about

    arg = dict: aboutlatex = {} ;
          one dictionary similar to the one sent by the function ``about``

    action = the list of packages directly known by the ¨latex distribution is
             refreshed


warning::
    You have to be in super user mode if you want this function to work.
    """
# We have to build infos about the ¨latex distribution.
    if aboutlatex == {}:
        aboutlatex = about()

# We must be a super user !
    _must_be_su(aboutlatex)

# TeX Live
    if aboutlatex['latexname'] == TEXLIVE:
        runthis('mktexlsr')

# MiKTex
    elif aboutlatex['latexname'] == MIKTEX:
        runthis('initexmf --update-fndb --verbose')

# Unkonwn !!!
    else:
        raise LatexError(
            'refreshing the list of LaTeX packages is not '
            'supported with your LaTeX distribution.'
        )


def make_miktex_localdir(aboutlatex):
    """
prototype::
    see = about

    arg = dict: aboutlatex ;
          one dictionary similar to the one sent by the function ``about``

    action = this function creates one local directory and add it to the list
             of directories automatically analysed by MiKTeX when it looks for
             packages.


info::
    Even it is a really bad idea, you can change the path ``MIKETEX_LOCALDIR``
    to put your homemade packages where you want.
    """
    if aboutlatex['osname'] != OS_WIN \
    or aboutlatex['latexname'] != MIKTEX:
        raise OSError(
            'this function can only be used with the OS "window" '
            'and the LaTeX distribution "miktex".'
        )

# Creation of the directory
    MIKETEX_LOCALDIR.create("dir")

# Adding the directory to the ones analysed by MiKTex.
    runthis(
        cmd = 'initexmf --admin --user-roots={0} --verbose'.format(
            MIKETEX_LOCALDIR
        )
    )

    runthis(cmd = 'initexmf --update-fndb --verbose')

    print(
        '',
        'The following local directory for MiKTeX has been created.',
        '\t<< {0} >>'.format(MIKETEX_LOCALDIR),
        sep = "\n"
    )


def install(
    ppath,
    regpath = "file::**",
    name    = "",
    clean   = True
):
    """
prototype::
    see = os_use._ppath_regpath2meta , about

    arg = PPath: ppath;
          the path of folder containg the package
    arg = str: name = "" ;
          you can use this variable so as to give explicitly the name of the
          package, otherwise that will be the name of the folder that will
          choosen
    arg = str: regpath = "file::**" ;
          this is a string that follows some rules named regpath rules (see
          the documentation of the function ``os_use._ppath_regpath2meta``)
    arg = bool: clean = True ;
          by default, ``clean = True`` asks to remove first an old version of
          the package

    action = this function install an homemade package in a dedicated folder
             known by your ¨latex distribution.


warning::
    This function can only be used with the "Super User" mode.


Let's suppose that we have package named latex::``lyxam`` stored in a folder
having the path path::``/Users/projetmbc/latex/lyxam`` and whose structure is
the following one.

dir::
    + lyxam
        + change_log
            + 2012
                * 02.txt
                * 03.txt
                * 04.txt
                * 10.txt
            * todo.txt
        * lyxam.sty
        + config
            * settings.tex
            + lang
                * en.tex
                * fr.tex
                + special
                    * fr.config
                + standard
                    * en.config
                    * fr.config
            + style
                * apmep.tex
                * default.tex


You can easily install this package locally in your ¨latex distribution like it
is done in the lines of code above.

pyterm::
    >>> from mistool.latex_use import install, PPath
    >>> package = PPath("/Users/projetmbc/latex/lyxam")
    >>> install(package)
    Starting installation of the package locally.
        * Deletion of the old << lyxam >> package in the local LaTeX directory.
        * Creation of a new << lyxam >> package in the local LaTeX directory.
            + Adding the new file << lyxam.sty >>
            + Adding the new file << change_log/todo.txt >>
            + Adding the new file << change_log/2012/02.txt >>
            + Adding the new file << change_log/2012/03.txt >>
            + Adding the new file << change_log/2012/04.txt >>
            + Adding the new file << change_log/2012/10.txt >>
            + Adding the new file << config/settings.tex >>
            + Adding the new file << config/lang/en.tex >>
            + Adding the new file << config/lang/fr.tex >>
            + Adding the new file << config/lang/special/fr.config >>
            + Adding the new file << config/lang/standard/en.config >>
            + Adding the new file << config/lang/standard/fr.config >>
            + Adding the new file << config/style/apmep.tex >>
            + Adding the new file << config/style/default.tex >>
        * Refreshing the list of LaTeX packages.


In this example we have used some default settings.

    1) ``regpath = "file::**"`` asks to copy all the files.

    2) ``name = ""`` tell to use the same name for the ¨latex package and the folder.

    3) ``clean = True`` is for removing first an old version if there is one
    (that is the case in our example).


Let's suppose now that we do not want to install all the path::``TXT`` files.
It is easy with "regpaths" as you can see in the following example (see the
documentation of the special function ``os_use._ppath_regpath2meta``).

pyterm::
    >>> from mistool.latex_use import install, PPath
    >>> package = PPath("/Users/projetmbc/latex/lyxam")
    >>> install(ppath = package, regpath = "file not::**.txt")
    Starting installation of the package locally.
        * Deletion of the old << lyxam >> package in the local LaTeX directory.
        * Creation of a new << lyxam >> package in the local LaTeX directory.
            + Adding the new file << lyxam.sty >>
            + Adding the new file << config/settings.tex >>
            + Adding the new file << config/lang/en.tex >>
            + Adding the new file << config/lang/fr.tex >>
            + Adding the new file << config/lang/special/fr.config >>
            + Adding the new file << config/lang/standard/en.config >>
            + Adding the new file << config/lang/standard/fr.config >>
            + Adding the new file << config/style/apmep.tex >>
            + Adding the new file << config/style/default.tex >>
        * Refreshing the list of LaTeX packages.
    """
# Sources :
#    * http://www.commentcamarche.net/forum/affich-7670740-linux-supprimer-le-contenu-d-un-repertoire
#    * http://stackoverflow.com/questions/185936/delete-folder-contents-in-python

# Let's talk about...
    print("Starting installation of the package locally.")

# About the package
    if not ppath.is_dir():
        raise NotADirectoryError("``ppath`` doesn't point to a directory.")

    if name == "":
        name = ppath.stem

# Can we do the job ?
    aboutlatex = about()
    _can_install(aboutlatex)

# The local directory of the package
    localdir = aboutlatex['localdir'] / 'tex' / 'latex'
    print(
        '{0}Local installation made in << {1} >>.'.format(_DECO_1, localdir)
    )

    packagedir = localdir / name

# We have to clean an old version.
    if clean and packagedir.is_dir():
        print(
            '{0}Deletion of the old "{1}" '.format(_DECO_1, name) \
            + 'package in the local LaTeX directory.'
        )

        packagedir.remove()

# Creation of the new local package.
    print(
        '{0}Creation of a new "{1}" '.format(_DECO_1, name) \
        + 'package in the local LaTeX directory.'
    )

    fileadded = False

    for pathfrom in ppath.walk(regpath):
        fileadded = True
        pathto = pathfrom.relative_to(ppath)

        print('{0}Adding the new file << {1} >>.'.format(_DECO_2, pathto))

        pathto = packagedir / pathto

        pathfrom.copy_to(pathto)

# We must refresh of the list of LaTeX packages.
    if fileadded:
        print('{0}Refreshing the list of LaTeX packages.'.format(_DECO_1))

        refresh(aboutlatex)

    else:
        print('{0}<< Warning ! >> The package is empty !'.format(_DECO_1))


def remove(name):
    """
prototype::
    arg = str: name ;
          the name of a local ¨latex package

    action = the package is removed from the local ¨latex distribution


warning::
    This function can only be used with the "Super User" mode.
    """
    print("Deletion of the package locally.")

# Can we do the job ?
    aboutlatex = about()
    _can_install(aboutlatex)

# The local directory of the package
    localdir = aboutlatex['localdir'] / 'tex' / 'latex'
    print(
        '{0}Local installation made in << {1} >>.'.format(_DECO_1, localdir)
    )

    packagedir = localdir / name

# We remive the old version.
    if packagedir.is_dir():
        packagedir.remove()

        print('{0}Refreshing the list of LaTeX packages.'.format(_DECO_1))

        refresh(aboutlatex)

    else:
        print(
            '{0}<< Warning ! >> No local package "{1}" !'.format(
                _DECO_1,
                name
            )
        )
