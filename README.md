What about this ?
=================

**misTool** is a contraction of **missing**, **miscellaneous** and **tool**.
This package contains the following modules that could be useful for Python
developments.

If you want more informations and examples than thereafter, just take a look at
the docstrings.


Warning about this new version `1.0.0`
======================================

This version breaks a lot of things regarding to the previous ones given on PyPI *(for example, the module ``log_test_use`` has been removed)*. See the change log for more informations.


Which OS can use this program ?
===============================

The modules have been tested under Mac OS El Capitan but they must work on all platforms.


Features of the module ``string_use``
=====================================

Auto completion
---------------

```python
>>> from mistool.string_use import AutoComplete
>>> myac = AutoComplete(
...     words = [
...         "article", "artist", "art",
...         "when", "who", "whendy",
...         "bar", "barbie", "barber", "bar"
...     ]
... )
>>> print(myac.matching("art"))
['article', 'artist']
>>> print(myac.matching(""))
[
    'art', 'article', 'artist',
    'bar', 'barber', 'barbie',
    'when', 'whendy', 'who'
]
>>> print(myac.missing("art", 'article'))
icle
```

The class ``AutoComplete`` builds a special "magical" dictionary which is stored
in the attribut ``self.assos`` that you can store somewhere, using ``pickle``
for example, so as to not build each time the same auto-completions. Here is an
example where the output has been enhanced and commented a little.

```python
>>> from mistool.string_use import AutoComplete
>>> myac = AutoComplete(
...     words = [
...         "article", "artist", "art",
...         "when", "who", "whendy",
...         "bar", "barbie", "barber", "bar"
...     ]
... )
>>> print(myac.assos)
{
    'words': [
# A
        'art', 'article', 'artist',
# B
        'bar', 'barber', 'barbie',
# W
        'when', 'whendy', 'who'
    ],
    'prefixes': {
# A
        'a'     : [0, 3],   # words in position 0 to 2 starts with "a"
        'ar'    : [0, 3],
        'art'   : [1, 3],   # "art" has not to be completed !
        'arti'  : [1, 3],
        'artic' : [1, 2],
        'artis' : [2, 3],   # "artist" has not to be completed
        'articl': [1, 2],   # so it is not a prefix like "artcile".
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
```

```python
>>> from mistool.string_use import AutoComplete
>>> myac = AutoComplete(
...     words = [
...         "article", "artist", "art",
...         "when", "who", "whendy",
...         "bar", "barbie", "barber", "bar"
...     ],
...     minsize = 3
... )
>>> print(myac.assos)
{
    'words': [
        'art', 'article', 'artist',
        'bar', 'barber', 'barbie',
        'when', 'whendy', 'who'
    ],
    'prefixes': {
# A
        'art'   : [1, 3],
        'arti'  : [1, 3],
        'artic' : [1, 2],
        'articl': [1, 2],
        'artis' : [2, 3],
# B
        'bar'  : [4, 6],
        'barb' : [4, 6],
        'barbe': [4, 5],
        'barbi': [5, 6],
# W
        'whe'  : [6, 8],
        'when' : [7, 8]
        'whend': [7, 8],
    }
}
```

You can directly give the dictionary stored in ``self.assos`` like in the
following fictive example where you can see the instance ``newoldac`` stores
no words, and that there is no matching for ``"a"`` because the magic dictionary
uses a depth of `3`.

```python
>>> oldassos = myac.assos
>>> newoldac = AutoComplete(assos = myac.assos)
>>> print(newoldac.matching("art"))
['article', 'artist']
>>> print(newoldac.matching("a"))
[]
>>> print(newoldac.words)
None
```

This can be very useful when you always use the same list of words : just ask
one time to the class to build the "magical" dictionary by giving one fixed
list of words just one time, and then store this dictionary to reuse it later.

Replace
-------

```python
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
```

```python
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
>>> mreplace.mode = "norecu"
>>> print(mreplace("W1 and W2 = W3"))
Word #1 and Word #2 = W1 and W2
```

```python
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
```

Split
-----

```python
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
```

```python
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

```

Escaping separators


```python
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
```

```python
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
None
```

Join
----

```python
>>> from mistool.string_use import joinand
>>> texts = ["1", "2", "3"]
>>> print(joinand(texts))
1, 2 and 3
>>> andtext_fr = "et"
>>> print(joinand(texts = texts, andtext= andtext_fr))
1, 2 et 3
```


ASCII translation
---------------

```python
>>> from mistool.string_use import isascii
>>> print(isascii("Vive la France !"))
True
>>> print(isascii("¡Viva España!"))
False
```

```python
>>> from mistool.string_use import ascii
>>> print(ascii("¡Viva España!"))
Viva Espana!
```

```python
>>> from mistool.string_use import ascii
>>> oldnew = {'!': ""}
>>> print(ascii(text = "¡Viva España!", oldnew = oldnew))
Viva Espana
```

