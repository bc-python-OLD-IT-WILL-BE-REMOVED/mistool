#!/usr/bin/env python3

"""
prototype::
    date = 2016-03-19


This module contains mainly classes and functions producing strings useful to
be printed in a terminal.
"""

from mistool.config.frame import ALL_FRAMES
from mistool.latex_use import escape as latex_escape
from mistool.os_use import (
# Class
    PPath,
# Safe constants
    ALL_DIR_TAGS, ALL_FILE_TAGS,
    DIR_TAG, FILE_TAG,
    FILE_DIR_OTHERS_NAME,
)


# -------------------- #
# -- SAFE CONSTANTS -- #
# -------------------- #

UPLEFT    = "upleft"
UPRIGHT   = "upright"
DOWNLEFT  = "downleft"
DOWNRIGHT = "downright"

LEFT     = "left"
CENTER   = "center"
RIGHT    = "right"
UPRULE   = "up"
DOWNRULE = "down"


# ------------------ #
# -- STEP BY STEP -- #
# ------------------ #

class Step:
    """
prototype::
    arg-attr = int: start = 1 ;
               the first number used for the steps
    arg-attr = func: textit = lambda n, t: "{0}) {1}".format(n, t) ;
               the function called to make the text corresponding to one action
               using two variables two variables ``n`` for the number, and ``t``
               for the users's text
    arg-attr = bool: isprinted = True ;
               this is to ask to print the texts in the terminal
    arg-attr = bool: isreturned = False ;
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
something else than print the steps in a terminal. You can even ask to not
print anything.
Here is an example where the actions are just put in a file with the long path
path::``/Users/projetmbc/file.log`` (you can also use ``mistool.os_use`` for
the actions on files).

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

The texts for the actions are made using the argument ``textit`` which must be
a function of two variables ``n`` for the number, and ``t`` for the users's
text. Here is an ugly but assumed example.

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
ALIGNMENTS = {
    LEFT  : "<",
    CENTER: "^",
    RIGHT : ">"
}
LONG_ALIGNMENTS = {x[0]: x for x in ALIGNMENTS}

def withframe(
    text,
    frame = DEFAULT_FRAME,
    align = LEFT
):
    """
prototype::
    see = showallframes , buildframe

    arg = str: text ;
          the text to put inside a frame
    arg = {str: str}: frame = DEFAULT_FRAME ;
          this dictionary indicates how to draw the frame (you can easily add
          new frames with the help of the function ``buildframe``)
    arg = str: align = LEFT in ALIGNMENTS.keys() + LONG_ALIGNMENTS.keys() ;
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

    >>> print(withframe(text = text, align = RIGHT))
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
    align = LONG_ALIGNMENTS.get(align, align)

    if align not in ALIGNMENTS:
        raise ValueError("unknown name for the positionning of the text.")

# The lines of the text.
    lines = [x for x in text.splitlines()]
    width = max([len(x) for x in lines])

# Formatting each line of text inside the frame.
    howtoput = '{' + ':{0}{1}'.format(
        ALIGNMENTS[align],
        width
    ) + '}'

    lines = [howtoput.format(x) for x in lines]

# The frame
    frametexts = []

# First rule
    hrule = "{0}{1}{2}".format(
        frame[UPLEFT],
        frame[UPRULE]*width,
        frame[UPRIGHT]
    )

    if hrule:
        frametexts.append(hrule)

# Inside
    for oneline in lines:
        frametexts.append(
            "{0}{1}{2}".format(
                frame[LEFT],
                oneline,
                frame[RIGHT]
            )
        )

# Last rule
    hrule = "{0}{1}{2}".format(
        frame[DOWNLEFT],
        frame[DOWNRULE]*width,
        frame[DOWNRIGHT]
    )

    if hrule:
        frametexts.append(hrule)

# Here we are...
    return "\n".join([x.rstrip() for x in frametexts])


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
          this string represents a frame with its content indicated using
          ``{text}`` (see the example below)

    return = {str: str} ;
             a dictionary that can be used as the argument ``frame`` of the
             function ``withframe``


