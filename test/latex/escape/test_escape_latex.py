#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from pathlib import Path
from pytest import fixture

from orpyste.data import ReadBlock as READ


# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from mistool import latex_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = Path(__file__).parent

ESCAPE_FUNCTION = latex_use.escape


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'escape.txt',
    mode    = {"keyval:: =": ":default:"}
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove():
        THE_DATAS_FOR_TESTING.remove()

    request.addfinalizer(remove)


# ------------------- #
# -- GOOD ESCAPING -- #
# ------------------- #

def test_latex_use_escape(or_datas):
    tests = THE_DATAS_FOR_TESTING.flatdict(nosep = True)

    for name, datas in tests.items():
        source        = datas['source']
        escaped_texts = {}

        if 'text' in datas:
            escaped_texts['text'] = datas['text']
        else:
            escaped_texts['text'] = datas['both']

        if 'math' in datas:
            escaped_texts['math'] = datas['math']
        else:
            escaped_texts['math'] = datas['both']

        for mode in ['text', 'math']:
            answer = ESCAPE_FUNCTION(
                text = source,
                mode = mode
            )

            assert answer == escaped_texts[mode]
