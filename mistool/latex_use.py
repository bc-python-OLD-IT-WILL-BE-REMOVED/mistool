#!/usr/bin/env python3

"""
Directory : mistool
Name      : latex_use
Version   : 2015.03
Author    : Christophe BAL
Mail      : projetmbc@gmail.com

This script gives some useful functions in relation with the powerful LaTeX
langage for typing scientific documents.
"""

from subprocess import check_call, check_output, CalledProcessError

from mistool import os_use
from mistool.config import latex

normpath = os_use.os.path.normpath
join     = os_use.os.path.join


# ------------------------- #
# -- FOR ERRORS TO RAISE -- #
# ------------------------- #

class LatexError(ValueError):
    """
Base class for errors specific to LaTeX.
    """
    pass

def _raise_ioerror(
    kind,
    path,
    action
):
    """
This function simply eases the raising of some specific errors.
    """
    if action == 'access':
        action = 'needs the "Super User\'s rights"'

    elif action == 'create':
        action = "can't be created"

    elif action == 'exist':
        action = "doesn't exist"

    elif action == 'notTeX':
        action = "is not a TeX one"

    raise IOError(
        "the following {0} {1}.\n\t<< {2} >>".format(kind, action, path)
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
-----------------
Small description
-----------------

In LaTeX language, somme character has one meaning. The purpose of this function
is to escape all this special charcaters so as to see them in the output
produced by LaTeX.

For example, ``escape("\OH/ & ...")`` is equal to ``"\textbackslash{}OH/ \&
..."``, whereas ``escape(text = "\OH/ & ...", mode = "math")`` is equal to
``"\backslash{}OH/ \& ..."``. Just notice the difference coming from the use of
``mode = "math"``. In math formulas and in simple text, the backslash is
indicated by using two different LaTeX commands.


-------------
The arguments
-------------

This function uses the following variables.

    1) ``text`` is simply the text to change.

    2) ``mode`` indicate which kind of text is analysed. By default, ``mode =
    "text"`` is for one content that will be simply text in the document
    produced by LaTeX. You can also use ``mode = "math"`` to indicate something
    that appears in one formula.


info::
    Two global dictionaries are used : ``CHARS_TO_ESCAPE`` indicates only
    characters that must be escaped whit one backslash ``\``, and
    ``CHARS_TO_LATEXIFY`` is for expressions that needs one LaTeX command.
    """
    if mode not in CHARS_TO_ESCAPE:
        raise ValueError(
            "unknown mode : << {0} >>.".format(mode)
        )

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
-----------------
Small description
-----------------

This class defines methods related to the compilation of LaTeX documents.


-------------
The arguments
-------------

This class uses the following variables.

    1) ``path`` is the path of the LaTeX file to compile.

    2) ``repeat`` indicates how many compilations must be done (for example, if
    the document has one table of content, several compilations are needed). By
    default, ``repeat = 1``.

    3) ``isverbose`` is a boolean with default value ``True``. Use ``isverbose``
    if you want to see, or not to see, the informations sent by LaTeX when it
    does the compilation.
    """
# Source :
#    * http://docs.python.org/py3k/library/subprocess.html
    SUBPROCESS_METHOD = {
# ``check_call`` prints informations given during the compilation.
        True : check_call ,
# ``check_output`` does not print informations given during the
# compilation. Indeed it returns all this stuff in one string.
        False: check_output
    }

    def __init__(
        self,
        path,
        repeat    = 1,
        isverbose = True
    ):
# Does the file to compile exist ?
        if not os_use.isfile(path):
            _raise_ioerror(
                kind   = "file",
                path   = path,
                action = "exist"
            )

# Do we have TEX file ?
        if os_use.ext(path) != "tex":
            _raise_ioerror(
                kind   = "file",
                path   = path,
                action = "notTeX"
            )

# Infos given by the user.
        self.path      = path
        self.pathnoext = os_use.filename(path)

        self.repeat    = repeat
        self.isverbose = isverbose

# General infos about the LaTeX distribution and the OS.
        self.aboutlatex = about()