To understand how this function has to be used, let's suppose we want to define
the following so ugly frame.

code::
    @@ --------------------%%
       |-> One small   <-+
       |-> text        <-+
       |-> to do tests <-+
    &&==================== $$


To do that, you just have to use the special string ``{text}`` instead of a real
text as we have done in the following text (be careful of spaces).

code::
    @@ --------------%%
       |-> {text} <-+
    &&=============== $$


This string can be directly given to the function ``buildframe`` that will
return a dictionary to be used with the function ``withframe``. That's all !

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
        'up'     : '-',
        'upright': '----%%',
    # BETWEEN UP & DOWN
        'left' : '   |-> ',
        'right': ' <-+',
    # DOWN
        'downleft' : '&&=====',
        'down'     : '=',
        'downright': '==== $$'
    }


warning::
    Only one character can be used upon ``{text}``, and the same is true below
    ``{text}``, but you can use one character upside, and another downside as
    we have done. This restriction comes from the different width of texts that
    can be framed.
    """
# The lines used
    lines = text.splitlines()

# Do we have a good number of lines ?
    nblines = len(lines)

    if nblines == 0:
        raise ValueError("you have given an empty string")

    elif nblines > 3:
        raise ValueError("you can't use more than three lines.")

# Up, (in)side, down
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

    if inside is None:
        raise ValueError("the line with ``{text}`` is missing.")

# Near to the end...
    start = inside.find('{text}')
    end   = start + 6

    frame = {
    # UP
        UPLEFT : up[:start],
        UPRIGHT: up[end:],
    # INSIDE
        LEFT : inside[:start],
        RIGHT: inside[end:],
    # DOWN
        DOWNLEFT : down[:start],
        DOWNRIGHT: down[end:],
    }

# We have to take care os spaces !
    up_start_end = up[start:end]

    if not up_start_end:
        frame[UPRULE] = " "

    elif len(set(up_start_end)) > 1:
        raise ValueError(
            "at most one character can be used to draw "
            "the line upside the text."
        )

    else:
        frame[UPRULE] = up[start]


    down_start_end = down[start:end]

    if not down_start_end:
        frame[DOWNRULE] = " "

    elif len(set(down_start_end)) > 1:
        raise ValueError(
            "at most one character can be used to draw "
            "the line downside the text."
        )

    else:
        frame[DOWNRULE] = down[start]

    return frame


# ----------------------- #
# -- VIEWS OF A FOLDER -- #
# ----------------------- #

def mustrebuild(meth):
    """
property::
    see = DirView

    type = decorator

    arg = func: meth ;
          one method of the class ``DirView``


