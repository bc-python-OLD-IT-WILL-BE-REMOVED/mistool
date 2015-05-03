#!/usr/bin/env python3

"""
Directory : mistool
Name      : string_use
Version   : 2014.10
Author    : Christophe BAL
Mail      : projetmbc@gmail.com

This module contains some simple tools dealing with strings.
"""

from unicodedata import name as ucname

from mistool.config.ascii import ASCII_CHARS
from mistool.config.frame import FRAMES_FORMATS, _ABREVS_FRAMES, _KEYS_FRAME

from mistool.config.pattern import PATTERNS_WORDS


# ------------- #
# -- REPLACE -- #
# ------------- #

def replace(
    text,
    replacements
):
    """
-----------------
Small description
-----------------

This function does replacements in the argument ``text`` using the assos
defined in the dictionary ``replacement``.


warning::
    The function does the replacements sequentially from the longer word to the
    shorter one.


Here is a small example.

python::
    from mistool import string_use

    littleExample = string_use.replace(
            text         = "one, two, three,...",
            replacements = {
                'one'  : "1",
                'two'  : "2",
                'three': "3"
            }
        )
    )


In that code, ``littleExample`` is equal to ``"1, 2, 3,..."``.


info::
    This function has not been build for texts to be replaced that contains some
    other texts to also replace. If you need this kind of feature, take a look
    at the class ``MultiReplace``.


-------------
The arguments
-------------

This function uses the following variables.

    1) ``text`` is a string argument corresponding to the text where the
    replacements must be done.

    2) ``replacements`` is a dictionary where each couple ``(key, value)`` is of
    the kind ``(text to find, replacement)``.
    """
    sortedkeys = sorted(
        replacements.keys(),
        key = lambda t: -len(t)
    )

    for old in sortedkeys:
        text = text.replace(old, replacements[old])

    return text


class MultiReplace:
    """
-----------------
Small description
-----------------

The purpose of this class is to replace texts that can contain some other texts
to also be replaced. Here is an example of use.

python::
    from mistool import string_use
    from mistool.config.pattern import PATTERNS_WORDS

    myReplace = string_use.MultiReplace(
        replacements = {
            'W1' : "word #1",
            'W2' : "word #2",
            'W12': "W1 and W2"
        },
        pattern = PATTERNS_WORDS["var"]
    )

    print(myReplace.replace("W1 and W2 = W12"))


Launched in a terminal, the preceding code will produce the following output.

terminal::
    word #1 and word #2 = word #1 and word #2


The only technical thing is the use of ``PATTERNS_WORDS["var"]`` which is
a regex grouping pattern. You can use directly the following patterns or use
your own grouping pattern.

    1) ``PATTERNS_WORDS["en"]`` is for words only made of ¨ascii letters.

    2) ``PATTERNS_WORDS["fr"]`` is for words only made of ¨ascii letters and
    the special letters "â", "à", "é", "è", "ê", "ë", "î", "ï", "ô", "ù", "ü",
    and "ç".

    3) ``PATTERNS_WORDS["var"]`` is for words only starting with one ¨ascii
    letter followed eventually by other ¨ascii letters, digits and underscores.


info::
    Before doing the replacements in a text, the class first build the
    dictionary ``self.replaceasit`` for which the replacements has been
    changed so to not contain text to be replaced. With the preceeding code,
    this dictionary is equal to the following one.

    python::
        {
            'W1' : "word #1",
            'W2' : "word #2",
            'W12': "word #1 and word #2"
        }


warning::
    In the following dictionnary defining replacements, there are cyclic
    definitions. In that case, the class will raise an error.

    python::
        replacements = {
            'WRONG_1': "one small text and  WRONG_2",
            'WRONG_2': "one small text, and then WRONG_3",
            'WRONG_3': "with WRONG_1, there is one problem here"
        }


-------------
The arguments
-------------

The instanciation of this class uses the following variables.

    1) ``replacements`` is a dictionary where each couple ``(key, value)`` is of
    the kind ``(text to find, replacement)``. Here the replacements can contain
    also text to be replaced.

    2) ``pattern`` is a regex grouping pattern indicating the kind of words to be replaced. By default, ``pattern = PATTERNS_WORDS["en"]`` where ``PATTERNS_WORDS`` is a renaming of ``config.pattern.PATTERNS_WORDS`` (see the the file ``config/pattern`` for more informations).
    """

    def __init__(
        self,
        replacements,
        pattern = PATTERNS_WORDS["en"]
    ):
        self.pattern      = pattern
        self.replacements = replacements
        self.replaceasit  = None

        self._crossreplace = None
        self._oldwords     = None

        self.update()

    def update(self):
        """
This method simply launches methods so as to verify that there is no cyclic
replacements, and then to build the direct replacements dictionary
``self.replaceasit``.
        """
        self._crossreplace = {}
        self._lookforcycle()
        self._replace_recursively()

    def _lookforcycle(self):
        """
This method verifies that there is no cyclic replacements.

Indeed all the job is done by the hidden method ``self._noviciouscycle``.
        """