```python
>>> from mistool.string_use import ascii
>>> print(ascii(text = "L'Odyssée de ∏", strict = False))
L'Odyssee de ∏
>>> print(ascii("L'Odyssée de ∏"))
Traceback (most recent call last):
[...]
ValueError: ASCII conversion can't be made because of the character << ∏ >>.
You can use the function ``_ascii_report`` so as to report more precisely
this fealure with eventually an ascii alternative.
```


Playing with cases of letters
-----------------------------

```python
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
```


```python
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
```

```python
iscase(text, kind)
```


Features of the module ``date_use``
=======================

Translating dates
-----------------

```python
>>> import datetime
>>> from mistool.date_use import translate
>>> onedate   = datetime.date(2015, 6, 2)
>>> oneformat = "%A %d %B %Y"
>>> print(translate(date = onedate, strformat = oneformat))
Tuesday 02 June 2015
>>> print(translate(date = onedate, strformat = oneformat, lang = "fr_FR"))
Mardi 02 juin 2015
```

Next day having a fixed english name
-----------------

```python
>>> from datetime import datetime
>>> from mistool.date_use import nextday

>>> onedate = datetime.strptime("2013-11-30", "%Y-%m-%d")
>>> print(onedate.strftime("%Y-%m-%d is a %A"))
2013-11-30 is a Saturday

>>> nextsunday = nextday(date = onedate, name = "sunday")
>>> print("Next Sunday:", nextsunday.strftime("%Y-%m-%d"))
Next Sunday: 2013-12-01
```


Features of the module ``url_use``
======================

Testing urls so as to look for dead links
----

```python
>>> from mistool.url_use import islinked
>>> islinked("http://www.google.com")
True
>>> islinked("http://www.g-o-o-g-l-e.com")
False
```

Escaping in urls the special characters
----

```python
>>> from mistool.url_use import escape
>>> print(escape("http://www.vivaespaña.com/camión/"))
http://www.vivaespa%C3%B1a.com/cami%C3%B3n/
```


??? Features of the module ``os_use``
=====================

* **Testing paths** so as to know if they point to one file, or one directory.
* **Extract informations from paths** like the name of a file with or without the extension, or the path of the parent parent directory...
* **Reading and building text files** very easily.
* **Opening a file with its associated default application** from a Python code.
* **Moving, copying and deleting** files.
* **Cleaning directories** with a fine tuning.
* **Listing the content of one directory** with fine tuning.
* **ASCII tree view of one directory**.
* **System** used and **environment's path**.


Features of the module ``term_use``
=========================

Step
------

```python
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
```

```python
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
```

```python
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
```

Frame
-----

```python
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
```

```python
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
```

```python
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
```

```python
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
```

Just take a look at the documentation of the function ``buildframe`` that allows
to build very easily a "frame" dictionary that can be used with ``withframe``.


DirView
---

All of the following examples will use a folder with the structure above and
having the whole path path::``/Users/projetmbc/dir``.

```
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
```


```python
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
```

```python
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
```

Let's see a last example using the argument ``regpath``. The following code
asks to keep only the files with the extension path::``py``. You can see that
the empty folders are given, and that the other files than the ones wanted are
indicated by ellipsis, this ones being always sorted at the end of the files.

```python
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
```


```python
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
```

The documentation of the function ``_ppath_regpath2meta`` gives all the
¨infos needed to use the regpaths.



aussi possible d'avoir ``dirview.tree``


```python
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
```


``dirview.toc``

```python
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
```


``dirview.latex`` you will have the following ¨latex code
than can be formated by the ¨latex package latex::``dirtree``.




```python
???
```

Features of the module ``python_use``
=========================

Easy quoted text with the least escaped quote symbols
------

```python
???>>> from mistool.python_use import quote
>>> print(quote('First example.'))
'First example.'
>>> print(quote("Same example."))
'Same example.'
>>> print(quote('One "small" example.'))
'One "small" example.'
>>> print(quote("The same kind of 'example'."))
"The same kind of 'example'."
>>> print(quote("An example a 'little' more \"problematic\"."))
'An example a \'little\' more "problematic".'
```


List of single values of a dictionary
----

```python
>>> from mistool.python_use import dictvalues
>>> onedict = {"a": 1, "b": 2, "c": 1}
>>> print(dictvalues(onedict))
[1, 2]
>>> print(list(onedict.values()))
[2, 1, 1]
```

??? Features of the module ``latex_use``
========================

* Easy **compilation** of LaTeX files.

```python
???
```

* **Removing the temporary files** produced by LaTeX during one compilation.

```python
???
```

* **Automatic installation** of personal LaTeX packages.

```python
???
```

* Crucial **informations about your LaTeX distribution**.

```python
???
```

* **Escaping** the special characters used by the LaTeX syntax.

```python
???
```
