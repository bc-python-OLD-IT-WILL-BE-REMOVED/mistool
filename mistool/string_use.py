#!/usr/bin/env python3

"""
prototype::
    date = 2015-06-07


This module contains some tools to manipulate strings.
"""

from unicodedata import name as ucname

from mistool.config.ascii import ASCII_CHARS
from mistool.config.pattern import PATTERNS_WORDS


# --------------------- #
# -- CASE FORMATTING -- #
# --------------------- #

_CASE_VARIANTS      = ['firstlast', 'lower', 'sentence', 'title', 'upper']
_LONG_CASE_VARIANTS = {x[0]:x for x in _CASE_VARIANTS}

def case(text, kind):
    """
prototype::
    arg    = str: text ;
             the text to modify
    arg    = str: kind in _CASE_VARIANTS or in _LONG_CASE_VARIANTS ;
             the kind of case you want
    return = str ;
             the text modified.


Here are all the different kinds of case you can apply to one text.

pyterm::
    >>> from mistool.string_use import case
    >>> text = "onE eXamPLe"
    >>> for kind in ['lower', 'upper', 'sentence', 'title', 'firstlast']:
    ...     print(case(text, kind),"  [{0}]".format(kind))
    ...
    one example   [lower]
    ONE EXAMPLE   [upper]
    One example   [sentence]
    One Example   [title]
    One examplE   [firstlast]


info::
    You can use only the first letter of a kind instead of its whole name.


info::
    The weird transformation ``case("onE eXamPLe", "firstlast")`` is useful for
    ¨pyba another project of the author of the package ¨mistool.
    """
# Good kind ?
    kind = _LONG_CASE_VARIANTS.get(kind, kind)

    if kind not in _CASE_VARIANTS:
        raise ValueError('unknown kind of case formatting.')

# Let's work...
    if kind == 'lower':
        return text.lower()

    elif kind == 'upper':
        return text.upper()

    elif kind == 'sentence':
        return text[0].upper() + text[1:].lower()

    elif kind == 'title':
        return text.title()

    elif kind == 'firstlast':
        return text[0].upper() + text[1:-1].lower() + text[-1].upper()


def camelto(
    text,
    kind,
    sep = "_"
):
    """
prototype::
    arg    = str: text ;
             the text to modify that uses the camel case (so it can't contain
             spaces)
    arg    = str: kind in _CASE_VARIANTS or in _LONG_CASE_VARIANTS ;
             the kind of case you want
    return = str ;
             the text modified after adding underscores with one space before each upper leters, except the starting one, and then applying the case using ``kind`` so as to finally remove all spaces.


The code below shows all the possibilities available with the default separator
``_``.

pyterm::
    >>> from mistool.string_use import camelto
    >>> text = "OneSmallExampLE"
    >>> for kind in ['lower', 'upper', 'sentence', 'title', 'firstlast']:
    ...     print(camelto(text, kind),"  [{0}]".format(kind))
    ...
    one_small_examp_l_e   [lower]
    ONE_SMALL_EXAMP_L_E   [upper]
    One_small_examp_l_e   [sentence]
    One_Small_Examp_L_E   [title]
    One_small_examp_l_E   [firstlast]


If you want to use another separator than ``_``, just use the argument ``sep`` as below.

pyterm::
    >>> from mistool.string_use import camelto
    >>> text = "OneSmallExampLE"
    >>> sep  = " "
    >>> kind = "title"
    >>> print(camelto(text, kind, sep))
    ...
    One Small Examp L E
    """
# An empty text
    if not text:
        return text

# The text is not empty
    if " " in text:
        raise ValueError("the text can't contain spaces.")

    sepplus = sep + " "
    answer = text[0]

    for onechar in text[1:]:
        if onechar.isupper():
            answer += sepplus

        answer += onechar

    answer = case(answer, kind)

    return answer.replace(sepplus, sep)


# ------------------ #
# -- CASE TESTING -- #
# ------------------ #

def iscase(text, kind):
    """
prototype::
    arg    = str: text ;
             the text to test
    arg    = str: kind in _CASE_VARIANTS or in _LONG_CASE_VARIANTS ;
             the kind of case you want to test
    return = bool ;
             the boolean value of the test ``text == case(text, kind)``
    """
# Good kind ?
    kind = _LONG_CASE_VARIANTS.get(kind, kind)

    if kind not in _CASE_VARIANTS:
        raise ValueError('unknown kind of case for testing.')

# Let's work...
    if kind == "lower":
        return text.islower()

    elif kind == "upper":
        return text.isupper()

    else:
        return text == case(text, kind)


# ------------- #
# -- REPLACE -- #
# ------------- #