# Building the crossing replacements.
        self._oldwords = list(self.replacements.keys())

        for old, new in self.replacements.items():
            self._crossreplace[old] = [
                x for x in self.pattern.findall(new)
                if x in self._oldwords
            ]

        self._noviciouscycle()

    def _noviciouscycle(
        self,
        visitedwords = [],
        nextwords    = None
    ):
        if nextwords == None:
            nextwords = self._oldwords

        for old in nextwords:
            oldinnew = self._crossreplace[old]

            if old in oldinnew:
                raise ValueError(
                    "<< {0} >> is used in its associated replacement." \
                        .format(old)
                )

            elif old in visitedwords:
                pos = visitedwords.index(old)

                visitedwords = visitedwords[pos:]
                visitedwords.append(old)
                visitedwords = [""] + visitedwords

                raise ValueError(
                    "the following viscious circle has been found." \
                    + "\n\t + ".join(visitedwords)
                )

            else:
                for new in oldinnew:
                    self._noviciouscycle(
                        visitedwords = visitedwords + [old],
                        nextwords    = self._crossreplace[old]
                    )

    def _replace_recursively(self):
        """
This method builds ``self.replaceasit`` the direct replacements dictionary.

Indeed all the job is done by the hidden method ``self._replace_oneword``.
        """
        self.replaceasit = {}

        for old, new in self.replacements.items():
            self.replaceasit[old] = self._replace_oneword(new)

    def _replace_oneword(
        self,
        text
    ):
        if not text:
            return text

        newtext = ""

        while True:
# Source :
#    http://www.developpez.net/forums/d958712/autres-langages/python-zope/general-python/amelioration-split-evolue/#post5383767
            newtext = self.pattern.sub(self._apply, text)

            if newtext == text:
                return text

            else:
                text = newtext

    def _apply(
        self,
        match
    ):
        """
This method is used to does the replacements corresponding the matching groups.
        """
        return self.replacements.get(match.group(1), match.group(0))

    def replace(
        self,
        text
    ):
        """
This method does the replacements in one text (indeed it simply calls the
function ``replace`` with the attribut ``self.replaceasit``).
        """
        return replace(
            text         = text,
            replacements = self.replaceasit
        )


# ------------------------------------- #
# -- ASCII TRANSLATION OF AN UTF TEXT-- #
# ------------------------------------- #

def _ascii_report(text):
    """
The function is to use to increase the list of the characters. A complete example
of use is given in the documentation of ``ascii``.
    """
    problems = []

    for onechar in set(text) - ASCII_CHARS:
        try:
            ascii(onechar)

        except StringUseError as e:
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

def ascii(
    text,
    replacements = {},
    strict       = True
):
    """
---------
Basic use
---------

The aim of this function is to give an ¨ascii translation of a text. The typical
use is for avoiding strange names of files. For example, the following lines of
code launched in a terminal will display the text ``Viva Espana!``.

python::
    from mistool import string_use

    print(
        string_use.ascii("¡Viva España!")
    )


-----------------------
Doing more replacements
-----------------------

You can use the optional argument ``replacement`` so as to do more replacements.
The code above will print ``Viva Espana`` instead of ``Viva Espana!``.

python::
    from mistool import string_use

    print(
        string_use.ascii(
            text         = "¡Viva España!",
            replacements = {'!': ""}
        )
    )


warning::
    You have to indicate the different case variants if you need them, and you
    have to know that the function does first the special replacements before
    cleaning the non ascii characters.


----------------
Partial cleaning
----------------

Sometimes, you just want to change the most characters as possible without. In
the example above, we use ``strict`` so as to obtain ``L'Odyssee de ᴨ`` instead
of an error.

python::
    from mistool import string_use

    print(
        string_use.ascii(
            text   = "L'Odyssée de ᴨ",
            strict = False
        )
    )


-------------------------------
Improving the replacements made
-------------------------------

It's easy to increase the list of special characters managed by default.

    1) The first method can be used for very special tunings like in the
    preceding code : just use the optional argument ``replacement``.

    2) If you think that your tuning is general enough, just follow the steps
    above where we will suppose that we want to give ascii representations for
    the greek letters "α", "β" and "γ". The upper case variants will be
    automatically managed.

        a) First use the following lines in a terminal.

        python::
            from mistool import string_use

            print(string_use._ascii_report("αβγ"))

        b) When you launch the snippet, you will obtain the output above.

        code::
            ====================================
            TO SEND TO THE AUTHOR OF ``misTool``
            ====================================

            Just replace each "?" with the appropriate
            ASCII character(s).

            ? >>> α : GREEK SMALL LETTER ALPHA
            ? >>> β : GREEK SMALL LETTER BETA
            ? >>> γ : GREEK SMALL LETTER GAMMA

        c) The most important lines are the ones with our special letters. Just
        copy all of them and produce the following text that you will send to the
        author of this package.

        code::
            A sympathic message... ;-)

            a >>> α : GREEK SMALL LETTER ALPHA
            b >>> β : GREEK SMALL LETTER BETA
            c >>> γ : GREEK SMALL LETTER GAMMA


-------------
The arguments
-------------

This function uses the following variables.

    1) ``text`` is simply the text to be translated.

    2) ``replacements`` is an optional dictionary giving assos from a
    character to an ascii, or not, character or string. By default, we have
    ``replacements = {}``.

    3) ``strict`` is an optional argument to use if you don't want the function
    to raise an error when the translation has been partial. By default, we have
    ``strict = True`` which indicates to raise an error.
    """
    for onechar in set(text) - ASCII_CHARS:
        if onechar not in replacements:
            infos = ucname(onechar).split(" ")

            asciichar = None

            if "SMALL" in infos:
                caseformat = "lower"

            else:
                caseformat = "upper"

            if "LETTER" in infos:
                i = infos.index("LETTER")
                asciichar = infos[i + 1]

                if len(asciichar) != 1:
                    asciichar = None

            elif "LIGATURE" in infos:
                i = infos.find("LIGATURE")
                asciichar = infos[i + 1]

            elif "MARK" in infos:
                asciichar = ""

            if asciichar != None:
                replacements[onechar] = case(
                    text = asciichar,
                    kind = caseformat
                )

            elif strict:
                raise ValueError(
                    "ASCII conversion can be achieved because of the character "
                    "<< {0} >>. ".format(onechar) + "\nYou can use the "
                    "function ``_ascii_report`` so as to report more precisely " "this with the possibility to indicate ascii assos."
                )

    text = replace(
        text         = text,
        replacements = replacements
    )

    return text

