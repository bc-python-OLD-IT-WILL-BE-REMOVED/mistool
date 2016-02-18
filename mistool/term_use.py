#!/usr/bin/env python3

"""
prototype::
    date = 2015-11-03


This module contains mainly classes and functions producing strings useful to be
printed in a terminal.
"""

from mistool.config.frame import ALL_FRAMES
from mistool.latex_use import escape as latex_escape
from mistool.os_use import (
    _ALL,
    _DIR,
    _EMPTY,
    _FILE, _FILE_DIR_QUERIES,
    _NOT,
    _OTHER_FILES,
    _RELSEARCH,
    _XTRA,
    PPath
)


# ------------------ #
# -- STEP BY STEP -- #
# ------------------ #

class Step:
    """
prototype::
    arg = int: start = 1 ;
          the first number used for the steps
    arg = func: textit = lambda n, t: "{0}) {1}".format(n, t) ;
          the function called to make the text corresponding to one action using
          two variables two variables ``n`` for the number, and ``t`` for the
          users's text
    arg = bool: isprinted = True ;
          this is to ask to print the texts in the terminal
    arg = bool: isreturned = False ;
          this is to ask to return the texts

    action = this tiny class allows to print ¨andor obtain texts for step by
             step actions that are automatically numbered.


==============
For a terminal
==============

When offers a console application, or to do a log file, it may be convenient to
have ¨infos given step by step. The class ``Step`` is doing for that. Here is
a toy example.

pyterm::
    >>> from mistool.term_use import Step
    >>> mysteps = Step()
    >>> i = 0
    >>> while i <= 12:
    ...     if i % 2:
    ...         mysteps("Action #{0}".format(i))
    ...     i += 1
    ...
    1) Action #1
    2) Action #3
    3) Action #5
    4) Action #7
    5) Action #9
    6) Action #11


==========
For a file
==========

The text can be returned when you call an instance of ``Step`` so you can do
something else than print the steps in a terminal. You can even ask to not print
anything.
Here is an example where the actions are just put in a file with the long path
path::``/Users/projetmbc/file.log`` (you can also use ``mistool.os_use`` for the
actions on files).

python::
    from pathlib import Path
    from mistool.term_use import Step
    mysteps = Step(
        isprinted  = False,
        isreturned = True
    )
    myfile = Path("/Users/projetmbc/file.log")
    with myfile.open(
        mode     = "w",
        encoding = "utf-8"
    ) as file:
        for i in range(0, 4):
            text = mysteps("Text #{0}".format(i))
            file.write(text)
            file.write("\n")


Suppose that our python script is in a file with the long path
path::``/Users/projetmbc/stepit.py``, and suppose also that ¨python can be
launched using term::``python``, then here is what you should see in a terminal
(nothing is printed).

term::
    > python3 stepit.py


If we open now the file path::``file.log``, its content is the following one.

log::
    1) Text #0
    2) Text #1
    3) Text #2
    4) Text #3


info::
    ¨latex prints and puts in a file its logging ¨infos. This kind of double
    logging can be done using ``Step(isreturned = True)`` (remember that by
    default we have ``isprinted = True``).


=======================
Another starting number
=======================

If you need to start the numbering at `7` instead of `1` for example, you can
just do as below.

pyterm::
    >>> from mistool.term_use import Step
    >>> mysteps = Step(start = 7)
    >>> for i in range(1, 6):
    ...     mysteps("Text #{0}".format(i))
    ...
    7) Text #1
    8) Text #2
    9) Text #3
    10) Text #4
    11) Text #5


===================================
Choose the way things are displayed
===================================

The texts for the actions are made using the argument ``textit`` which must be a
function of two variables ``n`` for the number, and ``t`` for the users's text.
Here is an ugly but assumed example.

pyterm::
    >>> from mistool.term_use import Step
    >>> mysteps = Step(
        textit = lambda n, t: "[{0}]-->> [[ {1} ]] <<--[{0}]".format(n, t)
    )
    >>> for i in range(1, 6):
    ...     mysteps("Text #{0}".format(i))
    ...
    [1]-->> [[ Text #1 ]] <<--[1]
    [2]-->> [[ Text #2 ]] <<--[2]
    [3]-->> [[ Text #3 ]] <<--[3]
    [4]-->> [[ Text #4 ]] <<--[4]
    [5]-->> [[ Text #5 ]] <<--[5]
    """
    def __init__(
        self,
        start      = 1,
        textit     = lambda n, t: "{0}) {1}".format(n, t),
        isprinted  = True,
        isreturned = False
    ):
        self.nb         = start
        self.textit     = textit
        self.isprinted  = isprinted
        self.isreturned = isreturned


    def __call__(
        self,
        text
    ):
        """
prototype::
    arg = str: text ;
          the text for the actual step is build using ``self.textit``, and
          then it is printed ¨andor returned regarding to the values of
          ``self.isprinted`` and ``self.isreturned``.
        """
        text = self.textit(n = self.nb, t = text)

        if self.isprinted:
            print(text)

        self.nb += 1

        if self.isreturned:
            return text


