#!/usr/bin/env python3

# The following lines were automatically build.

# ------------------- #
# -- LINE COMMANDS -- #
# ------------------- #

#    1) Local installation :
#         python3 setup.py install
#
#    2) Registering :
#         python3 setup.py register
#
#    3) Uploading the code on Pypi :
#         python3 setup.py sdist upload


# ---------------- #
# -- META-DATAS -- #
# ---------------- #

#     1) http://docs.python.org/3.0/distutils/setupscript.html#additional-meta-data
#     2) https://pypi.python.org/pypi?%3Aaction=list_classifiers


# ----------- #
# -- INFOS -- #
# ----------- #

#    1) http://wiki.python.org/moin/Distutils/Tutorial
#    2) http://www.developpez.net/forums/d1195941/autres-langages/python-zope/general-python/ajout-module-distribution-python/#post6555422
#    3) http://docs.python.org/distutils/sourcedist.html
#    4) http://www.developpez.net/forums/d1208929/autres-langages/python-zope/general-python/distutils-exclure-inclure-dossier-fichier-lors-setup/#post6619447


from distutils.core import setup

longdesc = """
**misTool** is a contraction of **missing**, **miscellaneous** and **tool**. This package contains the following modules that could be useful for Python developments.

If you want more informations and examples than thereafter, just take a look at the docstrings.


.. contents:: Table of Contents


Fork me on GitHub
=================

This project is hosted by the website `GitHub <https://github.com>`_. Just go to `this page <https://github.com/projetmbc/mistool>`_.


Which OS can use this program ?
===============================

All the modules have been tested under Mac OS Maverick and Lubuntu 14.


The module ``string_use``
=========================

* **Auto completion** features easily.
* **Replacement, split and join** advanced utilities.
* **ASCII translation** of a text.
* **Special cases for letters** so as to obtain for example easily "One example" from "one example".
* **Testing the case of one text**.
* **Camel case** transformations so as to obtain for example "One_Example" from "oneExample".
* **ASCII frame** for multiline texts.


The module ``date_use``
=======================

* **Translating dates**.
* **Next day** having a fixed name.


The module ``url_use``
======================

* **Testing urls** so as to look for dead links.
* **Escaping in urls** the special characters.


The module ``latex_use``
========================

* Easy **compilation** of LaTeX files.
* **Removing the temporary files** produced by LaTeX during one compilation.
* **Automatic installation** of personal LaTeX packages.
* Crucial **informations about your LaTeX distribution**.
* **Escaping** the special characters used by the LaTeX syntax.


The module ``os_use``
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


The module ``log_test_use``
===========================

* **Launching test suite with unittest** very easily in a directory (all you need is to follow some very simple rules for naming testing files and classes).
* **Special formatting** for logging during tests.
* **Differences between two dictionaries** given in a string format.


The module ``python_use``
=========================

* **Launching several Python files** easily.
* **Easy quoted text** with the least escaped quote symbols.
* **List of single values of a dictionary**.


Log of the last main changes
============================

Only the major changes are in english. You can find all of them in the directory ``change_log/en``.

If you want to know every changes, even the minor ones, there are in the directory ``change_log/fr`` but all of this is only in french.


2014-08-31
----------

**Some improvements !** Here's what to discover.

1. In the module ``python_use``, the new function ``runpys`` lets you launch different Python files using certain criteria related to the paths of the scripts to run.

2. In the modules ``os_use``, the functions ``listfile`` and ``nextfile``, and also the class ``DirView`` have a new boolean argument ``unkeephidden`` so as to skip the hidden files and/or the hidden folders whose names usually begin with a period.

3. In the module ``string_use``, to indicate several types of cases to the functions ``case`` and ``camelto``, it will be enough to simply separate these different formats using spaces.


**One bug fixed in the function ``about`` of the module ``latex_use``:** an error was raised in the case of a non-standard installation of LaTeX (bug discovered under Lubuntu 14 with a TeX Live  distribution installed by hand). This type of installation is not supported at this time (but this is on the list of things to do).


**One pseudo bug fixed in the module ``os_use``:** unlike what happens in Mac O$, under Lubuntu, folder paths returned by the standard function ``os.listdir`` do not appear in a logical order. This made impossible the practical use of the function ``listdir`` and class ``DirView`` (because it did not refer to standard output). This has been corrected.


**Fork misTool on GitHub:** the project is now managed via Git and hosted on the website GitHub.


2014-08-27
----------

**Disappearance of certain features:** the author of misTool has started a new project lexTex. This implies that the functionalities below will no longer be in the module misTool.

* The module ``parse_use``, and also the associated files ``config/group.py``, ``config/pattern.py`` and ``config/token.py`` have been deleted.

* In the file ``config/pattern.py``, the constants ``PATTERN_VAR_NAME``, ``PATTERN_ROMAN_NUMERAL`` and ``PATTERN_NATURAL`` have been removed.

* In the module ``string_use``, the function ``wrap`` has been deleted.

* In the module ``python_use``, the functions ``pyRepr`` and ``lambdify`` have been deleted.


**Deep renamings in the code:** for the remaining modules, many things have been renamed in order to stick to more coherent, but also easier to use, internal specifications. Here are all the changes. Sorry for all this mess! :-)


Let's start with everything concerning **the dates**.

+ In ``date_use.py``, it just has the following modifications.
    * The constant ``LANG`` becomes ``DEFAULT_LANG``.
    * The function ``nextDay`` becomes ``nextday``.

+ In ``config/date_name.py``, we have the following modifications.
    * The constant ``__ALL_LANGS`` becomes ``LANGS``.
    * The constant ``__POINTERS`` becomes ``_POINTERS``.
    * The constant ``__FORMAT_TRANSLATIONS`` becomes ``_FORMATS_TRANSLATIONS``.


Regarding **the latex utilities**, here is what to remember.

+ In ``latex_use.py``, we have the following modifications.
    * The function ``makeMiktexLocalDir`` becomes ``make_localdir_miktex``.
    * The function ``mikeTexLocalDir`` becomes ``localdir_miketex``.
    * In the function ``install``, we have the following modification.
        - The argument ``listFile`` becomes ``paths``.
    * In the class ``Build`` and the function ``clean``, we have the following modification.
        - The argument ``verbose`` becomes ``isverbose``.

+ In ``config/latex.py``, we have the following modifications.
    * The constant ``CLASSIFIED_TEMP_EXT`` becomes ``TEMP_EXTS``.
    * The constant ``ALL_EXT_TO_CLEAN`` becomes ``EXTS_TO_CLEAN``.
    * The constant ``CHAR_TO_ESCAPE`` becomes ``CHARS_TO_ESCAPE``.
    * The constant ``CHAR_TO_LATEXIFY`` becomes ``CHARS_TO_LATEXIFY``.


Regarding **the module ``log_test_use.py``**, here is what has changed.

+ In ``log_test_use.py``, we have the following modifications.
    * The constant ``ASCII_ASSO`` becomes ``ASCII_ASSOS``.
    * The function ``diffDict`` becomes ``diffdict``. For this function we have the following modification.
        - The argument ``recursive`` becomes ``dorecursive``.
    * The function ``launchTestSuite`` becomes ``runtests``.
    * The function ``logPrint`` becomes ``logprint``.
    * In the function ``what``, we have the following modification.
        - The argument ``isMethod`` becomes ``ismethod``.


For **the module ``os_use``**, you have to pay attention to the following things.

+ In ``os_use.py``, we have the following modifications.
    * In the function ``clean``, we have the following modification.
        - The argument ``ext`` becomes ``exts``.
    * The function ``commonPath`` becomes ``commonpath``.
    * The function ``fileName`` becomes ``filename``.
    * The function ``hasExtIn`` becomes ``hasextin``. For this function we have the following modification.
        - The argument ``listOfExt`` becomes ``exts``.
    * The function ``isDir`` becomes ``isdir``.
    * The function ``isFile`` becomes ``isfile``.
    * The function ``listDir`` becomes ``listdir``.
    * The function ``listFile`` becomes ``listfile``. For this function we have the following modifications.
        - The argument ``keepDir`` becomes ``keepdir``.
        - The argument ``ext`` becomes ``exts``.
        - The argument ``prefix`` becomes ``prefixes``.
    * The function ``makeDir`` becomes ``makedir``.
    * The function ``makeTextFile`` becomes ``maketxtfile``.
    * The function ``nextDir`` becomes ``nextdir``.
    * The function ``nextFile`` becomes ``nextfile``. For this function we have the following modifications.
        - The argument ``keepDir`` becomes ``keepdir``.
        - The argument ``ext`` becomes ``exts``.
        - The argument ``prefix`` becomes ``prefixes``.
    * The function ``parentDir`` becomes ``parentdir``.
    * The function ``pathEnv`` becomes ``pathenv``.
    * The function ``pathNoExt`` becomes ``noext``.
    * The function ``realPath`` becomes ``realpath``.
    * The function ``readTextFile`` becomes ``readtxtfile``.
    * The function ``relativeDepth`` becomes ``relativedepth``.
    * The function ``relativePath`` becomes ``relativepath``.
    * In the class ``DirView``, we have the following modifications.
        - The constant of class ``ASCII_DECORATION`` becomes ``ASCII_DECOS``.
        - The argument ``ext`` becomes ``exts``.
        - The argument ``prefix`` becomes ``prefixes``.
        - The argument ``seeMain`` becomes ``seemain``.
        - The attribute ``listView`` becomes ``listview``.
        - The method ``pathToDisplay`` becomes ``pathtodisplay``.


The tools related to **python** are only concerned with one change.

+ In ``python_use.py``, we have the following modification.
    * The function ``dictSingleValues​​`` becomes ``dictvalues``.


Finally, for **string manipulations**, here is what has changed.

+ In ``string_use.py``, we have the following modifications.
    * In the function ``ascii``, we have the following modification.
        - The argument ``replacement`` becomes ``replacements``.
    * The function ``beforeAfter`` becomes ``between``.
    * The function ``camelTo`` becomes ``camelto``.
    * The function ``isAscii`` becomes ``isascii``.
    * The function ``isCase`` becomes ``iscase``.
    * The function ``joinAnd`` becomes ``joinand``. For this function we have the following modification.
        - The argument ``andText`` becomes ``andtext``.
    * In the function ``replace``, we have the following modification.
        - The argument ``replacement`` becomes ``replacements``.
    * In the function ``split``, we have the following modification.
        - The argument ``sep`` becomes ``seps``.
    * In the class ``AutoComplete``, we have the following modification.
        - The argument ``dictAsso`` becomes ``assos``.
    * In the class ``MultiReplace``, we have the following modifications.
        - The argument ``replacement`` becomes ``replacements``.
        - The attribute ``replacementasit`` becomes ``replaceasit``.
    * In the class ``MultiSplit``, we have the following modifications.
        - The argument ``sep`` becomes ``seps``.
        - The attribute ``listView`` becomes ``listview``.

+ In ``config/frame.py``, we have the following modifications.
    * The constant ``_ABREV_FRAME`` becomes ``_ABREVS_FRAMES``.
    * The constant ``_KEY_FRAME`` becomes ``_KEYS_FRAMES``.
    * The constant ``FRAME_FORMATS`` becomes ``FRAMES_FORMATS``.

+ In ``config/pattern.py``, we have the following modification.
    * The constant ``PATTERN_GROUP_WORD`` becomes ``PATTERNS_WORDS``.


2013-03-17
----------

First downloadable version of the package.
""".strip()

setup(
    name = "mistool",
    version = "1.2014.8.31",
    author = "Christophe BAL",
    author_email = "projetmbc@gmail.com",
    url = "https://github.com/projetmbc/mistool",
    download_url = "https://pypi.python.org/pypi",
    packages = ['mistool', 'mistool.config'],
    package_dir = {'mistool': 'mistool'},
    package_data = {'mistool': ['change_log/*/*/*.txt']},
    classifiers = ['Development Status :: 5 - Production/Stable', 'Development Status :: 5 - Production/Stable', 'Intended Audience :: Developers', 'License :: OSI Approved :: GNU General Public License (GPL)', 'Programming Language :: Python :: 3', 'Operating System :: MacOS', 'Operating System :: Microsoft :: Windows', 'Operating System :: POSIX :: Linux', 'Topic :: Utilities', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Software Development :: Testing', 'Topic :: Desktop Environment :: File Managers', 'Topic :: Software Development :: Code Generators', 'Topic :: System :: Logging', 'Topic :: Text Processing :: Markup :: LaTeX'],
    description = "Miscellaneous missing tools that can help the py-developper.",
    long_description = longdesc,
)