# The directory where to put the "paper" files.
        self.directory = os_use.parentdir(path)

    def _compile(
        self,
        arguments,
        repeat
    ):
        """
This method launches the compilation in verbose mode or not.
        """
        subprocess_method = self.SUBPROCESS_METHOD[self.isverbose]

        for i in range(1, repeat + 1):
            if self.isverbose:
                print('\t+ Start of compilation Nb.{0} +'.format(i))

            subprocess_method(
# We go in the directory of the file to compile.
                cwd = self.directory,
# We use the terminal actions.
                args = arguments
            )

            if self.isverbose:
                print('\t+ End of compilation Nb.{0} +'.format(i))

    def pdf(
        self,
        repeat = None
    ):
        """
This method calls LaTeX so as to build the PDF output.
        """
        if repeat == None:
            repeat = self.repeat

# The option "-interaction=nonstopmode" don't stop the terminal even if there is
# an error found by ¨latex.
        self._compile(
            arguments = [
                'pdflatex',
                '-interaction=nonstopmode',
                self.path
            ],
            repeat = repeat
        )


# -------------- #
# -- CLEANING -- #
# -------------- #

TEMP_EXTS     = latex.TEMP_EXTS
EXTS_TO_CLEAN = latex.EXTS_TO_CLEAN

def clean(
    main,
    keep      = [],
    discard   = EXTS_TO_CLEAN,
    depth     = 0,
    isverbose = False
):
    """
-----------------
Small description
-----------------

This function removes extra files build during a LaTeX compilation.


-------------
The arguments
-------------

This function uses the following variables.

    1) ``main`` will be either one instance of the class ``Build`` or the path
    of one file or of one directory.

    In the case of one instance of the class ``Build`` or of one file, only the
    file having the same name of the file build, or indicated, will be
    removed.

    If ``main`` is the path of one directory, then the function will look for
    all files with path::``tex`` extension, and then the eventual extra files
    associated will be removed. In that case, you can use the two arguments
    ``depth`` and ``isverbose``.

    2) ``keep`` is for indicate the list of extensions to keep. This can be very
    usefull if you use the default value of the argument ``discard``.

    3) ``discard`` is for indicate the list of extensions to discard. By
    default, the extensions to clean are defined in the constant
    ``EXTS_TO_CLEAN``.

    info::
        If you want to build your own list of extensions you can use the
        dictionary ``TEMP_EXTS``.

    4) ``depth`` is the maximal depth for the research of the path::``tex``
    files when ``main`` is the path of one directory. The very special value
    ``(-1)`` indicates that there is no maximum. The default value is ``0``
    which asks to only look for in the direct content of the main directory to
    analyse.

    5) ``isverbose`` is a boolean which asks to print in one terminal the
    path::``tex`` files found when one search is made inside one directory. This
    argument is usefull only if ``main`` is the path of one directory.
    """
# One instance of ``Build()``
    if isinstance(main, Build):
        allpathsnoext = [main.pathnoext]

# One file
    elif os_use.isfile(main):
        if os_use.ext(main) != "tex":
            _raise_ioerror(
                kind   = "file",
                path   = main,
                action = "notTeX"
            )

        allpathsnoext = [main[:-4]]

# One directory
    elif os_use.isdir(main):
        allpathsnoext = [
            file[:-4]
            for file in os_use.nextfile(
                main  = main,
                exts  = {'keep': ["tex"]},
                depth = depth
            )
        ]

# Nothing existing
    else:
        allpathsnoext = []

# Clean now !
    for pathnoext in allpathsnoext:
        if isverbose:
            print('---> "{0}.tex"'.format(pathnoext))

        for ext in [x for x in discard if x not in keep]:
            if '¨' in ext:
                print("TODO  --->  ", ext)

            else:
                os_use.destroy(pathnoext + '.' + ext)


# ---------------------------------- #
# -- ABOUT THE LATEX DISTRIBUTION -- #
# ---------------------------------- #

# Sources :
#    * http://tex.stackexchange.com/questions/68730/terminal-commands-to-have-information-about-latex-distribution
#    * http://tex.stackexchange.com/questions/69483/create-a-local-texmf-tree-in-miktex
#    * https://groups.google.com/forum/?hl=fr&fromgroups=#!topic/fr.comp.text.tex/ivuCnUlW7i8

def localdir_miketex():
    """
You can redefine this function to choose another path than
path::``C:/texmf-local`` for the directory where we'll put special LaTeX
packages.


warning::
    Customize this function only if you know what you are doing !
    """
    return 'C:/texmf-local'