class MultiReplace():
    """
prototype::
    arg-attr = {str: str}: oldnew = {} ;
               this dictionary uses couples ``(key, value)`` that are of the
               kind ``(old text to find, new text for replacement)`` where the
               replacements can eventually contain also texts to be replaced
    arg-attr = str: mode = "norecu" in cls._MODES or in cls._LONG_MODES ;
               the default value asks to not do replacements recursively in the
               new texts used for replacements contrary to ``mode = "recu"``,
               this second mode needing to use also the argument ``pattern``
               (you can use ``"n"`` and ``"r"`` instead of ``"norecu"`` and
               ``"recu"``)
    arg-attr = regex: pattern = None ;
               ``pattern = None`` simply asks to do replacements everywhere it
               is possible, as the method ``replace`` does with strings, but if
               you give a "grouping" pattern regex::``(...)`` defining what a
               word is, then the replacemnts will only concern this words.

    action = after defining an instance of this class, you can use your instance
             as a "superpower" replacing function


========================
Unrecursive replacements
========================

By default we have ``mode = "norecu"`` which allows to do replacements
sequentially, the old texts being replaced from the longest to
the shortest ones, and for old texts of same length, the alphabetic order will
be used. Here is an example.

pyterm::
    >>> from mistool.string_use import MultiReplace
    >>> oldnew = {
    ...     'one'  : "1",
    ...     'two'  : "2",
    ...     'three': "3"
    ... }
    >>> mreplace = MultiReplace(oldnew)
    >>> text = "one, two, three..."
    >>> print(mreplace(text))
    1, 2, 3...


======================
Recursive replacements
======================

Used with ``mode = "recu"``, an instance of the class ``MultiReplace`` allows
to use replacement texts that also contains also texts to be replaced like in the
following example.

pyterm::
    >>> from mistool.string_use import MultiReplace
    >>> from mistool.config.pattern import PATTERNS_WORDS
    >>> oldnew = {
    ...     'W1': "Word #1",
    ...     'W2': "Word #2",
    ...     'W3': "W1 and W2"
    ... }
    >>> mreplace = MultiReplace(
    ...     oldnew  = oldnew,
    ...     mode    = "recu",
    ...     pattern = PATTERNS_WORDS['var']
    ... )
    >>> print(mreplace("W1 and W2 = W3"))
    Word #1 and Word #2 = Word #1 and Word #2


The only technical thing here is the use of ``PATTERNS_WORDS["var"]`` which is
a regex grouping pattern indicated that words starts with an ¨ascii letters
followed by ¨ascii letters, digits and underscores eventually.
Here is the definition of ``PATTERNS_WORDS`` (later there is a section showing
how to use an homemade kind of words).

python::
    FR_ACCENTUED_LETTERS = "âàéèêëîïôùüç"

    PATTERNS_WORDS = {
    # Natural language
        'en': re.compile("([a-zA-Z]+)"),
        'fr': re.compile(
            "([a-z{0}A-Z{1}]+)".format(
                FR_ACCENTUED_LETTERS,
                FR_ACCENTUED_LETTERS.upper()
            )
        ),
    # Coding
        'var': re.compile("([a-zA-Z][\d_a-zA-Z]*)"),
    }


info::
    We don't obtain the same result if we use ``mode = "norecu"`` as you can see
    in the following lines where no replacements have been done in the new text
    ``"W1 and W2"`` associated to the old one ``"W3"``. Be also careful about
    the fact that we only update the attribut ``mode``.

    ...pyterm::
        >>> mreplace.mode = "norecu"
        >>> print(mreplace("W1 and W2 = W3"))
        Word #1 and Word #2 = W1 and W2


info::
    Before doing the replacements in a text, the class first builds a dictionary
    ``self.asit`` for which the replacement texts have been changed so as to not
    contain texts to be replaced. The code below shows that the attribut
    ``asit`` depends, logically, to the method used for the replacements.

    pyterm::
        >>> from mistool.string_use import MultiReplace
        >>> from mistool.config.pattern import PATTERNS_WORDS
        >>> oldnew = {
        ...     'W1': "Word #1",
        ...     'W2': "Word #2",
        ...     'W3': "W1 and W2"
        ... }
        >>> mreplace = MultiReplace(oldnew)
        >>> print(mreplace.asit)
        {
            'W1': 'Word #1',
            'W2': 'Word #2',
            'W3': 'W1 and W2'
        }
        >>> mreplace.mode    = "recu"
        >>> mreplace.pattern = PATTERNS_WORDS['var']
        >>> print(mreplace.asit)
        {
            'W1': 'Word #1',
            'W2': 'Word #2',
            'W3': 'Word #1 and Word #2'
        }


===================
Cyclic replacements
===================

In the following code, there are cyclic replacements that is why the class is
complaining if ``mode = "recu"``.

pyterm::
    >>> from mistool.string_use import MultiReplace
    >>> from mistool.config.pattern import PATTERNS_WORDS
    >>> oldnew = {
    ...     'WRONG_1': "one small text and  WRONG_2",
    ...     'WRONG_2': "one small text, and then WRONG_3",
    ...     'WRONG_3': "with WRONG_1, there is one problem here"
    ... }
    >>> mreplace = MultiReplace(
    ...     oldnew  = oldnew,
    ...     mode    = "recu",
    ...     pattern = PATTERNS_WORDS["var"]
    ... )
    Traceback (most recent call last):
    [...]
    ValueError: the following viscious circle has been found.
    	 +  --> WRONG_2 --> WRONG_3 --> WRONG_1 --> WRONG_2


================================
How to define new kinds of words
================================

Let's finish with an example showing how to define words that must starts with
``@`` followed by at least one ¨ascii letter (we have to use regexes).

pyterm::
    >>> import re
    >>> from mistool.string_use import MultiReplace
    >>> oldnew = {
    ...     '@html': '"Hypertext Markup Language"',
    ...     '@rest': '"REpresentational State Transfer"'
    ... }
    >>> mreplace = MultiReplace(
    ...     oldnew  = oldnew,
    ...     pattern = re.compile("(@[a-z]+)")
    ... )
    >>> text = "@rest is a technology used to produce @html website."
    >>> print(mreplace(text))
    "REpresentational State Transfer" is a technology used to produce "Hypertext Markup Language" website.
    """
    _MODES      = ["recu", "norecu"]
    _LONG_MODES = {x[0]: x for x in _MODES}

    def __init__(
        self,
        oldnew  = {},
        mode    = "norecu",
        pattern = None
    ):