def isascii(text):
    """
This function simply return a boolean to know if a text contain only ASCII
characters.
    """
    return (set(text) <= ASCII_CHARS)


# ----------------- #
# -- LOOKING FOR -- #
# ----------------- #

# Source : http://www.developpez.net/forums/d921494/autres-langages/python-zope/general-python/naturel-chaine-stockage

class AutoComplete:
    """
-----------------
Small description
-----------------

The aim of this class is to ease auto completions. Here is an example.

python::
    from mistool import string_use

    myAC = string_use.AutoComplete(
        words = [
            "article", "artist", "art",
            "when", "who", "whendy",
            "bar", "barbie", "barber", "bar"
        ]
    )

    print(myAC.matching("art"))

    print('---')

    print(myAC.matching(""))


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
attribut ``assos``. With the preceding example, ``myAC.assos`` is equal to the
dictionary above where the lists of integers correspond to the good indexes in
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
    myAC = string_use.AutoComplete(
        assos = myMagicDict  # Previously build and stored somewhere.
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
        `3` seems to be a good value of ``depth`` for ¨gui application.

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
        if words == None and assos == None:
            raise ValueError(
                "you must give either the value of ``words`` or ``assos``."
            )

        self.words = words
        self.assos = assos
        self.depth = depth

# We have to build the magical dictionary.
        if self.assos == None:
            self.build()

    def build(self):
        """
This method builds the "magical" dictionary that will ease the auto completions.
Indeed, if you create a class ``AutoComplete`` without giving a "magical"
dictionary ``dict``, the method ``build`` is automatically called.


info::
    The idea of the magical dictionary comes from cf::``this discusion ;
    http://www.developpez.net/forums/d921494/autres-langages/python-zope/general-python/naturel-chaine-stockage``
        """
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


# -------------------- #
# -- JOIN AND SPLIT -- #
# -------------------- #

AND_TEXT = "and"

def joinand(
    texts,
    andtext = None
):
    """
-----------------
Small description
-----------------

This function joins texts given in the argument ``texts`` using coma as
separator excepted for the list piece of text which wil be preceded by default
by "and".

Here is a small example.

python::
    from mistool import string_use

    littleExample = string_use.joinand(["one", "two", "three"])


In that code, ``littleExample`` is equal to ``one, two and three"``.


You can change the text "and". There is two ways to do that.

    1) **Local change :** the function has on optional argument ``andText``
    which is the string value used before the last piece of text.

    2) **Global change :** ``AND_TEXT`` is the global constant to use so as to
    change the default text used before the last piece of text if the optional
    argument ``andText`` is not used when calling the function.


-------------
The arguments
-------------

This function uses the following variables.

    1) ``texts`` is a list of texts.

    2) ``andText`` is the text used betwen the two last texts. By default,
    ``andText = None`` which indicates to use the global constant ``AND_TEXT``
    which is equal to ``"and"`` by default.
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

