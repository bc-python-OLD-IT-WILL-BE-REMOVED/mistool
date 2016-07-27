What about this package  ?
==========================

**misTool** is the contraction of **missing**, **miscellaneous** and **tool(s)**.
This package contains some modules that could be useful for Python
developments.

***If you want more informations and examples than thereafter, just take
a look at the docstrings.***


I beg your pardon for my english...
===================================

English is not my native language, so be nice if you notice misunderstandings, misspellings or grammatical errors in my documents and codes.


Warning about this new version `1.0.0-beta`
===========================================

This version breaks a lot of things regarding to the previous ones *(for
example, the module ``log_test_use`` has been removed and a new module
``term_use`` has been added)*. See the change log for more informations.


The module ``os_use``
=====================

Changing the working directory for commands
-------------------------------------------

With ``os_use.cd``, you have a context which changes temporarily the directory where launching terminal like commands. When the context is closed, the working directory goes back to the one just before the call of ``os_use.cd``.

Let's see an example. We suppose that we have the following directory with the absolute path ``/Users/projetmbc/basic_dir`` in a Unix system.

```
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
```


The following code first goes inside ``/Users/projetmbc/basic_dir`` and then it moves to ``/Users/projetmbc/basic_dir/sub_dir``. With ``subprocess.call("ls")``, we simply use the Unix command ``ls`` so as to list files and folders inside the current working directory.

```python
>>> import subprocess
>>> from mistool.os_use import cd
>>> with cd("/Users/projetmbc/basic_dir"):
...     subprocess.call("ls")
empty_dir	python_1.py	python_4.py	text_2.txt
latex_1.tex	python_2.py	sub_dir		text_3.txt
latex_2.tex	python_3.py	text_1.txt
>>> with cd("/Users/projetmbc/basic_dir/sub_dir"):
...     subprocess.call("ls")
code_A.py	slide_A.pdf	sub_sub_dir
code_B.py	slide_B.pdf
```


Launching commands like in a terminal
-------------------------------------

The aim of the function ``os_use.runthis`` is to simplify  a lot the launching of subprocesses *(just use commands as you were inside your terminal)*. Let's consider the basic following Python script with absolute path ``/Users/projetmbc/script.py``.

```python
print("Everything is ok.")
```

To launch this program, we just have to use the single string Unix command ``python3 /Users/projetmbc/script.py`` like in the following lines. You can see that by default nothing is printed, so you have to use ``showoutput = True`` if
you want to see what the script launched prints.

```python
>>> from mistool.os_use import PPath, runthis
>>> pyfile = PPath("/Users/projetmbc/script.py")
>>> runthis(cmd = "python3 {0}".format(ppath))
>>> runthis(cmd = "python3 {0}".format(ppath), showoutput = True)
Everything is ok.
```


System used and environment's path
----------------------------------

The call to ``os_use.system()`` returns the name, in lower case, of the OS used : possible strings returned can be for example ``"windows"``, ``"mac"``, ``"linux"`` and also ``"java"``.


``os_use.pathenv()`` gives you the paths of executables known by your OS *(this is indeed an alias for ``os.getenv('PATH')``)*.


Enhanced version of the class ``pathlib.Path``
----------------------------------------------

The class ``os_use.PPath`` adds several methods to the useful class ``pathlib.Path``. Here are examples.


### Informations about one path

The following code shows additional informations given by the class ``os_use.PPath``.

```python
>>> from mistool.os_use import PPath
>>> path = PPath("dir/subdir/file.txt")
>>> path.parent
PPath('dir/subdir')
>>> print(path.depth)
2
>>> print(path.ext)
'txt'
```


Another useful method named ``is_protected`` works as explained below.

1. If the path does not point to an existing file or folder, an OS error is raised.

1. If the path is the one of a folder, the answer returned is ``True`` for a modifiable directory and ``False`` otherwise.

1. Finally if the path points to a file, then that is its parent folder which is tested.


There is also the method ``is_empty`` which can give three different responses.

1. If the path is the one of an empty directory, ``False`` is
returned.

1. ``True`` is returned when the path corresponds to an non-empty folder.