This decorator is used to indicate easily that the internal views used by
``DirView`` must be rebuilt.
    """
    def newmeth(self, *args, **kwargs):
        self._mustberebuilt = True

        return meth(self, *args, **kwargs)

    return newmeth


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
    arg-attr = str: display = "main short" in self.DISPLAY;
               this argument gives informations about the output to produce
               (you can just use the initials of the options)
    arg-attr = str: sorting = "alpha" in [x for x in cls.LAMBDA_SORT] or
                                      in [x for x in cls.LAMBDA_SORT_LONGNAMES];
               this argument indicates the way to sort the paths found

    clsattr = {str: (lambda, ?)}: LAMBDA_SORT ;
              this attribut of class, and not of one of its instance, defines
              different ways to sort the paths (see the end of the documentation
              above for more ¨infos)


===================================
The directory used for the examples
===================================

All of the following examples will use the same folder which has the structure
above and the absolute path path::``/Users/projetmbc/dir``.

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
paths instead of the "names". This needs to use the arguments ``display`` and
``sorting``. Here is an example where we must add the option ``"main"`` to
``display`` so as to see the main folder.

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
    All the available formattings are given later in a dedicated section of this
    documentation.


Let's see a last example using the argument ``regpath``. The following code
asks to keep only the files with the extension path::``py``. You can see that
the empty folders are not given.

pyterm::
    >>> from mistool.term_use import DirView, PPath
    >>> dir     = PPath("/Users/projetmbc/dir")
    >>> dirview = DirView(
    ...     ppath   = dir,
    ...     regpath = "file::**.py",
    ... )
    >>> print(dirview.ascii)
    + dir
        * code_1.py
        * code_2.py
        + doc
            * code_A.py
            * code_B.py


You can see other files than the ones wanted. Theuy will be indicated by
ellipsis. This feature is obtained using the ``"xtra"`` regpath query.

pyterm::
    >>> from mistool.term_use import DirView, PPath
    >>> dir     = PPath("/Users/projetmbc/dir")
    >>> dirview = DirView(
    ...     ppath   = dir,
    ...     regpath = "xtra file::**.py"
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
        * ...


info::
    The documentation of the function ``_ppath_regpath2meta`` gives all the
    ¨infos about the regpaths.


=======================
The "ruled" tree output
=======================

By default, ``dirview.tree`` give a tree view using rules similar to the ones
you can see in ¨gui applications displaying tree structure of a folder. Here we
use only ¨utf8 characters.

term::
    ╸dir 📁
     ┣━ code_1.py
     ┣━ code_2.py
     ┣━ file_1.txt
     ┣━ file_2.txt
     ┣━ doc 📁
     ┃  ┣━ code_A.py
     ┃  ┣━ code_B.py
     ┃  ┣━ slide_A.pdf
     ┃  ┣━ slide_B.pdf
     ┃  ┗━ licence 📁
     ┃     ┗━ doc.pdf
     ┗━ emptydir 📁


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
    All the paths for the folders will be always displayed as relative ones
    to the parent directory of the folder analyzed, and not to the folder
    analyzed, and all content of a folder will be inside a single "section".
    Paths formatting options apply only to files.


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

    a) ``long`` asks to display the absolute paths of the files and directories
    found.

    b) ``relative`` asks to display relative paths comparing to the main
    directory analysed.

    c) ``short`` asks to only display names of directories found, and of the
    files found with their extensions.

    d) ``main`` asks to display the main directory which is analyzed.


=======================
All the sorting options
=======================

The optional string argument ``sorting``, or the attribut with the same name
``sorting``, can be one of the following values (each name can be replaced by
its initial).

    a) ``alpha`` is the alphabetic sorting on the strings representing the
    paths. This the default value.

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
            "alpha": [
                lambda x: str(x["ppath"].name),
                'z'*500
            ],
            "name": [
                lambda x: (
                    str(x["ppath"].stem),
                    int(x['tag'] in ALL_DIR_TAGS)
                ),
                ('z'*500, 0)
            ],
            "filefirst": [
                lambda x: (
                    int(x['tag'] in ALL_DIR_TAGS),
                    str(x["ppath"])
                ),
                (0, 'z'*500)
            ],
            "date": [
                lambda x: -x["ppath"].stat().st_mtime,
                float('inf')
            ],
        }


     This dictionary uses the following conventions.

        1) The keys are the names of the sortings given in the form of strings.

        2) The values are lists of two elements.

            a) The first element is a lambda function that will give the values
            used for sorting where ``x`` is a dictionary stored in
            ``self.listview`` (see the technical documentation of the method
            ``DirView.build``).

            b) The second element is the special value used for sorting existing
            files that don't validate the "regpath" pattern.
    """

# Safe constants
    CONTENT_TAG = "content"
    DEPTH_TAG   = "depth"
    PPATH_TAG   = "ppath"
    TAG_TAG     = "tag"

    ASCII_TAG = "ascii"
    LATEX_TAG = "latex"
    TOC_TAG   = "toc"
    TREE_TAG  = "tree"

    DOT_TAG   = "dot"
    HRULE_TAG = "hrule"
    VRULE_TAG = "vrule"
    FNODE_TAG = "fnode"
    LNODE_TAG = "lnode"
    VNODE_TAG = "vnode"

    TAB_TAG = 'tab'

