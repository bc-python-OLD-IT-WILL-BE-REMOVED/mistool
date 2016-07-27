# ------------------------------------------------ #
# -- LINE COMMANDS FOR TWINE (which uses HTTPS) -- #
# ------------------------------------------------ #

# Source: https://pypi.python.org/pypi/twine

#     1) Create some distributions in the normal way:
#         > python setup.py sdist bdist_wheel
#
#     2) Register your project (if necessary):
#         > # One needs to be explicit here, globbing dist/* would fail.
#         > twine register dist/project_name-x.y.z.tar.gz
#         > twine register dist/mypkg-0.1-py2.py3-none-any.whl
#
#     3) Upload with twine:
#         > twine upload dist/*
#
#     Note : if you see the following error while uploading to PyPI, it
#     probably means you need to register (see step 2):
#         > HTTPError: 403 Client Error: You are not allowed to edit 'xyz'
#         package information


# -------------------- #
# -- STANDARD TOOLS -- #
# -------------------- #

from setuptools import setup, find_packages
from pathlib import Path


# ----------------- #
# -- README FILE -- #
# ----------------- #

readme = Path(__file__).parent / 'README.md'

with readme.open(encoding='utf-8') as f:
    longdesc = f.read()


# ----------------- #
# -- OUR SETTNGS -- #
# ----------------- #

setup(
# General
    name         = "mistool",
    version      = "1.0.0-beta",
    url          = 'https://github.com/bc-python-tools/mistool',
    license      = 'GPLv3',
    author       = "Christophe BAL",
    author_email = "projetmbc@gmail.com",

# Descritions
    description      = "Miscellaneous missing tools that can help the py-developper.",
    long_description = longdesc,

# What to add ?
    packages = find_packages(),

# Uggly classifiers
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Desktop Environment :: File Managers',
        'Topic :: System :: Logging',
        'Topic :: Text Processing :: Markup :: LaTeX'
    ],

# What does your project relate to?
    keywords = 'python latex os path string terminal tool',
)
