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

    def remove_extras():
        THE_DATAS_FOR_TESTING.remove_extras()

    request.addfinalizer(remove_extras)


# ------------------- #
# -- GOOD ESCAPING -- #
# ------------------- #

def test_latex_use_escape(or_datas):
    tests = THE_DATAS_FOR_TESTING.treedict

    for testname, infos in tests.items():
        source        = infos['source']['value']
        escaped_texts = {}

        if 'text' in infos:
            escaped_texts['text'] = infos['text']['value']
        else:
            escaped_texts['text'] = infos['both']['value']

        if 'math' in infos:
            escaped_texts['math'] = infos['math']['value']
        else:
            escaped_texts['math'] = infos['both']['value']

        for mode in ['text', 'math']:
            answer_wanted = ESCAPE_FUNCTION(
                text = source,
                mode = mode
            )

            answer_found = escaped_texts[mode]

            assert answer_wanted == answer_found