def split(
    text,
    seps,
    escape = "",
    strip  = False
):
    """
-----------------
Small description
-----------------

This function allows to split a text using a list of separators, and not only a
single separator. Here is an example.

python::
    from mistool import string_use

    splitText = string_use.split(
        text  = "p_1 ; p_2 ; p_3 | r_1 ; r_2 | s",
        seps  = ["|", ";"],
        strip = True
    )

In this code, the variable ``splitText`` is equal to the following list :
``['p_1', 'p_2', 'p_3', 'r_1', 'r_2', 's']``.


You can escape separators like in the following example that also uses the
possibility to give a single string instead of a one value list.

python::
    from mistool import string_use

    splitText = string_use.split(
        text   = "p_1 \; p_2 ; p_3",
        seps   = ";",
        escape = "\\",
        strip  = True
    )

In this code, the variable ``splitText`` is equal to the following list :
``['p_1 \; p_2', 'p_3']``.


-------------
The arguments
-------------

This function uses the following variables.

    1) ``text`` is simply the text to split.

    2) ``seps`` is either a string for a single separator, or a list or a tuple
    of separators.

    3) ``escape`` is a string used to escape the separators. By default,
    ``escape = None`` which indicates that there is no escaping feature.

    4) ``strip`` is a boolean variable to strip, or not, each pieces of text
    found. By default, ``strip = False``.
"""
# Clean out spaces.
    if strip:
        text = text.strip()

# No separator
    if not seps:
        return [text]

# At least one separator
    if isinstance(seps, str):
        seps = [seps]

    elif isinstance(seps, tuple):
        seps = list(seps)

    elif not isinstance(seps, list):
        raise TypeError(
            "the variable << sep >> must be a list or tuple of strings."
            "\n\t{0}".format(sep)
        )

    for sep in seps:
        if not isinstance(sep, str):
            raise TypeError(
                "the variable << seps >> must be list or tuple of strings."
                "\n\t{0}".format(seps)
            )

# << Warning ! >> We must sort the opening symbolic tags from the longer one
# to the shorter.
    seps.sort(key = lambda x: -len(x))

# We look for the positions where the separators are, but we also have to clean
# overlapping texts. Think of the separators "(((" and "(" for example.
#
# << WARNING ! >> We use the fact that the first positions are the ones of
# the longest separators !
    _posfound = []
    positions = []

    for sep in seps:
        sepsize = len(sep) - 1
        i = text.find(sep)

        while(i != - 1):
            iend = i + sepsize

            if not(escape and text[:i].endswith(escape)) \
            and i not in _posfound and iend not in _posfound:
                positions.append((i, iend))
                _posfound.extend(range(i, iend + 1))

            i = text.find(sep, iend + 1)

    positions.sort()

# Let's build the splited text.
    answer  = []
    lastend = 0

    for start, end in positions:
        answer.append(text[lastend: start])
        lastend = end + 1

    answer.append(text[lastend:])

# Strip or not strip, that is the question.
    if strip:
        answer = [x.strip() for x in answer]

# The job has been done !
    return answer

class _SplitKind:
    """
This class is simply an object like class used by the method ``__iter__`` of
the class ``MultiSplit``.
    """

    def __init__(
        self,
        type,
        val
    ):
        self.type = type
        self.val  = val

class MultiSplit:
    """
-----------------
Small description
-----------------

The purpose of this class is to split a text at different levels. You can use
either a list view version of the split text, or work with a special iterator.


Here is an example of the list view version of the split text.

python::
    from mistool import string_use

    SplitText = string_use.MultiSplit(
        text = "p_1 , p_2 ; p_3 | r_1 ; r_2 | s",
        seps = [
            "|",
            (";", ",")
        ],
        strip = True
    )

    listview = SplitText.listview


In this code, the variable ``listview`` is equal to the following list. There
is as many level of lists that the length of the list ``seps``. The use of
``(";", ",")`` simply indicates that the separators ``;`` and ``,`` have the
same importance.

python::
    [
        ['p_1', 'p_2', 'p_3'],
        ['r_1', 'r_2'],
        ['s']
    ]


Let see with an example how to use the instance as an iterator so as to ease
the walk in the split text.

python::
    from mistool import string_use

    SplitText = string_use.MultiSplit(
        text  = "p_1 , p_2 ; p_3 | r_1 ; r_2 | s",
        seps  = ["|", ";", ","],
        strip = True
    )

    for x in SplitText:
        print("{0} ---> {1}".format(x.type, x.val))


Launched in a terminal, the code will produce the following output that shows
how to work easily with the iterator of the class ``MultiSplit``. You have to
know that the type is a string, and also that for the "sep" type, the associated
value is equal to the separator used when the instance has been created.

terminal::
    sep ---> |
    sep ---> ;
    sep ---> ,
    list ---> ['p_1', 'p_2']
    sep ---> ;
    sep ---> ,
    list ---> ['p_3']
    sep ---> |
    sep ---> ;
    sep ---> ,
    list ---> ['r_1']
    sep ---> ;
    sep ---> ,
    list ---> ['r_2']
    sep ---> |
    sep ---> ;
    sep ---> ,
    list ---> ['s']


-------------
The arguments
-------------

The instanciation of this class uses the following variables.

    1) ``text`` is simply the text to split.

    2) ``seps`` is either a string for a single separator, or a list from the
    stronger separator to the weaker one. You can use list or tuple to gather
    separators having the same level of priority.

    3) ``escape`` is a string used to escape the separators. By default,
    ``escape = None`` which indicates that there is no escaping feature.

    4) ``strip`` is a boolean variable to strip, or not, each pieces of text
    found. By default, ``strip = False``.
"""

    def __init__(
        self,
        text,
        seps,
        escape = "",
        strip  = False
    ):
        self.text   = text
        self.seps   = seps
        self.strip  = strip
        self.escape = escape

        if isinstance(self.seps, str):
            self.seps = [self.seps]

        self.listview = self.build()

    def build(self):
        """
This method builds the list view version of the split text.

Indeed all the job is done by the hidden method ``self._build``.
        """
        return self._build(
            text   = self.text,
            seps   = self.seps,
            escape = self.escape,
            strip  = self.strip
        )

    def _build(
        self,
        text,
        seps,
        escape,
        strip
    ):