def _localdir_texlive(
    osname = None
):
    """
This function returns the path of the TeX Live directory where we'll put special
LaTeX packages.
    """
    if osname == None:
        osname = os_use.system()

# "check_output" is a byte string, so we have to use the method
# "decode" so as to obtain an "utf-8" string.
    try:
        if osname == "windows":
            localdir = check_output(
                args = ['kpsexpand',"'$TEXMFLOCAL'"]
            ).decode('utf8')

            return normpath(localdir.strip())

        elif osname in ["linux", "mac"]:
            localdir = check_output(
                args = ['kpsewhich','--var-value=TEXMFLOCAL']
            ).decode('utf8')

            return normpath(localdir.strip())

    except:
        ...

def about():
    """
The aim of this function is to give critical informations so to use the function
``install`.

This function returns the following kind of dictionary. This example has been
obtained with a Mac computer where TeXlive is installed.

python::
    {
        'osname'    : 'mac',
        'latexname' : 'texlive',
        'latexfound': True,
        'localdir'  : '/usr/local/texlive/texmf-local'
    }

The key ``'localdir'`` contains the path to use to install special packages.
    """
    osname = os_use.system()

    latexfound = False
    latexname  = ''
    localdir   = None

# Windows
    if osname == "windows":
        winpath = os_use.pathenv()

# Is MiKTeX installed ?
        if '\\miktex\\' in winpath:
            latexfound = True
            latexname  = 'miktex'

            if os_use.isdir(localdir_miketex()):
                localdir = localdir_miketex()

# Is TeX Live installed ?
        elif '\\texlive\\' in winpath:
            latexfound = True
            latexname  = 'texlive'
            localdir   = _localdir_texlive(osname)

# Linux and Mac
    elif osname in ["linux", "mac"]:
# Is LaTeX installed ?
        try:
            if check_output(args = ['which', 'pdftex']).strip():
                latexfound = True
                latexname  = 'texlive'
                localdir   = _localdir_texlive(osname)

        except CalledProcessError:
            ...

# Unknown method...
    else:
        raise OSError(
            "the OS << {0} >> is not supported. ".format(osname)
        )

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

def _issu(localdir_latex):
    """
This function tests if the script has been launched by the "Super User".
    """
    tempfile = join(
        localdir_latex,
        '-p-y-t-o-o-l-t-e-s-t-.t-x-t-x-t'
    )

    try:
        os_use.maketxtfile(tempfile)
        os_use.destroy(tempfile)

    except:
        _raise_ioerror(
            kind   = "directory",
            path   = localdir_latex,
            action = "access"
        )

def make_localdir_miktex():
    """
This function creates one local directory and add it to the list of directories
analysed by MiKTeX when it looks for packages.

The path of the local directory is given by ``localdir_miketex()``
because this variable is also used by the function ``about`` and ``install``.

Even it is a really bad idea, you can change this path just after the
importation of the module ``latexUse``.
    """
    aboutlatex = about()

    if aboutlatex['osname'] != "windows" \
    or aboutlatex['latexname'] != "miktex":
        raise OSError(
            'this function can only be used with the OS "window" '
            'and the LaTeX distribution "miktex".'
        )

# Creation of the directory
    try:
        os_use.makedir(localdir_miketex())

    except:
        _raise_ioerror(
            kind   = "directory",
            path   = localdir_miketex(),
            action = "create"
        )

# Adding the directory to the ones analysed by MiKTex.
    check_output(
        args = [
            'initexmf',
            '--admin',
            '--user-roots=' + localdir_miketex(),
#           '--register-root=' + localdir_miketex(),
            '--verbose'
        ]
    )

    check_output(
        args = [
            'initexmf',
            '--update-fndb',
            '--verbose'
            ]
        )

    print(
        '',
        'The following local directory for MiKTeX has been created.',
        '\t<< {0} >>'.format(localdir_miketex()),
        sep = "\n"
    )

def refresh(
    aboutlatex = None
):
    """
This function refreshes the list of packages directly known by the LaTeX
distribution. This always works in verbose mode (LaTeX is not very talkative
when it refreshes).

The only variable used is ``aboutlatex`` which is simply the informations
returned by the function ``about``.
    """
    if aboutlatex == None:
        aboutlatex = about()

# TeX Live
    if aboutlatex['latexname'] == 'texlive':
        check_call(args = ['mktexlsr'])