# User's arguments
        self.oldnew  = oldnew
        self.mode    = mode
        self.pattern = pattern

# Update the value of ``self.asit``
        self._updateit = True


# --------------------- #
# -- SPECIAL SETTERS -- #
# --------------------- #

    @property
    def oldnew(self):
        return self._oldnew

    @oldnew.setter
    def oldnew(self, value):
        self._updateit = True
        self._oldnew   = value


    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._updateit = True
        self._pattern  = value


    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._updateit = True

        value = self._LONG_MODES.get(value, value)

        if value not in self._MODES:
            raise ValueError("unknown mode.")

        self._mode = value

# ---------------------------- #
# -- BUILDINS ``self.asit`` -- #
# ---------------------------- #

    def _lookforcycle(self):
        """
prototype::
    see    = self._noviciouscycle
    action = this method verifies that there are no cyclic replacements (all the
             job is done recursively by ``self._noviciouscycle``).
        """
# Nothing to do...
        if self.mode == "norecu":
            return None

# Building the crossing replacements.
        self._allold = list(self.oldnew.keys())
        self._inold  = {}

        for old, new in self.oldnew.items():
            self._inold[old] = [
                x for x in self.pattern.findall(new)
                if x in self._allold
            ]

        self._noviciouscycle(self._allold)


    def _noviciouscycle(
        self,
        nextwords,
        wordsfound = [],
    ):
        """
prototype::
    arg    = list(str): nextwords ;
             the old words with replacement texts to analyze
    arg    = list(str): wordsfound ;
             the words found in replacement texts (here we start for one word,
             then we go in its replacement and so on...)
    action = this method looks for cyclic replacements (the job is done
             recursively).
        """
        for old in nextwords:
            thisoldinnew = self._inold[old]

            if old in thisoldinnew:
                raise ValueError(
                    "<< {0} >> is used in its replacement text.".format(old)
                )

            elif old in wordsfound:
                pos = wordsfound.index(old)

                wordsfound = [""] + wordsfound[pos:]
                wordsfound.append(old)

                raise ValueError(
                    "the following viscious circle has been found.\n\t + " \
                    + " --> ".join(wordsfound)
                )

            else:
                for new in thisoldinnew:
                    self._noviciouscycle(
                        wordsfound = wordsfound + [old],
                        nextwords  = self._inold[old]
                    )


    def _build_asit(self):
        """
prototype::
    action = this method builds the direct replacements dictionary ``self.asit``
             (all the job is done by ``self._replace_in_new`` if ``self.mode =
             "norecu"``)
        """
        if self.mode == "norecu":
            self.asit = self.oldnew

        else:
            self.asit = {}

            for old, new in self.oldnew.items():
                self.asit[old] = self._replace_in_new(new)


    def _replace_in_new(self, text):
        """
prototype::
    action = this method builds the direct replacements dictionary ``self.asit``
             (all the job is done by ``self._replace_in_new`` if ``self.mode =
             "norecu"``)
        """
# Nothing ot do.
        if not text:
            return text

# The text is not empty.
        newtext = ""

        while True:
# Source :
#    http://www.developpez.net/forums/d958712/autres-langages/python-zope/general-python/amelioration-split-evolue/#post5383767
            newtext = self.pattern.sub(self._apply_in_new_for_asit, text)

            if newtext == text:
                return text

            else:
                text = newtext


    def _apply_in_new_for_asit(self, match):
        """
prototype::
    action = this method is used to do the replacements for the values of
             ``self.asit`` regarding the words defined by ``self.pattern``.
        """
        return self.oldnew.get(match.group(1), match.group(0))


