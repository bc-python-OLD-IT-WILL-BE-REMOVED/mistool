**misTool** is a contraction of **missing**, **miscellaneous** and **tool**. This package contains the following modules that could be useful for Python developments.

If you want more informations and examples than thereafter, just take a look at the docstrings.


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

2. In the modules ``os_use``, the functions ``listfile`` and ``nextfile``, and also the class ``DirView`` have a new boolean argument ``unkeephidden`` so as to skip the files and/or the hidden folders whose names usually begin with a period.

3. In the module ``string_use``, to indicate several types of cases to the functions ``case`` and ``camelto``, it will be enough to simply separate these different formats using spaces.


**One bug fixed in the function ``about`` of the module ``latex_use``:** an error was raised in the case of a non-standard installation of LaTeX (bug discovered under Lubuntu 14 with a TeX Live  distribution installed by hand). This type of installation is not supported at this time (but this is on the list of things to do).


**One pseudo bug fixed in the module ``os_use``:** unlike what happens in Mac O$, under Lubuntu, folder paths returned by the standard function ``os.listdir`` do not appear in a logical order. This made impossible the practical use of the function ``listdir`` and class ``DirView`` (because it did not refer to standard output). This has been corrected.


**Fork misTool on GitHub:** the project is now managed via Git and hosted on the website GitHub.