# -------------------- #
# -- TEXTUAL FRAMES -- #
# -------------------- #

DEFAULT_FRAME = ALL_FRAMES['python_basic']

# Source: https://docs.python.org/3/library/string.html#format-specification-mini-language
_ALIGNMENTS = {
    'left'  : "<",
    'center': "^",
    'right' : ">"
}
_LONG_ALIGNMENTS = {x[0]: x for x in _ALIGNMENTS}

def withframe(
    text,
    frame = DEFAULT_FRAME,
    align = "left"
):
    """
prototype::
    see = showallframes , buildframe

    arg = str: text ;
          the text to put inside a frame
    arg = {str: str}: frame = DEFAULT_FRAME ;
          this dictionary indicates how to draw the frame (you can easily add
          new frames with the help of the function ``buildframe``)
    arg = str: align = "left" ;
          this indicates how to align the text inside the frame

    return = str ;
             the text put inside a frame


=========
BASIC USE
=========

Let's see how ``withframe`` works with the default parameters.

pyterm::
    >>> from mistool.term_use import withframe
    >>> text = '''
    ... One small
    ... text
    ... to do tests
    ... '''.strip()
    >>> print(withframe(text))
    ###############
    # One small   #
    # text        #
    # to do tests #
    ###############


Easy to use but can we use other frames. Yes we can first use the frames stored
in the dictionary ``ALL_FRAMES``.

pyterm::
    >>> from mistool.term_use import withframe, ALL_FRAMES
    >>> text = '''
    ... One small
    ... text
    ... to do tests
    ... '''.strip()
    >>> frame = ALL_FRAMES["python_pretty"]
    >>> print(
    ...     withframe(
    ...         text  = text,
    ...         frame = frame
    ...     )
    ... )
    # ----------------- #
    # -- One small   -- #
    # -- text        -- #
    # -- to do tests -- #
    # ----------------- #


info::
    There is one section after will give you an easy way to see all the default
    frames stored in the dictionary ``ALL_FRAMES``.


=========
ALIGNMENT
=========

By default the text is left aligned but you can center it or right align it.
Here is how to do that.

pyterm::
    >>> from mistool.term_use import withframe
    >>> text = '''
    ... One small
    ... text
    ... to do tests
    ... '''.strip()
    >>> print(withframe(text))
    ###############
    # One small   #
    # text        #
    # to do tests #
    ###############

    >>> print(withframe(text = text, align = "center"))
    ###############
    #  One small  #
    #    text     #
    # to do tests #
    ###############

    >>> print(withframe(text = text, align = "right"))
    ###############
    #   One small #
    #        text #
    # to do tests #
    ###############


================================
ALL THE DEFAULT FRAMES AVAILABLE
================================

Using the two lines below you can see all the default frames with their names
indicated after the arrow ``---->`` (in the output, term::``[...]`` indicates
that lines have been cut).

pyterm::
    >>> from mistool.term_use import showallframes
    >>> showallframes()

    ----> ascii_star

    ***************
    * One small   *
    * text        *
    * to do tests *
    ***************


    ----> c_basic

    /***************
     * One small   *
     * text        *
     * to do tests *
     ***************/

    [...]


=======================================
HOW TO DEFINE AND USE AN HOMEMADE FRAME
=======================================

Just take a look at the documentation of the function ``buildframe`` that allows
to build very easily a "frame" dictionary that can be used with ``withframe``.
    """
# Long name of the position
    align = _LONG_ALIGNMENTS.get(align, align)

    if align not in _ALIGNMENTS:
        raise ValueError("unknown name for the positionning of the text.")

# The lines of the text.
    lines = [x for x in text.splitlines()]
    width = max([len(x) for x in lines])