# ----------------------- #
# -- REPLACE IN A TEXT -- #
# ----------------------- #

    def __call__(self, text):
        """
prototype::
    arg    = str: text ;
             a text where to do replacements
    return = str ;
             the text where all the replacements have been done.
        """
        if self._updateit:
            if not self.pattern and self.mode == "recu":
                raise ValueError(
                    'the mode "recu" must be used with a regex pattern.'
                )

            self._lookforcycle()
            self._build_asit()

            self._updateit = False

        if self.mode == "recu":
            text = self.pattern.sub(self._apply_asit, text)

        else:
            sortedkeys = sorted(
                self.oldnew.keys(),
                key = lambda t: (-len(t), t)
            )

            for old in sortedkeys:
                text = text.replace(old, self.oldnew[old])

        return text


    def _apply_asit(self, match):
        """
prototype::
    action = this method is used to do the replacements in the user's text
             regarding the words defined by ``self.pattern``.
        """
        return self.asit.get(match.group(1), match.group(0))


# ----------- #
# -- SPLIT -- #
# ----------- #

class SplitInfos:
    """
prototype::
    see    = MultiSplit
    action = this class is simply an object used by the method ``__iter__`` of
             the class ``MultiSplit``.
    """

    def __init__(
        self,
        type,
        val
    ):
        self.type = type
        self.val  = val


class MultiSplit():
    """
prototype::
    arg-attr = str , list(str): seps ;
               this argument can be either a string for a single separator, or a
               list of strings for different level of separators
    arg-attr = str: esc_char = "" ;
               this string indicated an escaping sequence for the separators.
               By default, ``escape = ""`` indicates that there is no escaping
               feature.
    arg-attr = bool: strip = False ;
               this boolean variable indicates to strip, or not, each pieces of
               text found.

    action = after defining an instance of this class, you can use your instance
             as a "superpower" spliting function


================================
Split a text at different levels
================================

The purpose of this class is to split a text at different levels. You can use
either a list view version of the splitted text, or work with a special iterator
as we will see at the end of this documentation.
Here is an example of the "listview" version. As you can see one separator give
a 1-depth list, two separators give a 2-depth list and so on...

pyterm::
    >>> from mistool.string_use import MultiSplit
    >>> msplit = MultiSplit(seps = "|")
    >>> print(msplit("p_1 ; p_2 ; p_3 | r_1 ; r_2 | s"))
    [
        'p_1 ; p_2 ; p_3 ',
        ' r_1 ; r_2 ', ' s'
    ]
    >>> msplit.seps = ["|", ";"]
    >>> print(msplit("p_1 ; p_2 ; p_3 | r_1 ; r_2 | s"))
    [
        ['p_1 ', ' p_2 ', ' p_3 '],
        [' r_1 ', ' r_2 '], [' s']
    ]


================
Strip the pieces
================

If you don't care about leading and ending spaces of each pieces found, just use
``strip = True``.

python::
    >>> from mistool.string_use import MultiSplit
    >>> msplit = MultiSplit(
    ...     seps  = ["|", ";"],
    ...     strip = True
    ... )
    >>> print(msplit("p_1 ; p_2 ; p_3 | r_1 ; r_2 | s"))
    [
        ['p_1', 'p_2', 'p_3'],
        ['r_1', 'r_2'],
        ['s']
    ]


===================
Escaping separators
===================

Using the argument or attribut ``esc_char``, you can indicate an escaping
sequence of characters like in the example below.

python::
    >>> from mistool.string_use import MultiSplit
    >>> msplit = MultiSplit(
    ...     seps  = ["|", ";"],
    ...     strip = True
    ... )
    >>> print(msplit("p_1 ; p_2 \; p_3 | r_1 ; r_2 | s"))
    [
        ['p_1', 'p_2 \\', 'p_3'],   # Three elements
        ['r_1', 'r_2'],
        ['s']
    ]
    >>> msplit.esc_char = "\\"
    >>> print(msplit("p_1 ; p_2 \; p_3 | r_1 ; r_2 | s"))
    [
        ['p_1', 'p_2 \\; p_3'],     # Just two elements
        ['r_1', 'r_2'],
        ['s']
    ]


========================
A user friendly iterator
========================

``MultiSplit`` has a method ``iter`` which gives an easy way to walk in the
splitted text.

pyterm::
    >>> from mistool.string_use import MultiSplit
    >>> msplit = MultiSplit(
    ...     seps  = ["|", ";", ","],
    ...     strip = True
    ... )
    >>> listview = msplit("p_1 , p_2 ; p_3 | r_1 ; r_2 | s")
    >>> for infos in msplit.iterate():
    ...     print("{0} ---> {1}".format(infos.type, infos.val))
    ...
    sep ---> |
    sep ---> ;
    sep ---> ,
    val ---> p_1
    val ---> p_2
    sep ---> ;
    sep ---> ,
    val ---> p_3
    sep ---> |
    sep ---> ;
    sep ---> ,
    val ---> r_1
    sep ---> ;
    sep ---> ,
    val ---> r_2
    sep ---> |
    sep ---> ;
    sep ---> ,
    val ---> s


If you read the output, you can interpret it like this :

    1) First we know that things separated by ``|`` are coming.

    2) Then there are things separated by `;`, and after others separated by
    ``,``.

    2) This last things are the values ``p_1`` and ``p_2``.

    3) After we have things separated first by `;`, and secondly by ``,``, this
    last ones being just one value ``p_3``, and so on...


warning::
    We have used ``msplit.iterate()`` so as to walk in the last list view built
    by ``msplit``.
    If you need to use another view stored in a variable ``anotherview`` for
    example, you can use ``for infos in msplit.iterate(anotherview):...``.
    """

    def __init__(
        self,
        seps,
        esc_char = "",
        strip    = False
    ):