# Trees
    ASCII_DECOS = {
        k: v
        for v, keys in {
            "+"  : ALL_DIR_TAGS,
            "*"  : ALL_FILE_TAGS,
            " "*4: [TAB_TAG],
        }.items()
        for k in keys
    }

# Source for the rules:
#     * http://en.wikipedia.org/wiki/Box-drawing_character#Unicode
#     * http://en.wikipedia.org/wiki/Box-drawing_character#Unicode

    UTF8_DECOS = {
# Initial
        DOT_TAG: "\u2578",          # --->  ╸
# Horizontal and vertical rules
        HRULE_TAG: "\u2501",        # --->  ━
        VRULE_TAG: "\u2503",        # --->  ┃
# First, vertical and horizontal nodes
        FNODE_TAG: "\u250F",        # --->  ┏
        VNODE_TAG: "\u2523",        # --->  ┣
        LNODE_TAG: "\u2517",        # --->  ┗
# Decorations
        DIR_TAG : "\U0001F4C1",     # --->  📁
        FILE_TAG: "",
    }

    LAMBDA_SORT = {
        "alpha": [
            lambda x: str(x["ppath"].name),
            'z'*500
        ],
        "name": [
            lambda x: (
                str(x["ppath"].stem),
                int(x['tag'] in ALL_DIR_TAGS)
            ),
            ('z'*500, 0)
        ],
        "filefirst": [
            lambda x: (
                int(x['tag'] in ALL_DIR_TAGS),
                str(x["ppath"])
            ),
            (0, 'z'*500)
        ],
        "date": [
            lambda x: -x["ppath"].stat().st_mtime,
            float('inf')
        ],
    }

    LAMBDA_SORT_LONGNAMES = {x[0]: x for x in LAMBDA_SORT}

# Additional paths
    MAIN_PATH = "main"

# Formattings of the paths
    PATH_FORMATS = LONG_PATH, REL_PATH, SHORT_PATH = "long", "relative", "short"

    PATH_FORMATS = set(PATH_FORMATS)

# All formats
    DISPLAY = set(PATH_FORMATS)
    DISPLAY.add(MAIN_PATH)

    DISPLAY_LONGNAMES = {x[0]: x for x in DISPLAY}

    def __init__(
        self,
        ppath,
        regpath = "**",
        display = "main short",
        sorting = "alpha"
    ):
# General settings
        self._mustberebuilt = True

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
    @mustrebuild
    def ppath(self, value):
# Do we have a folder ?
        if not value.is_dir():
            raise NotADirectoryError("``ppath`` doesn't point to a directory.")

        self._ppath = value

    @property
    def regpath(self):
        return self._regpath

    @regpath.setter
    @mustrebuild
    def regpath(self, value):
        self._regpath = value

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, value):
        self._display = set(
            self.DISPLAY_LONGNAMES.get(x.strip(), x.strip())
            for x in value.split(" ")
            if x.strip()
        )

        if not self._display <= self.DISPLAY:
            raise ValueError("illegal formatting rule (see ``display``).")

        nb_path_formats = len(self._display & self.PATH_FORMATS)

        if nb_path_formats == 0:
            self._display.add(self.SHORT_PATH)

        elif nb_path_formats != 1:
            raise ValueError(
                "several path formatting rules (see ``display``)."
            )

        self._mustberebuilt = True

    @property
    def sorting(self):
        return self._sorting

    @sorting.setter
    @mustrebuild
    def sorting(self, value):
        self._sorting = self.LAMBDA_SORT_LONGNAMES.get(value, value)

        if self._sorting not in self.LAMBDA_SORT:
            raise ValueError("unknown sorting rule.")