# No separator
        if not seps:
            if strip:
                text = text.strip()

            answer = [text]

# At least one separator
        else:
            answer = split(
                text   = text,
                seps   = seps[0],
                escape = escape,
                strip  = strip
            )

            otherseps = seps[1:]

            if otherseps:
                answer = [
                    self._build(
                        text   = piece,
                        seps   = otherseps,
                        escape = escape,
                        strip  = strip
                    )
                    for piece in answer
                ]

# The job has been done !
        return answer

    def __iter__(self):
        return self._iter(listview = self.listview)

    def _iter(
        self,
        listview,
        depth = 0
    ):
        if listview:
            if isinstance(listview[0], str):
                yield _SplitKind(
                    type = "sep",
                    val  = self.seps[depth]
                )

                yield _SplitKind(
                    type = "list",
                    val  = listview
                )

            else:
                for x in listview:
                    yield _SplitKind(
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
    start,
    end,
    keep = False
):
    """
-----------------
Small description
-----------------

The function will look for the piece of text between the first texts ``start``
and ``end`` found in ``text``. Then by default the function returns the text
before the text ``start`` and the one after the text ``end`` in a couple.

If ``keep = True`` then the text ``start`` will be added at the end of the first
text returned, and the second text returned will begin with the text ``end``.

You can also use ``keep = (True, False)`` or ``keep = (True, False)`` so as to
use just one half of the features which have just been explained. Indeed ``keep
= True`` and ``keep = False`` are shortcuts for ``keep = (True, True)`` and
``keep = (False, False)`` respectively.


-------------
The arguments
-------------

This function uses the following variables.

    1) ``text`` is a string argument corresponding to the texte where the search
    must be done.

    2) ``start`` and ``end`` are string arguments that indicated the start and
    end pieces of text to find.

    3) ``keep`` is an optional argument which can be either a boolen or a couple
    of boolean. By default, ``keep = False`` which indicates to unkeep the start
    and the end in the piece of text found.
    """
    if start == "" and end == "":
        raise ValueError(
            'the variables << start >> and  << end >> can not be both empty.'
        )

    if isinstance(keep, bool):
        keepstart = keep
        keepend   = keep

    else:
        keepstart, keepend = keep

    if start == "":
        s = 0

    else:
        s = text.find(start)

        if s == -1:
            raise ValueError(
                'the starting text << {0} >> has not been found.'.format(start)
            )

        s += len(start)

    if end == "":
        e = s

    else:
        e = text.find(end, s)

        if e == -1:
            message = 'the ending text  << {1} >> has not been found after ' \
                    + 'the first text << {0} >>.'

            raise ValueError(message.format(start, end))

        if start == "":
            s = e


    if not keepstart and start:
        s -= len(start)

    if not keepend and end:
        e += len(end)


    return (text[:s], text[e:])


# --------------------- #
# -- CASE FORMATTING -- #
# --------------------- #

_CASE_VARIANTS = ['lower', 'upper', 'sentence', 'title', 'firstLast']