# User's arguments
        self.seps     = seps
        self.esc_char = esc_char
        self.strip    = strip


# --------------------- #
# -- SPECIAL SETTERS -- #
# --------------------- #

    @property
    def seps(self):
        return self._seps

    @seps.setter
    def seps(self, value):
        if not value:
            raise ValueError(
                "the variable << seps >> can't be an \"empty\" object."
            )

        elif isinstance(value, str):
            value = [value]

        else:
            if not isinstance(value, list):
                raise TypeError(
                    "the variable << seps >> must be a string "
                    "or list of strings."
                )

            for sep in value:
                if not isinstance(sep, str):
                    raise TypeError(
                        "the variable << seps >> must be a string "
                        "or list of strings."
                    )

        self._seps = value


# -------------- #
# -- LISTVIEW -- #
# -------------- #

    def __call__(self, text):
        """
prototype::
    see    = self._build
    arg    = str: text ;
             a text to be splitted.
    return = listview ;
             this method builds a list view version of the splitted text that is
             a list of lists of lists of ... of lists of strings. The depth of
             the list is equal to the number of separators
             (indeed, all the job is done recursively by ``self._build``).
        """
        self.listview = self._build(
            text = text,
            seps = self.seps
        )

        return self.listview


    def _build(self, text, seps):
        """
prototype::
    arg    = str: text ;
             a text to be splitted.
    arg    = list(str): seps ;
             a list of separators (not necessary the user's list).
    return = listview ;
             a list view version of the splitted text, this list being made
             recursively.
        """
# Split regarding one separator.
        thissep = seps[0]
        lensep  = len(thissep)
        answer  = []
        imax    = len(text)
        i       = 0
        ilast   = 0

        while(i < imax):
            if text[i:].startswith(thissep):
                lastpiece = text[ilast: i]

                if not(self.esc_char and lastpiece.endswith(self.esc_char)):
                    i    += lensep
                    ilast = i

                    if self.strip:
                        lastpiece = lastpiece.strip()

                    answer.append(lastpiece)

            i += 1

        endtext = text[ilast:]

        if endtext:
            if self.strip:
                endtext = endtext.strip()

            answer.append(endtext)

# Split regarding other separators.
        otherseps = seps[1:]

        if otherseps:
            answer = [
                self._build(
                    text   = piece,
                    seps   = otherseps
                )
                for piece in answer
            ]

# The job has been done !
        return answer


# ------------------------------------ #
# -- ITERATE EASILY IN THE LISTVIEW -- #
# ------------------------------------ #

    def iter(self, listview = None):
        """
prototype::
    see   = SplitInfos , self._iter
    arg   = None, listview: listview = None ;
            a listview made by an instance of ``MultiSplit``, or ``None`` if you
            want to use the last listview built.
    yield = SplitInfos
        """
        if listview == None:
            listview = self.listview

        return self._iter(listview, depth = 0)


    def _iter(self, listview, depth):
        """
prototype::
    see   = SplitInfos
    arg   = listview: listview ;
            a listview or a sublistview made by an instance of ``MultiSplit``.
    arg   = int: depth ;
            the depth level of the separators to use.
    yield = SplitInfos
        """
        if listview:
            if isinstance(listview[0], str):
                yield SplitInfos(
                    type = "sep",
                    val  = self.seps[depth]
                )

                for x in listview:
                    yield SplitInfos(
                        type = "val",
                        val  = x
                    )

            else:
                for x in listview:
                    yield SplitInfos(
                        type = "sep",
                        val  = self.seps[depth]
                    )

                    for y in self._iter(
                        listview = x,
                        depth    = depth + 1
                    ):
                        yield y