# Formatting each line of text inside the frame.
    howtoput = '{' + ':{0}{1}'.format(
        _ALIGNMENTS[align],
        width
    ) + '}'

    lines = [howtoput.format(x) for x in lines]

# The frame
    frametexts = []

# First rule
    hrule = "{0}{1}{2}".format(
        frame["upleft"],
        frame["uprule"]*width,
        frame["upright"]
    )

    if hrule:
        frametexts.append(hrule)

# Inside
    for oneline in lines:
        frametexts.append(
            "{0}{1}{2}".format(
                frame["left"],
                oneline,
                frame["right"]
            )
        )

# Last rule
    hrule = "{0}{1}{2}".format(
        frame["downleft"],
        frame["downrule"]*width,
        frame["downright"]
    )

    if hrule:
        frametexts.append(hrule)

# Here we are...
    return "\n".join(frametexts)


def showallframes():
    """
prototype::
    action = this function prints all the available kinds of frames and shows
             how they "work"
    """
    text = """
One small
text
to do tests
    """.strip()

    for name in sorted(ALL_FRAMES.keys()):
        print(
            "",
            "----> {0}".format(name),
            "",
            withframe(text = text, frame = ALL_FRAMES[name]),
            "",
            sep = "\n"
        )


def buildframe(text):
    """
prototype::
    arg = str: text ;
          a text representatiing a frame with its content indicated using
          ``{text}`` (see the example)

    return = {str: str} ;
             a dictionary that can be used with the argument ``frame`` of the
             function ``withframe``


To understand how this function has to be used, let's suppose we want to define
the following ugly frame.

code::
    @@ --------------------%%
       |-> One small   <-+
       |-> text        <-+
       |-> to do tests <-+
    &&==================== $$


To do that, you just have to use the special string ``{text}`` instead of a real
text as we have done in the following text.

code::
    @@ --------------%%
       |-> {text} <-+
    &&=============== $$


This string can be directly given to the function ``buildframe`` that will return
a dictionary directly usable with the function ``withframe``. That's all !

pyterm::
    >>> from mistool.term_use import buildframe
    >>> frame = buildframe(
    ...     '''
    ... @@ --------------%%
    ...    |-> {text} <-+
    ... &&=============== $$
    ...     '''.strip()
    ... )
    >>> print(frame)
    {
    # UP
        'upleft' : '@@ ----',
        'uprule' : '-',
        'upright': '----%%',
    # INSIDE
        'left' : '   |-> ',
        'right': ' <-+',
    # DOWN
        'downleft' : '&&=====',
        'downrule' : '=',
        'downright': '==== $$'
    }


warning::
    Only one character can be used upon ``{text}``, and the same is true below
    ``{text}``, but you can use one character upside, and another downside as we
    have done. This restriction comes from the different width of texts that can
    be framed.
    """
# The lines used
    lines = text.splitlines()

# Do we have a good number of lines ?
    nblines = len(lines)

    if nblines == 0 or nblines > 3:
        raise ValueError(
            "you must use at least one line and at most three lines."
        )

# Up, inside and down
    inside = None
    for i in range(nblines):
        if "{text}" in lines[i]:
            if nblines == 3 and (i == 0 or i == 2):
                raise ValueError("the line with ``{text}`` is misplaced.")

            inside = lines[i]

            if nblines == 1:
                lines = [""] + lines + [""]

            elif nblines == 2:
                if i == 0:
                    lines = [""] + lines

                else:
                    lines = lines + [""]

            up, inside, down = lines

            break

    if inside == None:
        raise ValueError("the line with ``{text}`` is missing.")

# Near to the end...
    start = inside.find('{text}')
    end   = start + 6

    frame = {
    # UP
        "upleft" : up[:start],
        "upright": up[end:],
    # INSIDE
        "left" : inside[:start],
        "right": inside[end:],
    # DOWN
        "downleft" : down[:start],
        "downright": down[end:],
    }

    if len(set(up[start:end])) != 1:
        raise ValueError(
            "only one character can be used to draw the line upside the text."
        )

    frame["uprule"] = up[start]

    if len(set(down[start:end])) != 1:
        raise ValueError(
            "only one character can be used to draw the line downside the text."
        )

    frame["downrule"] = down[start]

    return frame


# ----------------------- #
# -- VIEWS OF A FOLDER -- #
# ----------------------- #