1. If the path doesn't point to an existing directory an OS error is raised.


### Changing one path

Changing or adding an extension is very easy with the method ``with_ext``.

```python
>>> from mistool.os_use import PPath
>>> path_no_ext = PPath("dir/subdir")
>>> path_no_ext.with_ext("ext")
PPath('dir/subdir.ext')
>>> path_ext = PPath("dir/subdir/file.txt")
>>> path_ext.with_ext("ext")
PPath('dir/subdir/file.ext')
```


Obtaining a short version or a normalized one of a path needs no effort. Here is how to do that *(``~`` is a shortcut for the main OS user's folder)*.

```python
>>> from mistool.os_use import PPath
>>> path_too_long = PPath("~/dir_1/dir_2/dir_3/../../file.txt")
>>> path_too_long.normpath
PPath('/Users/projetmbc/dir_1/file.txt')
>>> path_long = PPath("/Users/projetmbc/dir_1/dir_2/dir_3/../../file.txt")
>>> path_long.shortpath
PPath('~/dir_1/file.txt')
```


### Comparing paths

The "common" folder of several paths is obtained by using the method ``common_with`` or equivalently the magic operator ``&``.

```python
>>> from mistool.os_use import PPath
>>> path        = PPath("/Users/projetmbc/source/doc")
>>> path_1      = PPath("/Users/projetmbc/README")
>>> path_2      = PPath("/Users/projetmbc/source/misTool/os_use.py")
>>> path_danger = PPath("/NoUser/projects")
>>> path.common_with(path_1)           # Same as ``path & path_1``
PPath('/Users/projetmbc')
>>> path.common_with(path_2)           # Same as ``path & path_2``
PPath('/Users/projetmbc/source')
>>> path.common_with(path_danger)      # No error raised !
PPath('/')
>>> path.common_with(path_1, path_2)   # Same as ``path & path_1 & path_2``
PPath('/Users/projetmbc')
>>> path.common_with([path_1, path_2]) # Same as ``path & [path_1, path_2]``
PPath('/Users/projetmbc')
```


The class ``os_use.PPath`` adds a magic method so as to use ``path - anotherpath`` instead of ``path.relative_to(anotherpath)`` where the method ``relative_to`` is implemented by the class ``pathlib.Path``.

```python
>>> from mistool.os_use import PPath
>>> main    = PPath("/Users/projetmbc")
>>> path_1  = PPath("/Users/projetmbc/README")
>>> path_2  = PPath("/Users/projetmbc/source/misTool/os_use.py")
>>> path_1 - main
PPath('README')
>>> path_2 - main
PPath('source/misTool/os_use.py')
>>> path_2 - path_1
Traceback (most recent call last):
[...]
ValueError: '/Users/projetmbc/source/misTool/os_use.py' does not start with '/Users/projetmbc/README'
```


If you need to know the depth of one path relatively to another, just call the method ``depth_in``.

```python
>>> from mistool.os_use import PPath
>>> main    = PPath("/Users/projetmbc")
>>> path_1  = PPath("/Users/projetmbc/README")
>>> path_2  = PPath("/Users/projetmbc/source/misTool/os_use.py")
>>> path_pb = PPath("/NoUser/projects")
>>> print(path_1.depth_in(main))
0
>>> print(path_2.depth_in(main))
2
>>> print(path_pb.depth_in(main))
Traceback (most recent call last):
[...]
ValueError: '/NoUser/projects' does not start with '/Users/projetmbc'
```

### The special concept of "regpath"

A "regpath" is a query mixing all the power of regexes and the Unix-glob special characters  *(there are also some additional query
features)*. We will use some "regpaths" in the incoming examples.

**See the docstring of the method ``regpath2meta`` for complete informations about the "regpaths".**


### Walk and see

The method ``see`` **tries** to open the current path with a possible associated application. For example, an HTML file will be opened by your default browser.


You can walk very easily inside a directory thanks to the method ``walk`` and the "regpaths" *(see the previous section)*. For example, let's suppose that we have the following directory with absolute path
``/Users/projetmbc/basic_dir`` in a Unix system.

```
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
```


Here are easy to understand examples where the regpath ``"*"`` is for a
non-recursive search contrary to the regpath ``"**"``.

```python
>>> from mistool.os_use import PPath
>>> folder = PPath("/Users/projetmbc/basic_dir")
>>> for p in folder.walk("dir::**"):
...     print("+", p)
...
+ /Users/projetmbc/basic_dir/empty_dir
+ /Users/projetmbc/basic_dir/sub_dir
+ /Users/projetmbc/basic_dir/sub_dir/sub_sub_dir
>>> for p in folder.walk("file::**.py"):
...     print("+", p)
...
+ /Users/projetmbc/basic_dir/python_1.py
+ /Users/projetmbc/basic_dir/python_2.py
+ /Users/projetmbc/basic_dir/python_3.py
+ /Users/projetmbc/basic_dir/python_4.py
+ /Users/projetmbc/basic_dir/sub_dir/code_A.py
+ /Users/projetmbc/basic_dir/sub_dir/code_B.py
>>> for p in folder.walk("file::*.py"):
...     print("+", p)
...
+ /Users/projetmbc/basic_dir/python_1.py
+ /Users/projetmbc/basic_dir/python_2.py
+ /Users/projetmbc/basic_dir/python_3.py
+ /Users/projetmbc/basic_dir/python_4.py
```


### Create

Creating files and folders is straight forward with the method ``create`` even if this needs to add several parent directories that don't yet exist. In the following example, we suppose that the current directory has absolute path ``/Users/projetmbc``, and doesn't contain any subfolder.

```python
>>> from mistool.os_use import PPath
>>> path_1 = PPath("test/README")
>>> path_1.is_file()
False
>>> path_1.create("file")
>>> path_1.is_file()
True
>>> path_2 = PPath("test/README")
>>> path_2.create("dir")
Traceback (most recent call last):
[...]
ValueError: path points to an existing file.
```


### Remove

If you want to destroy a whole directory, or simply a file, given by its ``PPath``, just use the method ``remove``.


**Warning ! Because removing a file or a directory can be a dangerous thing, you can use the method ``can_be_removed`` which by default will raise an OS error if the ``PPath`` is one of an existing file or folder.**


The method ``clean`` allows to remove specific files and/or directories matching a regpath given as an argument.


### Move & copy

By default, the method ``copy_to`` allows you to copy a file or a directory into another location, whereas the method ``move_to`` will move a file or a directory to another place.


The module ``string_use``
=========================

Multi-replacements
------------------

The class ``string_use.MultiReplace`` makes possible to do multi-replacements recursively or not *(by default ``mode = "norecu"``)*.

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
>>> mreplace.build()
>>> print(mreplace("W1 and W2 = W3"))
Word #1 and Word #2 = W1 and W2
```

The code above show that cyclic definitions will raise a ``ValueError`` exception.

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
	 + WRONG_2 --> WRONG_3 --> WRONG_1 --> WRONG_2
```


Multi-splits
------------

The aim of the class ``string_use.MultiSplit`` is to split a text on several semantic depths. Here is an example of use.

```python
>>> from mistool.string_use import MultiSplit
>>> msplit = MultiSplit(seps = "|")
>>> print(msplit("p_1 ; p_2 ; p_3 | r_1 ; r_2 | s"))
[
    'p_1 ; p_2 ; p_3 ',
    ' r_1 ; r_2 ',
	' s'
]
>>> msplit.seps  = ["|", ";"]
>>> msplit.strip = True
>>> print(msplit("p_1 ; p_2 ; p_3 | r_1 ; r_2 | s"))
[
    ['p_1', 'p_2', 'p_3'],
    ['r_1', 'r_2'],
    ['s']
]
```

Before, between and after
-------------------------

The function ``string_use.between`` looks for two separators such as to return the text before, between and after the first matching of this separators.
``None`` is returned if no matching has been found. Just take a look at a concrete example.

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

Join with a last special text
-----------------------------

You can join several strings with a special final separator as the examples above show.

```python
>>> from mistool.string_use import joinand
>>> texts = ["1", "2", "3"]
>>> print(joinand(texts))
1, 2 and 3
>>> print(joinand(texts = texts, andtext = "et"))
1, 2 et 3
>>> print(joinand(texts = texts, sep = " + ", andtext = "="))
1 + 2 = 3
```


Playing with cases of letters
-----------------------------

The function ``string_use.case`` gives more auto-formatting of strings *(the last formatting looks strange but it is useful for an incoming project of the author of ``mistool``)*.

```python
>>> from mistool.string_use import case
>>> text = "onE eXamPLe"
>>> for kind in ['lower', 'upper', 'sentence', 'title', 'firstlast']:
...     print("{0}  [{1}]".format(case(text, kind), kind))
...
one example   [lower]
ONE EXAMPLE   [upper]
One example   [sentence]
One Example   [title]
One examplE   [firstlast]
```


A camel case string can be "uncamelized" by the function ``string_use.camelto``. Here is how to use it *(you can change the separator by using the optional argument ``sep`` which is ``"_"`` by default)*.

```python
>>> from mistool.string_use import camelto
>>> text = "OneSmallExampLE"
>>> for kind in ['lower', 'upper', 'sentence', 'title', 'firstlast']:
...     print("{0}  [{1}]".format(camelto(text, kind), kind))
...
one_small_examp_l_e   [lower]
ONE_SMALL_EXAMP_L_E   [upper]
One_small_examp_l_e   [sentence]
One_Small_Examp_L_E   [title]
One_small_examp_l_E   [firstlast]
```

If you need to check the case of a string, just use ``string_use.iscase(text, kind)``.


Playing with ASCII
------------------

You can check if a string is a pure ASCII one.

```python
>>> from mistool.string_use import isascii
>>> print(isascii("Vive la France !"))
True
>>> print(isascii("¡Viva España!"))
False
```


You can also transform a string to a pure ASCII one *(this will not always work but in case of failure you can contribute very easily to enhance ``string_use.ascii_it``)*.

```python
>>> from mistool.string_use import ascii_it
>>> print(ascii_it("¡Viva España!"))
Viva Espana!
>>> oldnew = {'!': ""}
>>> print(ascii_it(text = "¡Viva España!", oldnew = oldnew))
Viva Espana
```


The last example above shows how to be permissive : this means that ``string_use.ascii_it`` will "asciify" the most characters as possible.

```python
>>> from mistool.string_use import ascii_it
>>> print(ascii_it(text = "L'Odyssée de ∏", strict = False))
L'Odyssee de ∏
>>> print(ascii_it("L'Odyssée de ∏"))
Traceback (most recent call last):
[...]
ValueError: ASCII conversion can't be made because of the character << ∏ >>.
You can use the function ``_ascii_report`` so as to report more precisely
this fealure with eventually an ascii alternative.
```


Auto completion
---------------

The class ``string_use.AutoComplete`` gives the auto-completion feature accessible without using any GUI package.

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


It is a convention in GUI applications to give auto-completion only for at least three characters. You can do that by using the optional argument ``minsize`` which is ``1`` by default.


The module ``term_use``
=======================

Auto-numbering steps
--------------------

For terminal informations, it can be useful to number some important printed steps. This can be done easily with the class ``term_use.Step``.

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

The class ``term_use.Step`` has two optional arguments.

1. ``start`` gives the first number which is ``1`` by default.

2. ``textit`` is a function of two variables ``(n, t)`` returning the text containing the step number ``n`` and the text ``t``. By default, ``textit = lambda n, t: "{0}) {1}".format(n, t)``.


Frame
-----

The function ``term_use.withframe`` puts a text inside an ASCII frame *(you can choose the alignment and use other kinds of frames if necessary as it is explained in the docstrings)*.

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


ASCII tree views of one directory
---------------------------------

For our examples, we consider a folder with the following structure and the absolute path ``/Users/projetmbc/dir``.

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

The preceding ASCII tree view was built easily using the following code *(``PPath`` is the class defined in ``os_use`` added in ``term_use`` for you comfort)*.

```python
>>> from mistool.term_use import DirView, PPath
>>> dir     = PPath("/Users/projetmbc/dir")
>>> dirview = DirView(
...     ppath   = dir,
...     sorting = "filefirst"
... )
>>> print(dirview.ascii)
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


Using the "regpath" concept of the module ``os_use``, we can filter folders and files shown as in the example above *(we also use the argument ``display`` so as to customize the output)*.

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


You can also use the following property methods.

1. ``dirview.tree`` is a graphical tree.

1. ``dirview.toc`` gives a minimal tabulated tree.

1. ``dirview.latex`` is for the LaTeX package ``dirtree``.


The module ``python_use``
=========================

Easy quoted text with the least escaped quote symbols
-----------------------------------------------------

With ``python_use.quote`` you can add without pain quotes around a text.

```python
>>> from mistool.python_use import quote
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
-------------------------------------

If you need to list all the value of one dictionary, the function ``python_use.dictvalues`` is made for you.

```python
>>> from mistool.python_use import dictvalues
>>> onedict = {"a": 1, "b": 2, "c": 1}
>>> print(dictvalues(onedict))
[1, 2]
>>> print(list(onedict.values()))
[2, 1, 1]
```


The module ``date_use``
=======================

Translating dates
-----------------

The function ``date_use.translate`` translates safely and easily all the names in dates.

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
------------------------------------

In some applications you want to know the next monday after a fixing date. Here is how to do that.

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


The module ``url_use``
======================

Looking for dead or bad urls
----------------------------

For the following example, we suppose that we have a working internet connection.

```python
>>> from mistool.url_use import islinked
>>> islinked("http://www.google.com")
True
>>> islinked("http://www.g-o-o-g-l-e.com")
False
```

Escaping special characters in urls
-----------------------------------

It is safe to not use non-ASCII characters in a url. Here is one way to do that.

```python
>>> from mistool.url_use import escape
>>> print(escape("http://www.vivaespaña.com/camión/"))
http://www.vivaespa%C3%B1a.com/cami%C3%B3n/
```


The module ``latex_use``
========================

Escaping the special LaTeX characters
-------------------------------------

The function ``latex_use.escape`` will escape all special characters for you regarding the text or math mode.

```python
>>> from mistool.latex_use import escape
>>> onetext = "\OH/ & ..."
>>> print(escape(onetext))
\textbackslash{}OH/ \& ...
>>> print(escape(text = onetext, mode = "math"))
\backslash{}OH/ \& ...
```


Easy LaTeX compilation(s)
-------------------------

The class ``latex_use.Build`` compiles a LaTeX file for you *(for the moment only the PDF compilation is implemented)*. Let's consider the
following LaTeX file with the absolute path ``/Users/projetmbc/latex/file.tex``.

```latex
\documentclass[11pt, oneside]{article}

\begin{document}

\section{One little test}

One basic formula : $E = mc^2$.

\end{document}
```

In the following code, we call to the class ``term_use.DirView`` so as to show the new files made by LaTeX *(the ellipsis ``[...]``
indicates some lines not reproduced here)*.

```python
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
```

The PDF file has been build by LaTeX but there are also temporary ones. If you need several compilations, so as to build a table of content for example, just use the attribut-argument ``repeat``, and if you don't want to see the LaTeX ouput, just set the attribut-argument ``showinfos`` to ``False``.


Removing the temporary files produced by LaTeX
----------------------------------------------

We keep the same LaTeX example file. The function ``latex_use.clean`` cleans all unuseful temporary files when the compilation has been done.

```python
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
>>> clean(ppath = latexdir, showinfos = True)
* Cleaning for "/Users/projetmbc/latex/file.tex"
>>> print(DirView(latexdir.parent).ascii)
+ latex
    * file.pdf
    * file.tex
```


Automatic installation of personal LaTeX packages
-------------------------------------------------

Let's suppose that we have package named ``lyxam`` stored in a folder having the absolute path ``/Users/projetmbc/latex/lyxam`` and whose structure is the following one.

```
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
```

To install this package locally in your LaTeX distribution, just do like in the code above.

```python
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
```


Using the concept of "regpath" of the module ``os_use``, you can for example choose to not install all the ``TXT`` files.

```python
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
```


Remove a personal LaTeX packages
--------------------------------

Just use ``remove(name)`` where ``name`` is the name of a local LaTeX package.