def between(
    text,
    seps
):
    """
prototype::
    arg    = str: text ;
             the text that must be splitted
    arg    = [str, str]: seps ;
             ``seps[0]`` is the start delimiter and ``seps[1]`` the end
             delimiter, none of this strings can be empty
    return = [str, str, str] ;
             ``[before, between, after]`` where ``between`` is the piece of text
             between the first ``seps[0]`` and ``seps[1]``, in this order, that
             have been found in ``text``, and where ``before`` is just before
             ``seps[0]``, and ``after`` just after ``seps[1]`` (if nothing has
             been found, the unfction returns ``[text, "", ""]``)


Here is an example of use.

pyterm::
    >>> from mistool.string_use import between
    >>> text = "f(x ; y) = x**2 + y**2"
    >>> seps = ["(", ")"]
    >>> print(between(text, seps))
    [
        'f',                # Before
        'x ; y',            # Between
        ' = x**2 + y**2'    # After
    ]
    >>> seps = ["{", "}"]
    >>> print(between(text, seps))
    Traceback (most recent call last):
    [...]
    ValueError: the starting text has not been found.
    """
    if not isinstance(seps, list) or len(seps) != 2 \
    or not isinstance(seps[0], str) or not isinstance(seps[1], str) \
    or seps[0] == "" or seps[1] == "":
        raise TypeError(
            'the variable << seps >> must be a list of two non-empty strings.'
        )

    start, end = seps

    s = text.find(start)

    if s == -1:
        raise ValueError('the starting text has not been found.')

    sbis = s + len(start)

    e = text.find(end, sbis)

    if e == -1:
        raise ValueError(
            'the ending text has not been found after the starting text.'
        )


    return [text[:s], text[sbis:e], text[e + len(end):]]


# ---------- #
# -- JOIN -- #
# ---------- #

def joinand(
    texts,
    andtext = "and"
):
    """
prototype::
    arg    = list(str): texts ;
             the texts to be joined
    arg    = str: andtext = "and" ;
             the text used to separate the two last strings
    return = str ;
             the text obtained by joining the strings in ``texts`` using comas
             between each string, excpet for the two last ones that are separated
             by the value of ``andtext``


Here is a small example.

pyterm::
    >>> from mistool.string_use import joinand, AND_TEXT
    >>> texts = ["1", "2", "3"]
    >>> print(joinand(texts))
    1, 2 and 3
    >>> fr_andtext = "et"
    >>> print(joinand(texts = texts, andtext= fr_andtext))
    1, 2 et 3
    """
    if len(texts) == 1:
        return texts[0]

    if andtext == None:
        andtext = AND_TEXT

    return "{0} {1} {2}".format(
        ", ".join(texts[:-1]),
        andtext,
        texts[-1]
    )


# --------------------------------------- #
# -- ASCII TRANSLATION OF AN UTF8 TEXT -- #
# --------------------------------------- #

def isascii(text):
    """
prototype::
    arg    = str: text ;
             the text to be tested
    return = bool ;
             ``True`` if the text contains only ¨ascii characters, or ``False``
             if not

Here is how to use this function.

pyterm::
    >>> from mistool.string_use import isascii
    >>> print(isascii("Vive la France !"))
    True
    >>> print(isascii("¡Viva España!"))
    False
    """
    return bool(set(text) <= ASCII_CHARS)