class DirView:
    """
prototype::
    type = cls ;
           this class allows to display in different formats the tree structure
           of one directory with the extra possibility to keep and show only
           some informations, and also to set a little the format of the output

    see = os_use._ppath_regpath2meta, os_use._ppath_walk

    arg-attr = os_use.PPath: ppath ;
               this argument is the path of the directory to analyze
    arg-attr = str: regpath = "**" ;
               this argument follows some rules named "regpath" rules so as to
               choose the files and the directories that must be kept (see the
               documentation of ``os_use._ppath_regpath2meta``)
    arg-attr = str: display = "main short" in self._FORMATS;
               this argument gives informations about the output to produce (you
               can just use the initials of the options)
    arg-attr = str: sorting = "alpha" in [x[0] for x in cls.LAMBDA_SORT] or
                                      in [x[1] for x in cls.LAMBDA_SORT];
               this argument inidcates the way to sort the paths found

    clsattr = {(str, str): (lambda, ?)}: LAMBDA_SORT ;
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
        + doc
            * code_A.py
            * code_B.py
            * slide_A.pdf
            * slide_B.pdf
            + licence
                * doc.pdf
        + emptydir


==============
The ascii tree
==============

Let's start with the default output for the ¨ascii tree. In the following code,
in the text printed, the files and the folders are sorting regarding their names
(this text follows the syntax used to generate the view of the folders used in
the documentation that you are reading).

pyterm::
>>> from mistool.term_use import DirView, PPath
>>> dir     = PPath("/Users/projetmbc/dir")
>>> dirview = DirView(dir)
>>> print(dirview.ascii)
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
``sorting``. Here is an example of use where we must add the option ``"main"``
for ``display`` so as to see the main folder.

pyterm::
    >>> from mistool.term_use import DirView, PPath
    >>> dir     = PPath("/Users/projetmbc/dir")
    >>> dirview = DirView(
    ...     ppath   = dir,
    ...     display = "main relative",
    ...     sorting = "filefirst"
    ... )
    >>> print(dirview.ascii)
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
asks to keep only the files with the extension path::``py``. You can see that
the empty folders are given, and that the other files than the ones wanted are
indicated by ellipsis, this ones being always sorted at the end of the files.

pyterm::
    >>> from mistool.term_use import DirView, PPath
    >>> dir     = PPath("/Users/projetmbc/dir")
    >>> dirview = DirView(
    ...     ppath   = dir,
    ...     regpath = "file::**.py"
    ... )
    >>> print(dirview.ascii)
    + dir
        * code_1.py
        * code_2.py
        + doc
            * code_A.py
            * code_B.py
            + licence
                * ...
            * ...
        + emptydir
        * ...


If you use the option ``display = "main short found"`` instead of the default
one ``display = "main short"``, then the output will only show the files found
as above, and the empty folders will not be given.

pyterm::
    >>> from mistool.term_use import DirView, PPath
    >>> dir     = PPath("/Users/projetmbc/dir")
    >>> dirview = DirView(
    ...     ppath   = dir,
    ...     regpath = "file::**.py",
    ...     display = "main short found"
    ... )
    >>> print(dirview.ascii)
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

By default, ``dirview.tree`` give a tree view using rules similar to the ones
you can see in ¨gui applications displaying tree structure of a folder. Here we
use only ¨utf8 characters.

term::
    ╸dir
     ┣━ ╸code_1.py
     ┣━ ╸code_2.py
     ┣━ ╸file_1.txt
     ┣━ ╸file_2.txt
     ┣━ ╸doc
     ┃   ┣━ ╸code_A.py
     ┃   ┣━ ╸code_B.py
     ┃   ┣━ ╸slide_A.pdf
     ┃   ┣━ ╸slide_B.pdf
     ┃   ┗━ ╸licence
     ┃       ┗━ ╸doc.pdf
     ┗━ ╸emptydir


=====================
The "toc" like output
=====================

Using ``dirview.toc`` with the sorting option ``sorting = "filefirst"``, this is
the better sorting option here, you will obtain the following output which looks
like a kind of table of contents with sections for folders, and subsections for
files.

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
    analyzed. Paths formatting options apply only to files.


===================================================
A ¨latex version for the package latex::``dirtree``
===================================================

By default, using ``dirview.latex`` you will have the following ¨latex code
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

The optional string argument ``display``, or the attribut with the same name
``display``, can be made of one or several of the following values separated by
spaces where each name can be replaced by its initial.

    a) ``long`` asks to display the whole paths of the files and directories
    found.

    b) ``relative`` asks to display relative paths comparing to the main
    directory analysed.

    c) ``short`` asks to only display names of directories found, and of the
    files found with their extensions.

    d) ``main`` asks to display the main directory which is analyzed.

    e) ``found`` asks to only display directories and files with a path matching
    the pattern ``regpath``. If ``found`` is not given, then ellipsis will be
    used to indicate unmatching files and the empty directory will be always
    given.


=======================
All the sorting options
=======================

The optional string argument ``sorting``, or the attribut with the same name
``sorting``, can be one of the following values (each name can be replaced by
its initial).

    a) ``alpha`` is the alphabetic sorting on the strings representing the paths.

    b) ``filefirst`` gathers first the files and then the folders, and in each
    of this category an alphabetic sorting is applied.

    c) ``name`` first sorts the objects regarding only their name without the
    extension, and if a file and a folder have the same position, then the file
    will be put before the directory.

    d) ``date`` simply used the date of the last physical changes.


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
            ("name", "n"): [
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

        1) The keys are tuples ``(name, shortcut)`` of two strings.

        2) The values are lists of two elements.

            a) The ¨1ST element is a lambda function that will give the values
            used for the sorting.
            Here ``x`` is a dictionary stored in ``self.listview`` (see the
            documentation of the method ``self.buildviews``).

            b) The ¨2ND element is the special value used for the sorting when
            special ellipsis ``"..."`` is met (ellipsis are used to indicate
            unmatching files).
    """
    _ELLIPSIS = "..."

    ASCII_DECOS = {
        k: v
        for v, keys in {
            "+"  : [_DIR, _EMPTY, _OTHER_FILES],
            "*"  : [_FILE],
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
        ("name", "n"): [
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
    _INTERNAL_QUERIES = set([_XTRA, _FILE, _DIR])

    def __init__(
        self,
        ppath,
        regpath = "**",
        display = "main short",
        sorting = "alpha"
    ):
# General settings
        self._mustberebuilt = True

        self._LAMBDA_SORT_LONGNAMES = {
            k[0]: v for k, v in self.LAMBDA_SORT.items()
        }

        self._sorting_long_names = {x[1]: x[0] for x in self.LAMBDA_SORT}

        self._display_long_names = {x[0]: x for x in self._FORMATS}

# Verifications are done by the build method !
        self.ppath   = ppath
        self.regpath = regpath
        self.display = display
        self.sorting = sorting


# --------------------- #
# -- SPECIAL SETTERS -- #
# --------------------- #

    @property
    def ppath(self):
        return self._ppath

    @ppath.setter
    def ppath(self, value):
# Do we have a folder ?
        if not value.is_dir():
            raise OSError("``ppath`` doesn't point to a directory.")

        self._ppath         = value
        self._mustberebuilt = True


    @property
    def regpath(self):
        return self._regpath

    @regpath.setter
    def regpath(self, value):
        self._regpath       = value
        self._mustberebuilt = True


    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, value):
        self._display = set(
            self._display_long_names.get(x.strip(), x.strip())
            for x in value.split(" ")
            if x.strip()
        )

        if not self._display <= self._FORMATS:
            raise ValueError("illegal formatting rule (see ``display``).")

        nb_path_formats = len(self._display & self._PATH_FORMATS)

        if nb_path_formats == 0:
            self._display.add(self._SHORT_PATH)

        elif nb_path_formats != 1:
            raise ValueError(
                "several path formatting rules (see ``display``)."
            )

        self._mustberebuilt = True


    @property
    def sorting(self):
        return self._sorting

    @sorting.setter
    def sorting(self, value):
        self._sorting = self._sorting_long_names.get(value, value)

        if self._sorting not in self._LAMBDA_SORT_LONGNAMES:
            raise ValueError("unknown sorting rule.")

        self._mustberebuilt = True


# -------------------- #
# -- INTERNAL VIEWS -- #
# -------------------- #

    def buildviews(self):
        """
prototype::
    see = self.sort , self.ascii , self.latex , self.toc , self.tree

    action = this method builds one flat list ``self.listview`` of dictionaries,
             that store all the informations about the directory even the empty
             folders and the unmatching files.
             This method also builds ``self.treeview`` another list of
             dictionaries which is like the natural tree structure of the folder
             analyzed (both of this objects are sorted regarding to the value of
             the attribut ``self.sorting``)


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
                 (this can also be an extra path)
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
# Regpath infos
        queries, pattern = self.ppath.regpath2meta(
            self.regpath,
            regexit = False
        )

        allqueries = queries | self._INTERNAL_QUERIES
        allregpath = "{0}::{1}".format(" ".join(allqueries), pattern)

        self._extradepth = int(self._MAIN_PATH in self._display)

        self._all_listview = [
            {
                'tag'  : tag,
                'depth': ppath.depth_in(self.ppath) + self._extradepth,
                'ppath': ppath
            }
            for ppath, tag in self.ppath.walk(
                regpath  = allregpath,
                givetags = True
            )
        ]

        self._filedir_queries = queries & _FILE_DIR_QUERIES

# We can now do the job.
        self._build_listview()
        self._build_treeview()

        self.sort()

        self._mustberebuilt = False


    def _build_listview(self):
        """
prototype::
    see = self.buildviews

    action = the attribut ``self.listview`` is build using the attribut
             ``self._all_listview``
        """
# Sub fles and folders found
        addall    = bool(self._ONLY_FOUND_PATHS not in self._display)
        _listview = []

        for metadatas in self._all_listview:
            addthis = bool(
                self._MAIN_PATH in self._display
                or
                metadatas['ppath'] != self.ppath
            )

            if metadatas['tag'] in [_EMPTY, _OTHER_FILES]:
                if addall:
                    if addthis:
                        _listview.append(metadatas)

                    if metadatas['tag'] == _OTHER_FILES:
                        _listview.append({
                            'tag'  : _FILE,
                            'depth': metadatas['depth'] + 1,
                            'ppath': metadatas['ppath'] / self._ELLIPSIS
                        })

            elif metadatas['tag'] in self._filedir_queries:
                if addthis:
                    _listview.append(metadatas)

        _listview.sort(key = lambda x: str(x['ppath']))


# We have to find folders with only unmacthing files or with matching and
# unmacthing files, and also all the parent directories.
#
# Main or not main, that is the question.
        if self._MAIN_PATH in self._display:
            if _listview \
            and _listview[0]["ppath"] != self.ppath:
                self.listview = [{
                    'tag'  : _DIR,
                    'depth': 0,
                    'ppath': self.ppath
                }]

            else:
                self.listview = []

            lastreldirs   = [PPath('.')]

        else:
            self.listview = []
            lastreldirs   = []

        for metadatas in _listview:
            relpath = metadatas['ppath'].relative_to(self.ppath)
            parents = relpath.parents

# We have to add all the parent directories !
            if "dir" in metadatas['tag']:
                lastreldirs.append(metadatas['ppath'].relative_to(self.ppath))

            else:
                for parent in reversed(parents):
                    if parent not in lastreldirs:
                        ppath = self.ppath / parent

                        if self._MAIN_PATH in self._display \
                        or ppath != self.ppath:
                            self.listview.insert(
                                -1,
                                {
                                    'tag'  : _DIR,
                                    'depth': ppath.depth_in(self.ppath) \
                                             + self._extradepth,
                                    'ppath': ppath
                                }
                            )

                        lastreldirs.append(parent)

            self.listview.append(metadatas)

    def _build_treeview(self):
        """
prototype::
    see = self.buildviews , self._rbuild_treeview

    action = this method returns the attribut ``self.treeview`` but all the
             job is done recursively by the method ``self._rbuild_treeview``
        """
        self.treeview = self._rbuild_treeview(self.listview)


    def _rbuild_treeview(self, listview):
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
            if metadatas['tag'] == _FILE:
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

                else:
                    metadatas['content'] = []

                treeview.append(metadatas)

        return treeview


# ------------- #
# -- SORTING -- #
# ------------- #

    def _ellipsis_sort(self, metadatas):
        """
prototype::
    see = self.buildviews , self._metadatas

    arg = dict: metadatas

    return = str ;
             the value to use for the sorting
        """
        if metadatas['ppath'].name == self._ELLIPSIS:
            return self._ellipsi_sort_value

        else:
            return self._lambda_sort(metadatas)


    def sort(self):
        """
prototype::
    see = self._rsort

    action = this method sorts the attribut ``self.treeview`` regarding to the
             value of the attribut ``self._sorting``, this job being done
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


    def _rsort(self, treeview):
        """
prototype::
    see = self.buildviews , self._metadatas , self._ellipsis_sort

    arg = list(dict): treeview

    return = list(dict) ;
             the treeview sorting regarding to the value of ``self._sorting``
             (the job is done recursively)
        """
        treeview.sort(key = self._ellipsis_sort)

        for i, metadatas in enumerate(treeview):
            if 'content' in metadatas:
                metadatas['content'] = self._rsort(metadatas['content'])
                treeview[i] = metadatas

        return treeview


    def _rtree_to_list_view(self, treeview):
        """
prototype::
    see = self.sort

    arg = list(dict): treeview

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
                listview += self._rtree_to_list_view(content)

            else:
                listview.append(metadatas)

        return listview


# ------------ #
# -- OUPUTS -- #
# ------------ #

    def havetobuild(self, kind):
        """
prototype::
    return = bool ;
             ``True`` only if the output have to be remade (in that case the
             method ``self.buildviews`` is called if it is necessary)
        """
        if self._mustberebuilt:
            self.buildviews()

        return kind not in self.outputs


    def pathtoprint(self, metadatas):
        """
prototype::
    arg = dict: metadatas

    return = str ;
             the string to print for a path
        """
# << Warning ! >> The paths are whole ones by default !
        ppath = metadatas["ppath"]
        name  = ppath.name

        if name == self._ELLIPSIS \
        or self._SHORT_PATH in self._display:
            strpath = name

        elif self._REL_PATH in self._display:
            if ppath == self.ppath:
                strpath = name

            else:
                strpath = str(ppath.relative_to(self.ppath))

        else:
            strpath = str(ppath)

        return strpath


    @property
    def ascii(self):
        """
prototype::
    type = property

    return = str ;
             a basic tree using only ¨ascii characters
        """
# The job has to be done.
        if self.havetobuild('ascii'):
            text = []

            for metadatas in self.listview:
                depth = metadatas["depth"]
                tab   = self.ASCII_DECOS['tab']*depth

                decokind    = self.ASCII_DECOS[metadatas["tag"]]
                pathtoprint = self.pathtoprint(metadatas)

                text.append(
                    "{0}{1} {2}".format(tab, decokind, pathtoprint)
                )

            self.outputs['ascii'] = '\n'.join(text)

# The job has been done.
        return self.outputs['ascii']


    @property
    def tree(self):
        """
prototype::
    type = property

    see = self._rtree

    return = str ;
             a tree using special ¨unicode characters such as to draw some
             additional rules
        """
# The job has to be done.
        if self.havetobuild('tree'):
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


    def _rtree(self, treeview):
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
            isdir = 'dir' in metadatas['tag']

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
    def toc(self):
        """
prototype::
    type = property

    return = str ;
             the content only shows files and their direct parent folder like in
             a table of content where the section are always relative paths of
             parent directories and subsection are path of files
        """
# The job has to be done.
        if self.havetobuild('toc'):
            text       = []
            lastparent = ""
            tab        = self.ASCII_DECOS["tab"]
            decodir    = self.ASCII_DECOS["dir"]
            decofile   = self.ASCII_DECOS["file"]
            mainname   = self.ppath.name

            for metadatas in self.listview:
# One file
                if metadatas["tag"] == _FILE:
                    thisparent = str(
                        metadatas["ppath"].parent.relative_to(self.ppath)
                    )

                    if lastparent != thisparent:
                        dirpath \
                        = mainname / metadatas["ppath"].parent.relative_to(self.ppath)

                        text.append("")
                        text.append("{0} {1}".format(decodir, dirpath))

                        lastparent = thisparent

                    text.append(
                        "{0}{1} {2}".format(
                            tab,
                            decofile,
                            self.pathtoprint(metadatas)
                        )
                    )

# One empty directory
                elif metadatas["tag"] == "empty_dir":
                    dirpath = mainname / metadatas["ppath"].relative_to(
                        self.ppath
                    )

                    text.append("")
                    text.append("{0} {1}".format(decodir, dirpath))

# "Lines to text" transformation can be done
            self.outputs['toc'] = '\n'.join(text[1:])


# The job has been done.
        return self.outputs['toc']


    @property
    def latex(self):
        """
prototype::
    type = property

    return = str ;
             a ¨latex code for the ¨latex package latex::``dirtree``
        """
# The job has to be done.
        if self.havetobuild('latex'):
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
