#!/usr/bin/env python3

from collections import OrderedDict

# Note: the following variables were automatically built.

TEMP_EXTS = OrderedDict([
    ('debug', ['blg', 'ilg', 'log', 'glg']),
    ('html', ['4ct', '4tc', 'idv', 'lg', 'tmp', 'xref']),
    ('slide', ['nav', 'snm', 'vrb']),
    ('editor', ['synctex.gz', 'synctex.gz(busy)', 'synctex(busy)']),
    ('float', ['fff', 'ttt']),
    ('list', ['lof', 'lol', 'lot', 'bcl']),
    ('toc', ['toc', 'maf', 'mlf', 'mlt', 'mtc', 'plf', 'plt', 'ptc']),
    ('ref', ['aux', 'brf', 'out', 'glo', 'ist', 'gls', 'idx', 'ind', 'xdy']),
    ('biblio', ['bbl', 'run.xml']),
    ('listings', ['listing']),
    ('theorem', ['thm']),
    ('misc', ['fdb_latexmk', 'fls'])
])

EXTS_TO_CLEAN = [
# debug
#
# ``log`` is produced by latex compilations, ``ilg`` and ``glg`` by
# makeindex compilations, where ``glg`` is related to the package glossary.
# ``blg`` is produced by bibtex compilations.
# 
# 
    'blg', 'ilg', 'log', 'glg',
# html
#
# This extensions are produced by the package ``tex4ht``.
# 
# 
    '4ct', '4tc', 'idv', 'lg', 'tmp', 'xref',
# slide
    'nav', 'snm', 'vrb',
# editor
#
# ``synctex.gz`` is produced by some editors to do synchronization between
# the LaTeX source file and its PDF output.
# 
# 
    'synctex.gz', 'synctex.gz(busy)', 'synctex(busy)',
# float
    'fff', 'ttt',
# list
#
# ``bcl`` is produced by the package ``bclogo`` : this gives the list of
# the logos.
# 
# ``f`` is for Figure, ``l`` for Listing (cf. the package ``listings``),
# and ``t`` for Table.
# 
# 
    'lof', 'lol', 'lot', 'bcl',
# toc
#
# The package ``minitoc`` produces all this extensions excepted ``toc``.
# 
# 
    'toc', 'maf', 'mlf', 'mlt', 'mtc', 'plf', 'plt', 'ptc',
# ref
#
# ``out`` is produced by the package ``hyperref`` with the option
# ``bookmarks``, and ``brf`` with the option ``backref``.
# 
# The package ``glossary`` produces ``glo`` and ``gls``, and also ``ist``
# if an additional makeindex compilation is launched.
# 
# ``idx`` and ``ind`` are produced by makeindex compilations.
# 
# ``xdy`` is produced by the package glossary.
# 
# 
    'aux', 'brf', 'out', 'glo', 'ist', 'gls', 'idx', 'ind', 'xdy',
# biblio
#
# ``bbl`` is produces by bibtex compilations, and ``run.xml`` by biber
# compilations.
# 
# 
    'bbl', 'run.xml',
# listings
#
# The package ``tcolorbox`` produces ``listing`` when the macros ``tcblisting`` is used.
# 
# 
    'listing',
# theorem
    'thm',
# misc
    'fdb_latexmk', 'fls'
]

# Sources :
#    * The page 7 in "The Comprehensive LATEX Symbol List" of Scott Pakin.
#    * http://www.grappa.univ-lille3.fr/FAQ-LaTeX/21.26.html

CHARS_TO_ESCAPE = {
    'text': "{}_$&%#",
    'math': "{}_$&%#" 
}

CHARS_TO_LATEXIFY = {
    'text': {
        '\\': "\\textbackslash{}"
    },
    'math': {
        '\\': "\\backslash{}"
    }
}