# -------------------- #
# -- INTERNAL VIEWS -- #
# -------------------- #

    def buildviews(self):
        """
prototype::
    see = self.sort , self.ascii , self.latex , self.toc , self.tree

    action = this method builds one flat list ``self.listview`` of dictionaries,
             that store all the informations about the directories and the
             folders matching the regpath.
             This method also builds ``self.treeview`` another list of
             dictionaries which is like the natural tree structure of the folder
             analyzed (both of this objects are sorted regarding to the value of
             the attribut ``self.sorting``)


======================================
Dictionaries used in ``self.listview``
======================================

warning::
    You must know the structure of the attribut ``listview`` if you want to
    define your own kind of sorting for the outputs.


``self.listview`` is a list of dictionaries that respects the structure of the
folder analyzed, the files being placed before the folders. The dictionaries
have the keys and values explained below.

    1) The key ``'tag'`` can have the values FILE_TAG,  FILE_OTHERS_TAG,
    DIR_TAG and DIR_OTHERS_TAG.

    2) The key ``'depth'`` is simply a relative depth regarding to the folder
    analyzed.

    3) The last key ``'ppath'`` is simply the absolute path of one directory
    or file found.


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
        self._build_treeview()
        self._build_listview()
        self.sort()
        self._mustberebuilt = False

    def _build_treeview(self):
        """
prototype::
    see = self.buildviews , self._rbuild_treeview

    action = this method returns the attribut ``self.treeview`` (most of the
             job is done recursively by the method ``self._rbuild_treeview``)
        """
        walkview   = []
        extradepth = 0
        dirs_found = []

# Main folder or not ?
        if self.MAIN_PATH in self._display:
            walkview.append({
                self.TAG_TAG  : DIR_TAG,
                self.DEPTH_TAG: 0,
                self.PPATH_TAG: self.ppath
            })

            extradepth += 1

            dirs_found.append(PPath("."))

# We have to take care of the parent folders of the matching files and folders.
        for ppath in self.ppath.walk(self.regpath):
            relppath = ppath.relative_to(self.ppath)

            for rel_onepar in relppath.parents:
                if rel_onepar in dirs_found:
                    break

                else:
                    onepar = self.ppath / rel_onepar

                    walkview.append({
                        self.TAG_TAG  : DIR_TAG,
                        self.DEPTH_TAG: ppath.depth_in(onepar) + extradepth,
                        self.PPATH_TAG: onepar
                    })

                    dirs_found.append(rel_onepar)

            if ppath._tag in ALL_DIR_TAGS:
                dirs_found.append(ppath.relative_to(self.ppath))

            walkview.append({
                self.TAG_TAG  : ppath._tag,
                self.DEPTH_TAG: ppath.depth_in(self.ppath) + extradepth,
                self.PPATH_TAG: ppath
            })

        walkview.sort(key = lambda x: str([x[self.PPATH_TAG]]))

# Let's work recursively.
        self.treeview = self._rbuild_treeview(walkview)

    def _rbuild_treeview(self, walkview, depth = 0):
        """
prototype::
    action = the attribut ``self.treeview`` is build recursively
        """
        treeview = []

        i    = 0
        imax = len(walkview)

        while(i < imax):
            metadatas = walkview[i]

# Simply a file.
            if metadatas[self.TAG_TAG] in ALL_FILE_TAGS:
                treeview.append(metadatas)
                i += 1

# For a directory, we have to catch its content that will be analyzed
# recursively.
            else:
                depth   = metadatas[self.DEPTH_TAG]
                content = []
                i += 1

                while(i < imax):
                    submetadatas = walkview[i]
                    subdepth     = submetadatas[self.DEPTH_TAG]

                    if subdepth > depth:
                        content.append(submetadatas)
                        i += 1

                    else:
                        break

                if content:
                    metadatas[self.CONTENT_TAG] = self._rbuild_treeview(content)

                else:
                    metadatas[self.CONTENT_TAG] = []

                treeview.append(metadatas)

        return treeview

    def _build_listview(self):
        """
prototype::
    see = self.buildviews , self._build_treeview

    action = this method returns the attribut ``self.listview`` (all the
             job is done recursively by the method ``self._rbuild_listview``)
        """
        self.listview = self._rbuild_listview(self.treeview)

    def _rbuild_listview(self, treeview):
        """