def case(
    text,
    kind
):
    """
-----------------
Small description
-----------------

This function produces different case variants of the text contained in the
string variable ``text``.


For example, ``case("onE eXamPLe", "lower")``, ``case("onE eXamPLe", "upper")``
and ``case("onE eXamPLe", "sentence")`` and ``case("onE example", "title")`` are
respectively equal to "one example", "ONE EXAMPLE", "OnE eXamPLe" and "One
Example".


You can also the weird transformation ``case("onE eXamPLe", "firstLast")`` which
is equal to "One examplE". This special feature is indeed used by pyBaNaMa which
is another project of the author of the package ¨mistool.


If you need all the possible case variants, juste use ``case("onE eXamPLe",
"all")`` which is equal to the following dictionary.

python::
    {
        'lower'    : 'one example',
        'upper'    : 'ONE EXAMPLE',
        'sentence' : 'One example',
        'title'    : 'One Example',
        'firstLast': 'One examplE'
    }


If for example you only need to have the lower case and the title case versions
of one text, then you just have to use ``case("OnE eXamPLe", "lower title")``
which is equal to the following dictionary.

python::
    {
        'lower': 'ONE EXAMPLE',
        'title': 'One Example'
    }


-------------
The arguments
-------------

This function uses the following variables.

    1) ``text` is a string variable corresponding to the text to modify.

    2) ``kind`` indicates the case transformation wanted. The possible case
    variants are the following ones.

        a) ``"lower"``, ``"upper"``, ``"sentence"`` and ``"title"`` are for
        lower case, upper case, sentence and title case versions of one text.

        b) ``"firstLast"`` is to have a lower case text with its firts and last
        letter in upper case.

        c) ``"all"`` is to have all the possible case variants.

        d) If for example you only need to have the lower case and the title
        case versions of one text, just use ``kind = "lower title")``.
    """
    kind = kind.strip()

    if kind == 'all':
        answer = {}

        for kind in _CASE_VARIANTS:
            answer[kind] = case(text, kind)

        return answer

    elif ' ' in kind:
        answer = {}

        for kind in kind.split(' '):
            kind = kind.strip()

            if kind not in answer:
                casevariant = case(text, kind)

                if isinstance(casevariant, dict):
                    for kind, onecase in casevariant.items():
                        answer[kind] = onecase

                else:
                    answer[kind] = casevariant

        return answer

    elif kind == 'lower':
        return text.lower()

    elif kind == 'upper':
        return text.upper()

    elif kind == 'sentence':
        return text[0].upper() + text[1:].lower()

    elif kind == 'title':
        return text.title()

    elif kind == 'firstLast':
        return text[0].upper() + text[1:-1].lower() + text[-1].upper()

    else:
        raise ValueError(
            '<< {0} >> is not an existing kind of case variant formatting.' \
                .format(kind)
        )

def camelto(
    text,
    kind
):
    """
-----------------
Small description
-----------------

This function transforms one text using camel syntax to one of the case variants
proposed by the function ``case``. Indeed, each time one upper letter is met,
one underscore followed by one space is added before it, then the function
``case`` is called, and finally extra spaces are removed. For example,
``camelto("oneExample", "title")`` is equal to ``"One_Example"``.


-------------
The arguments
-------------

This function uses the following variables.

    1) ``text` is a string variable corresponding to the text to modify.

    2) ``kind`` indicates the case transformation wanted. The possible case
    variants are the same as for the function ``case``.
    """
    answer = ''

    for onechar in text:
        if onechar.isupper():
            answer += '_ '

        answer += onechar

    answer = case(answer, kind)

    if isinstance(answer, dict):
        for kind, text in answer.items():
            answer[kind] = text.replace('_ ', '_')

    else:
        answer = answer.replace('_ ', '_')

    return answer


# ------------------ #
# -- CASE TESTING -- #
# ------------------ #

def iscase(
    text,
    kind
):
    """
-----------------
Small description
-----------------

If ``kind`` is one of the strings ``"lower"``, ``"upper"``, ``"sentence"``,
``"title"`` or ``"firstLast"`` the function will simply return the result of
the test ``text == case(text, kind)``. See the documentation of the function
``case`` for more informations about this case formats.

If ``kind = "mix"``, the answer returned will be ``True`` only if the text is
not all lower, not all upper and not in sentence-case format.


warning::
    Something like ``One examplE`` has both the case ``"mix"`` and
    ``"sentence"``.


-------------
The arguments
-------------

This function uses the following variables.

    1) ``text`` is simply a string representing the text to be tested.

    2) ``kind`` is a string whose values can only be ``"lower"``, ``"upper"``,
    ``"sentence"``, ``"title"``, ``"firstLast"`` or ``"mix"``.
    """
    if kind == "mix":
        return not text.islower() \
               and not text.isupper() \
               and text != case(text, "sentence")

    elif kind not in _CASE_VARIANTS:
        raise ValueError(
            '<< {0} >> is not an existing kind of case variant testing.' \
                .format(kind)
        )

    elif kind == "lower":
        return text.islower()

    elif kind == "upper":
        return text.isupper()

    else:
        return text == case(text, kind)


# ------------------- #
# -- DECORATE TEXT -- #
# ------------------- #