def ascii(
    text,
    oldnew = {},
    strict = True
):
    """
prototype::
    arg    = str: text ;
             the text to be translated
    arg    = {str: str}: oldnew = {} ;
             this dictionary uses couples ``(key, value)`` that are of the kind
             ``(non-ascii character, ascii version)``
    arg    = bool: strict = True ;
             ``strict = True`` indicates to raise an error when the translation
             can only be partial, and with ``strict = True`` no error will be
             raised
    return = str ;
             a partial or total ¨ascii version of ``text``


=========
Basic use
=========

The aim of this function is to give an ¨ascii translation of a text. The typical
use is for avoiding strange names of files. Here is a standard use where you can
see that non-¨ascii ponctuation mark are simply cleaned.

pyterm::
    >>> from mistool.string_use import ascii
    >>> print(ascii("¡Viva España!"))
    Viva Espana!


=======================
Doing more replacements
=======================

You can use the optional argument ``oldnew`` so as to do more replacements. In
the code below we have choose to also clean ``!``.

pyterm::
    >>> from mistool.string_use import ascii
    >>> oldnew = {'!': ""}
    >>> print(ascii(text = "¡Viva España!", oldnew = oldnew))
    Viva Espana


================
Partial cleaning
================

Sometimes, you just want to change the most characters as possible. In the
example below, we use ``strict`` so as to obtain ``L'Odyssee de (`` instead
of an error as the second use of ``ascii`` shows.

pyterm::
    >>> from mistool.string_use import ascii
    >>> print(ascii(text = "L'Odyssée de ∏", strict = False))
    L'Odyssee de ∏
    >>> print(ascii("L'Odyssée de ∏"))
    Traceback (most recent call last):
    [...]
    ValueError: ASCII conversion can't be made because of the character << ∏ >>.
    You can use the function ``_ascii_report`` so as to report more precisely
    this fealure with eventually an ascii alternative.


===============================
Improving the replacements made
===============================

It's easy to increase the list of special characters managed by default.

    1) The first method is for very special tunings useful at a moment, in that
    case just use the optional argument ``oldnew``.

    2) If you think that your tuning is general enough, just follow the steps
    below where we will suppose that we want to give ascii representations for
    the greek letters "𝛂", "𝛃" and "𝝲". The upper case variants will be
    automatically managed.

        a) First use the following lines in a terminal.

        pyterm::
            >>> from mistool.string_use import _ascii_report
            >>> print(_ascii_report("𝛂𝛃𝝲"))

        b) When you launch this snippet, you will obtain the output below.

        code::
            ==============================================
            TO SEND TO THE AUTHOR OF ``misTool``

            Subject of your mail : "mistool: ascii report"
            ==============================================

            Just replace each "?" with an appropriate
            ASCII character(s).

            ? >>> 𝝲 : MATHEMATICAL SANS-SERIF BOLD SMALL GAMMA
            ? >>> 𝛃 : MATHEMATICAL BOLD SMALL BETA
            ? >>> 𝛂 : MATHEMATICAL BOLD SMALL ALPHA

        c) The most important lines are the ones with your special letters. Just
        copy all of them and produce the following text that you will send to
        the author of this package. Here we have coosen to associate "a", "b"
        and "g" to "𝛂", "𝛃" and "𝝲" respectively.

        code::
            A sympathic message... ;-)

            g >>> 𝝲 : MATHEMATICAL SANS-SERIF BOLD SMALL GAMMA
            b >>> 𝛃 : MATHEMATICAL BOLD SMALL BETA
            a >>> 𝛂 : MATHEMATICAL BOLD SMALL ALPHA
    """
    for onechar in set(text) - ASCII_CHARS:
        if onechar not in oldnew:
            infos = ucname(onechar).split(" ")

            asciichar = None

            if "SMALL" in infos:
                caseformat = "lower"

            else:
                caseformat = "upper"

            if "LETTER" in infos:
                i = infos.index("LETTER")
                asciichar = infos[i + 1]

            elif "LIGATURE" in infos:
                i = infos.find("LIGATURE")
                asciichar = infos[i + 1]

            elif "MARK" in infos:
                asciichar = ""

            if asciichar != None:
                oldnew[onechar] = case(
                    text = asciichar,
                    kind = caseformat
                )

            elif strict:
                raise ValueError(
                    "ASCII conversion can't be made because of the character "
                    "<< {0} >>. ".format(onechar) + "\nYou can use the "
                    "function ``_ascii_report`` so as to report more precisely "
                    "this fealure with eventually an ascii alternative."
                )

    return MultiReplace(oldnew)(text)


def _ascii_report(text):
    """
prototype::
    arg    = str: text ;
             the non-¨ascii characters for the report
    return = str ;
             a text to be sent to the author of ¨mistool
    """
    problems = []

    for onechar in set(text) - ASCII_CHARS:
        try:
            ascii(onechar)

        except ValueError as e:
            problems.append(
                "? >>> {0} : {1}".format(
                    onechar,
                    ucname(onechar)
                )
            )

    if problems:
        problems = """
==============================================
TO SEND TO THE AUTHOR OF ``misTool``

Subject of your mail : "mistool: ascii report"
==============================================

Just replace each "?" with an appropriate
ASCII character(s).

{0}
    """.format("\n".join(problems))

    else:
        problems = "Nothing to report."

    return problems








# ----------------- #
# -- LOOKING FOR -- #
# ----------------- #

# Source : http://www.developpez.net/forums/d921494/autres-langages/python-zope/general-python/naturel-chaine-stockage