# MiKTex
    elif aboutlatex['latexname'] == 'miktex':
        check_call(args = ['initexmf', '--update-fndb', '--verbose'])

# Unkonwn !!!
    else:
        raise LatexError(
            'the refresh of the list of LaTeX packages is not supported '
            'with your LaTeX distribution.'
        )

def install(
    paths,
    name,
    clean = False
):
    """
-----------------
Small description
-----------------

This function helps you to easily install unofficial packages to your LaTeX
distribution.


warning::
    This function can only be called by one script launched by the super user.


-------------
The arguments
-------------

This function uses the following variables.

    1) ``name`` is the name of the LaTeX package to build.

    2) ``paths`` is the list of all the paths of the files to copy. This
    variable can be easily build with the function ``listFile`` from the module
    ``os_use`` contained in the ¨python package ``Mistool``. The tree structure
    will be similar to the one corresponding to the files to copy.

    3) ``clean`` is boolean variable to delete or not an eventual package
    directory named ``name`` in the local directory of the LaTeX distribution.
    The default value of ``clean`` is ``False``.
    """
# Sources :
#    * http://www.commentcamarche.net/forum/affich-7670740-linux-supprimer-le-contenu-d-un-repertoire
#    * http://stackoverflow.com/questions/185936/delete-folder-contents-in-python

# Directories
    aboutlatex = about()

    localdir_latex = aboutlatex['localdir']

    if localdir_latex == None:
        message = "no local directory for special packages has been found."

        if aboutlatex['latexname'] == "miktex":
            message += "You can use the function << make_localdir_miktex >>."

        raise LatexError(message)

    localdir_latex = os_use.SEP.join([
        localdir_latex,
        'tex',
        'latex',
        name
    ])

# We must have the super user's rights with the local Latex directory.
    _issu(localdir_latex)

# We must find the smaller directory that contains all the files so as to
# respect the original tree directory structure.
    maindir = os_use.commonpath(listFile)

# Directories to add
    directories_and_files = {}

    for onepath in paths:
        if not os_use.isfile(onepath):
            _raise_ioerror(
                kind   = "file",
                path   = onepath,
                action = "exist"
            )

        localsubdir_latex = localdir_latex + os_use.parentDir(
            os_use.relativePath(maindir, onepath)
        ).strip()

        if localsubdir_latex in directories_and_files:
            directories_and_files[localsubdir_latex].append(onepath)
        else:
            directories_and_files[localsubdir_latex] = [onepath]

# Installation on Mac O$, Linux and Windows
    if aboutlatex['osname'] in ['mac', 'linux', 'windows']:
# Actions to do are...
        actions      = []
        decotab      = '    * '
        decotab_plus = '        + '
        decotab_more = '            - '

# Creation of directories and copy of the files
#
#    1) Deletion of a local package named ``name``
        if clean and os_use.isdir(localdir_latex):
            print(
                decotab + 'Deletion of the old << {0} >> '.format(name) \
                + 'package in the local LaTeX directory.'
            )

            os_use.destroy(localdir_latex)

#    2) Creation of the new local package named ``name``
        print(
            decotab + 'Creation of the new << {0} >> '.format(name) \
            + 'package in the local LaTeX directory.'
        )

#    3) Creation of the new directories with their contents
        for newdir in sorted(directories_and_files.keys()):
            print(
                decotab_plus + 'Adding new directory --> << {0} >> '.format(
                    newdir
                )
            )

            os_use.makedir(newdir)

            for onepath in directories_and_files[newdir]:
                if not os_use.isfile(onepath):
                    _raise_ioerror(
                        kind   = "file",
                        path   = onepath,
                        action = "exist"
                    )

                print(
                    decotab_more + 'Adding new file  --> << {0} >> '.format(
                        os_use.fileName(onepath) \
                        + "." \
                        + os_use.ext(onepath)
                    )
                )

                localsubdir_latex = localdir_latex + os_use.parentDir(
                    os_use.relativePath(maindir, onepath)
                ).strip()

                os_use.copy(onepath, localsubdir_latex)

#   We must refresh of the list of LaTeX packages.
        print(
            decotab + 'Refreshing the list of LaTeX packages.'
        )

        refresh(aboutlatex)

# Unsupported OS
    else:
        raise LatexError(
            'the installation of local packages is not yet supported '
            'with the OS << {0} >>.'.format(aboutlatex['osname'])
        )