DEFAULT_FRAME = FRAMES_FORMATS['python_basic']

def _draw_hrule(
    rule,
    left,
    right,
    lenght,
    nbspace
):
    """
-----------------
Small description
-----------------

This function is used to draw the horizontal rules of a frame around one text.


-------------
The arguments
-------------

This function uses the following variables.

    1) ``rule`` is the character used to draw the rule.

    2) `left`` and ``right`` are the first and last additional texts used around
    the rule.

    3) ``lenght`` is an integer giving the lenght of the rule.

    4) ``nbspace`` is the number of spaces to add before the first additional
    text (this is for cases when left corners have different lenghts).
    """
    if rule:
        return [
            ' '*(nbspace - len(left))
            + left
            + rule*lenght
            + right
        ]

    elif left:
        return [
            left
            + ' '*lenght
            + right
        ]

    elif right:
        return [
            ' '*(nbspace + lenght)
            + right
        ]

    else:
        return []

def frame(
    text,
    format = DEFAULT_FRAME,
    center = True
):
    """
--------------
Default frames
--------------

This function makes it possible to put one text into one frame materialized by
ASCII characters. This can be usefull for console outputs or for pretty comments
in listings like the following python comment.

python::
    #############
    # one       #
    # comment   #
    # easily    #
    # formatted #
    #############


This text has been produced using the following lines.

python::
    from mistool import string_use

    oneText = '''one
    comment
    easily
    formatted'''

    print(
        string_use.frame(
            text   = oneText,
            center = False
        )
    )


By default, ``center`` is equal ``True`` which asks to merely center the content
of the frame. Here we use the default frame ``DEFAULT_FRAME`` which is equal to
``FRAMES_FORMATS['python_basic']``. The dictionary ``FRAMES_FORMATS`` contains all
the default formats. For example, in the following code we use another default
formats.

python::
    from mistool import string_use

    oneText = '''one
    comment
    with C-like
    style'''

    print(
        string_use.frame(
            text   = oneText,
            format = string_use.FRAMES_FORMATS['c_basic'],
            center = False
        )
    )


This will give the following output.

code_c::
    /***************
     * one         *
     * comment     *
     * with C-like *
     * style       *
     ***************/


---------------
Homemade frames
---------------

The following frame can be obtained by using the default format
``string_use.FRAMES_FORMATS['python_pretty']``.

python::
    # ------------- #
    # -- one     -- #
    # -- pretty  -- #
    # -- comment -- #
    # ------------- #


Let see the definition ``FRAMES_FORMATS['python_pretty']``.

python::
    {
        'rule': {
            'down': '-',
            'left': '--',
            'right': '--',
            'up': '-'
        },
        'extra': {
            'rule': {
                'left': '#',
                'right': '#'
            }
        }
    }


In this dictionary, we define a frame and then an extra frame. Indeed, you can
use a dictionary looking like the one above. A missing key is a shortcut to
indicate an empty string.

python::
    {
        'rule' : {
            'up'   : "Single character",
            'down' : "Single character",
            'left' : "Some characters",
            'right': "Some characters"
        },
        'corner': {
            'leftup'   : "Some characters",
            'leftdown' : "Some characters",
            'rightup'  : "Some characters",
            'rightdown': "Some characters"
        },
        'extra': {
            'rule' : {
                'up'   : "Single character",
                'down' : "Single character",
                'left' : "Some characters",
                'right': "Some characters"
            },
            'corner': {
                'leftup'   : "Some characters",
                'leftdown' : "Some characters",
                'rightup'  : "Some characters",
                'rightdown': "Some characters"
            },
        }
    }


You can use the following abreviations for the positional keys.

    * ``u``, ``d``, ``l`` and ``r`` are abreviations for ``up``, ``down``,
    ``left`` and ``right`` respectively.

    * ``lu``, ``ld``, ``ru`` and ``rd`` are abreviations for ``leftup``,
    ``leftdown``, ``rightup`` and ``rightdown`` respectively.


-------------
The arguments
-------------

This function uses the following variables.

    1) ``text`` is a string value corresponding to the text to put in a frame.

    2) ``center`` is a boolean variable to center or not the text inside the
    frame. By default, ``center = True``.

    3) ``format`` is an optional dictionary defining the frame. By default,
    ``format = DEFAULT_FRAME`` which is equal to
    ``FRAMES_FORMATS['python_basic']``.

    info::
        All the default formats are in the dictionary ``FRAMES_FORMATS``.


    The general structure of a dictionary to use with ``format`` is the following
    one.
    """