class AutoComplete:
    """
prototype::
    arg    = str: lang = DEFAULT_LANG ;
             ????
    return = str ;
             ????





-----------------
Small description
-----------------

The aim of this class is to ease auto completions. Here is an example.

python::
from mistool.string_use import AutoComplete
myac = AutoComplete(
    words = [
        "article", "artist", "art",
        "when", "who", "whendy",
        "bar", "barbie", "barber", "bar"
    ]
)
print(myac.matching("art"))
print('---')
print(myac.matching(""))






Launched in a terminal, the preceding code will produce something similar to the
following output.

terminal::
    ['art', 'article', 'artist']
    ---
    [
        'art', 'article', 'artiste',
        'bar', 'barbie', 'barber',
        'when', 'whendy', 'who'
    ]


The method ``matching`` simply gives all the words starting with the prefix
given. If the prefix is empty, the matching words are all the words defining the
auto completion.


The search indeed uses a special "magical" dictionary which is stored in the
attribut ``assos``. With the preceding example, ``myac.assos`` is equal to the
dictionary below where the lists of integers correspond to the good indexes in
the ordered list of words.





python::
    {
        'words': [
    # A
            'art', 'article', 'artist',
    # B
            'bar', 'barber', 'barbie',
    # W
            'when', 'whendy', 'who'
        ],
        'completions': {
    # A
            'a'     : [0, 3],
            'ar'    : [0, 3],
            'art'   : [1, 3],
            'arti'  : [1, 3],
            'artic' : [1, 2],
            'artis' : [2, 3],
            'articl': [1, 2],
    # B
            'b'    : [3, 6],
            'ba'   : [3, 6],
            'bar'  : [4, 6],
            'barb' : [4, 6],
            'barbe': [4, 5],
            'barbi': [5, 6],
    # W
            'w'    : [6, 9],
            'wh'   : [6, 9],
            'whe'  : [6, 8],
            'when' : [7, 8],
            'whend': [7, 8]
        }
    }


You can directly give this dictionary like in the following fictive example.
This can be very useful when you always use the same list of words : just ask
one time to the class to build the "magical" dictionary, by giving the fixed
list of words just one time, and then store this dictionary to reuse it later
(you can use the function ``pyRepr``  of the module ``python_use`` to hard store
the dictionary).

python::
    myac = AutoComplete(
        assos = mymagicdict  # Previously build and stored somewhere.
    )


There is two other useful methods (see their docstrings for more informations).

    1) ``build`` simply builds the "magical" dictionary. This method can be used
    for local updating of the list of words used for the auto completion.

    2) ``missing`` simply gives the letters remaining after one prefix in a
    word.


-------------
The arguments
-------------

The instanciation of this class uses the following variables.

    1) ``words`` is the list of words to use for the auto completions.

    2) ``depth`` is the minimal size of the prefix used to look for the auto
    completions. By default, ``depth = 0`` which indicates to start the auto
    completion with the first letter.

    infoo:
        `3` seems to be a good value of ``depth`` for �gui application.

    3) ``assos`` is a "magical" dictionary that eases the auto completion. This
    dictionary is build by the method ``build`` from the list of words to be
    used for the auto completions.
    """

    def __init__(
        self,
        words = None,
        assos = None,
        depth = 0
    ):
# User's arguments
        self.words = words
        self.assos = assos
        self.depth = depth

# Update the value of ``self.assos``
        self._updateit = True







# --------------------- #
# -- SPECIAL SETTERS -- #
# --------------------- #

    @property
    def words(self):
        return self._words

    @words.setter
    def words(self, value):
        if value != None:
            self._updateit = True

        self._words = value


    @property
    def assos(self):
        return self._assos

    @assos.setter
    def assos(self, value):
        if value != None:
            self._updateit = True

        self._assos = value


    @property
    def depth(self):
        return self._depth

    @assos.setter
    def depth(self, value):
        self._updateit = True
        self._depth    = value


# -------------------------- #
# -- THE MAGIC DICTIONARY -- #
# -------------------------- #

    def build(self):
        """
prototype::
    arg    = str: lang = DEFAULT_LANG ;
             ????
    return = str ;
             ????





This method builds the "magical" dictionary that will ease the auto completions.
Indeed, if you create a class ``AutoComplete`` without giving a "magical"
dictionary ``dict``, the method ``build`` is automatically called.


info::
    The idea of the magical dictionary comes from cf::``this discusion ;
    http://www.developpez.net/forums/d921494/autres-langages/python-zope/general-python/naturel-chaine-stockage``
        """
# Can we do the job ?
        if self.words == None:
            raise ValueError(
                "you must give either the value of ``words`` or ``assos``."
            )

# Sorted list of single words.
        sortedwords = list(set(self.words))
        sortedwords = sorted(sortedwords)

# Maximum depth.
        depth = self.depth

        if depth == 0:
            for word in sortedwords:
                depth = max(depth, len(word) - 1)

# Let's build the magical dictionary.
        self.assos = {
            'words'      : sortedwords,
            'completions': {}
        }

        for idword, word in enumerate(sortedwords):
            maxSize = min(depth, len(word))

            for i in range(maxSize):
                prefix = word[:i+1]

                if prefix != sortedwords[idword]:
                    if prefix in self.assos['completions']:
                        self.assos['completions'][prefix][1] = idword + 1

                    else:
                        self.assos['completions'][prefix] = [idword, idword + 1]











    def matching(
        self,
        prefix
    ):
        """
prototype::
    arg    = str: lang = DEFAULT_LANG ;
             ????
    return = str ;
                 ????


This method looks for words given in the list ``words`` that start with the
string variable ``prefix``.
        """
        if prefix.strip() == '':
            return self.assos['words']

        if prefix in self.assos['completions']:
            first, last = self.assos['completions'][prefix]

            return self.assos['words'][first: last]

    def missing(
        self,
        prefix,
        word
    ):
        """
prototype::
    arg    = str: lang = DEFAULT_LANG ;
             ????
    return = str ;
                 ????


-----------------
Small description
-----------------

Giving a word ``"prefixExample"`` and one prefix ``"pre"``, this method will
return simply ``"fixExample"``.


-------------
The arguments
-------------

This method uses the following variables.

    1) ``prefix`` is a string corresponding to the prefix expected.

    2) ``word`` is a string where the prefix ``prefix`` must be removed.
        """
        if not word.startswith(prefix):
            raise ValueError(
                "the word << {0} >> does not start with the prefix << {1} >>."\
                    .format(word, prefix)
            )

        return word[len(prefix):]