prototype::
    arg = list(dict): treeview

    return = list(dict) ;
             the listview associated to ``self.treeview`` (the job is done
             recursively)
        """
        listview = []

        for metadatas in treeview:
            if self.CONTENT_TAG in metadatas:
                content = metadatas[self.CONTENT_TAG]

# << Warning ! >> We can't use ``del metadatas['content']`` because this will
# always change self.treeview (we could have used a deepcopy but this  would
# be not efficient).
                newmetadatas = {}

                for k, v in metadatas.items():
                    if k != self.CONTENT_TAG:
                        newmetadatas[k] = v

                listview.append(newmetadatas)
                listview += self._rbuild_listview(content)

            else:
                listview.append(metadatas)

        return listview

# ------------- #
# -- SORTING -- #
# ------------- #

    def _sort_all(self, metadatas):
        """
prototype::
    see = self.buildviews , self._metadatas

    arg = dict: metadatas

    return = str ;
             the value to use for the sorting
        """
        if metadatas[self.PPATH_TAG].name == FILE_DIR_OTHERS_NAME:
            return self.ELLIPSIS_sort_value

        else:
            return self._lambda_sort(metadatas)

    def sort(self):
        """
prototype::
    see = self._rsort

    action = this method sorts the attribut ``self.treeview`` regarding to the
             value of the attribut ``self._sorting``


info::
    The job is done recursively by the method ``self._rsort``, and then the list
    ``self.listview`` is rebuild using the new ``self.treeview`` (this is uggly
    but this allows to define naturlly the methods of sorting, and this is also
    easier to code).
        """
        self._lambda_sort, self.ELLIPSIS_sort_value \
        = self.LAMBDA_SORT[self.sorting]

# Each new sorting
        self.outputs = {}

# We sort first the treeview (that allows to define natural sortings).
        self.treeview = self._rsort(self.treeview)

# We have to go back to ``self.listview`` !
        self.listview = self._rbuild_listview(self.treeview)

    def _rsort(self, treeview):
        """
prototype::
    see = self.buildviews , self._metadatas , self.ELLIPSIS_sort

    arg = list(dict): treeview

    return = list(dict) ;
             the treeview sorting regarding to the value of ``self._sorting``
             (the job is done recursively)
        """
        treeview.sort(key = self._sort_all)

        for i, metadatas in enumerate(treeview):
            if self.CONTENT_TAG in metadatas:
                metadatas[self.CONTENT_TAG] \
                = self._rsort(metadatas[self.CONTENT_TAG])

                treeview[i] = metadatas

        return treeview

# ------------- #
# -- OUTPUTS -- #
# ------------- #

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
        ppath = metadatas[self.PPATH_TAG]
        name  = ppath.name

        if name == FILE_DIR_OTHERS_NAME \
        or self.SHORT_PATH in self._display:
            strpath = name

        elif self.REL_PATH in self._display:
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
        if self.havetobuild(self.ASCII_TAG):
            text = []

            for metadatas in self.listview:
                depth = metadatas[self.DEPTH_TAG]
                tab   = self.ASCII_DECOS[self.TAB_TAG]*depth

                decokind    = self.ASCII_DECOS[metadatas[self.TAG_TAG]]
                pathtoprint = self.pathtoprint(metadatas)

                text.append(
                    "{0}{1} {2}".format(tab, decokind, pathtoprint)
                )

            self.outputs[self.ASCII_TAG] = '\n'.join(text)

# The job has been done.
        return self.outputs[self.ASCII_TAG]

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
        if self.havetobuild(self.TREE_TAG):
# Ugly patch !!!
            for i, x in enumerate(self._rtree(self.treeview)):
                if i == 0:
                    self.outputs[self.TREE_TAG] \
                    = self.UTF8_DECOS[self.DOT_TAG] + x[3:]

                else:
                    self.outputs[self.TREE_TAG] += "\n " + x[3:]

# The job has been done.
        return self.outputs[self.TREE_TAG]

    def _rtree(self, treeview):
        """