# Default values must be chosen if nothing is given.
    if not set(format.keys()) <= {'rule', 'corner', 'extra'}:
        raise ValueError("illegal key for the dictionary << format >>.")

    for kind in ['rule', 'corner', 'extra']:
        if kind not in format:
            format[kind] = {}


    for kind in ['rule', 'corner']:
        if not set(format[kind].keys()) <= _KEYS_FRAME[kind]:
            raise ValueError(
                "illegal key for the dictionary << format >>. "
                "See the kind << {0} >>.".format(kind)
            )

        for key, abrev in _ABREVS_FRAMES[kind].items():
            if abrev in format[kind] and key in format[kind]:
                message = "use of the key << {0} >> and its abreviation " \
                        + "<< {1} >> for the dictionary << format >>."

                raise ValueError(message.format(key, abrev))

            if abrev in format[kind]:
                format[kind][key] = format[kind][abrev]

            elif key not in format[kind]:
                format[kind][key] = ""

# Horizontal rules can only use one single character.
    for loc in ['up', 'down']:
        if len(format['rule'][loc]) > 1:
            message = "You can only use nothing or one single character " \
                    + "for rules.\nSee << {0} >> for the {1} rule."

            raise ValueError(
                message.format(format['rule'][loc], loc)
            )

# Infos about the lines of the text.
    lines     = [oneline.rstrip() for oneline in text.splitlines()]
    nbmaxchar = max([len(oneline) for oneline in lines])

# Space to add before vertical rules.
    nbspace = max(
        len(format['corner']['leftup']),
        len(format['corner']['leftdown'])
    )

    spacetoadd = ' '*nbspace

# Text decoration for vertical rules
    if format['rule']['left']:
        leftrule = format['rule']['left'] + ' '
    else:
        leftrule = ''

    if format['rule']['right']:
        rightrule = ' ' + format['rule']['right']
    else:
        rightrule = ''

# Length of the rule without the corners
    lenght = nbmaxchar + len(leftrule) + len(rightrule)

# First line of the frame
    answer = _draw_hrule(
        rule    = format['rule']['up'],
        left    = format['corner']['leftup'],
        right   = format['corner']['rightup'],
        lenght  = lenght,
        nbspace = nbspace
    )

# Management of the lines of the text
    for oneline in lines:
        nbmissingspaces = nbmaxchar - len(oneline)

# Space before and after one line of text.
        if center:
            if nbmissingspaces % 2 == 1:
                spaceafter = ' '
            else:
                spaceafter = ''

            nbmissingspaces = nbmissingspaces // 2

            spacebefore = ' '*nbmissingspaces
            spaceafter += spacebefore

        else:
            spacebefore = ''
            spaceafter = ' '*nbmissingspaces

        answer.append(
            spacetoadd
            +
            '{0}{1}{2}{3}{4}'.format(
                leftrule,
                spacebefore,
                oneline,
                spaceafter,
                rightrule
            )
        )

# Last line of the frame
    answer += _draw_hrule(
        rule    = format['rule']['down'],
        left    = format['corner']['leftdown'],
        right   = format['corner']['rightdown'],
        lenght  = lenght,
        nbspace = nbspace
    )

    answer = '\n'.join([x.rstrip() for x in answer])

# Does we have an extra frame ?
    if format['extra']:
        try:
            answer = frame(
                text   = answer,
                format = format['extra'],
                center = center
            )

        except ValueError as e:
            raise ValueError(
                str(e)[:-1] + " in the definition of the extra frame."
            )

# All the job has been done.
    return answer


# ------------------ #
# -- STEP BY STEP -- #
# ------------------ #

class Step:
    """
-----------------
Small description
-----------------

This class displays texts for step by step actions. The numbering of the steps
is automatically updated and displayed.


-------------
The arguments
-------------

There are two optional variables.

    1) ``nb`` is the number of the current step. When the class is instanciated,
    the default value is ``1``.

    2) ``deco`` indicates how to display the numbers. When the class is
    instanciated, the default value is ``""1)""`` where ``1`` symbolises the
    numbers.
    """
    def __init__(
        self,
        nb   = 1,
        deco = "1)"
    ):
        self.nb   = nb
        self.deco = deco.replace('1', '{0}')

    def print(
        self,
        text,
        deco
    ):
        """
-----------------
Small description
-----------------

This method simply prints ``deco`` the text of the actual numbering, and then
``text`` the content of the actual step.

You can redefine this method for finer features.


-------------
The arguments
-------------

This method uses the following variables.

    1) ``text`` is simply the text of the actual step.

    2) ``deco`` is a string corresponding to the text indicated what is the
    actual step number.
        """
        print(
            deco,
            text,
            sep = " "
        )

    def display(
        self,
        text
    ):
        """
-----------------
Small description
-----------------

This method simply calls the method ``self.print`` so as to print the
informations contained in the variable ``text``, and then ``self.nb`` is
augmented by one unit.

You can redefine the method ``self.print`` for finer features.


-------------
The arguments
-------------

This method uses one variable ``text`` which is the text of the actual step.
        """
        self.print(
            text = text,
            deco = self.deco.format(self.nb)
        )

        self.nb += 1
