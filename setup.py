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
    version      = "1.0.0",
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