prototype::
    return = str ;
             the lines of the tree that uses ¨unicode characters to draw some
             additional rules
        """
        lines       = []
        imax        = len(treeview) - 1
        thisdepth   = treeview[0][self.DEPTH_TAG]

        if thisdepth <= 3:
            subtabdepth = 0

        else:
            subtabdepth = thisdepth - 2

        for i, metadatas in enumerate(treeview):
# Rule regarding the kind of object.
            isdir = DIR_TAG in metadatas[self.TAG_TAG]

# Rule before any kind of rule.
            if thisdepth == 0:
                addvrule = False
# Ugly patch !!!
                before   = " "

            elif i == imax:
                addvrule = False
                before   = self.UTF8_DECOS[self.LNODE_TAG]

            else:
                addvrule = True
                before   = self.UTF8_DECOS[self.VNODE_TAG]

# Deco after.
            if metadatas["tag"] in ALL_DIR_TAGS:
                after = self.UTF8_DECOS[DIR_TAG]

            else:
                after = self.UTF8_DECOS[FILE_TAG]

# Just add the object.
            lines.append(
                "{0}{1} {2} {3}".format(
                    before,
                    self.UTF8_DECOS[self.HRULE_TAG],
                    self.pathtoprint(metadatas),
                    after
                )
            )

# A new not empty directory
            if isdir and metadatas[self.CONTENT_TAG]:
                subbefore = " "*subtabdepth

                if addvrule:
                    subbefore += self.UTF8_DECOS[self.VRULE_TAG] + "  "

                else:
                    subbefore += "   "

                lines += [
                    subbefore + x
                    for x in self._rtree(metadatas[self.CONTENT_TAG])
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
        if self.havetobuild(self.TOC_TAG):
            text       = []
            lastparent = ""
            tab        = self.ASCII_DECOS[self.TAB_TAG]
            decodir    = self.ASCII_DECOS[DIR_TAG]
            decofile   = self.ASCII_DECOS[FILE_TAG]
            mainname   = self.ppath.name

# Always files first here !
            _usersort_   = self.sorting
            self.sorting = "filefirst"
            self.sort()

            self.sorting = _usersort_
            self._mustberebuilt = True

# Let's go !
            for metadatas in self.listview:
# One directory
                if metadatas[self.TAG_TAG] in ALL_DIR_TAGS:
                    dirpath = mainname / metadatas[self.PPATH_TAG].relative_to(
                        self.ppath
                    )

                    text.append("")
                    text.append("{0} {1}".format(decodir, dirpath))

                    lastparent = str(
                        metadatas[self.PPATH_TAG].relative_to(self.ppath)
                    )

# One file
                else:
                    thisparent = str(
                        metadatas[self.PPATH_TAG].parent.relative_to(self.ppath)
                    )

                    if lastparent != thisparent:
                        dirpath = mainname / metadatas[
                            self.PPATH_TAG
                        ].parent.relative_to(self.ppath)

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


# "Lines to text" transformation can be done
            self.outputs[self.TOC_TAG] = '\n'.join(text[1:])


# The job has been done.
        return self.outputs[self.TOC_TAG]

    @property
    def latex(self):
        """
prototype::
    type = property

    return = str ;
             a ¨latex code for the ¨latex package latex::``dirtree``
        """
# The job has to be done.
        if self.havetobuild(self.LATEX_TAG):
            text = []

            for metadatas in self.listview:
                depth = metadatas[self.DEPTH_TAG] + 1
                pathtoprint = latex_escape(self.pathtoprint(metadatas))

                text.append(
                    "{0}.{1} <{2}>.".format(
                        "  "* depth,
                        depth,
                        pathtoprint
                    )
                )

            text = "\dirtree<%\n{0}\n>".format('\n'.join(text))

            self.outputs[self.LATEX_TAG] \
            = text.replace('<', '{').replace('>', '}')

# The job has been done.
        return self.outputs[self.LATEX_TAG]
