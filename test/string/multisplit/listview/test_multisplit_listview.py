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

from mistool import string_use
from mistool.config.pattern import PATTERNS_WORDS

# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = Path(__file__).parent

CLASS_MULTI_SPLIT = string_use.MultiSplit


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = READ(
    content = THIS_DIR / 'multisplit_listview.txt',
    mode = {
        'container' : ":default:",
        'verbatim'  : ["text", "seps", "escape", "listview"]
    }
)

@fixture(scope="module")
def or_datas(request):
    THE_DATAS_FOR_TESTING.build()

    def remove_extras():
        THE_DATAS_FOR_TESTING.remove_extras()

    request.addfinalizer(remove_extras)


# --------------- #
# -- REPLACING -- #
# --------------- #

def test_string_use_multisplit_listview(or_datas):
    tests = THE_DATAS_FOR_TESTING.treedict

    for testname, infos in tests.items():
        _, text = infos['text'][0]
        text    = text.strip()

        _, seps = infos['seps'][0]
        seps    = eval(seps)

        print(infos['listview'])

        listview_wanted = " ".join([
            l
            for _, l in infos['listview']
        ])

        listview_wanted = eval("({0})".format(listview_wanted))

        if 'escape' in infos:
            _, escape = infos['escape'][0]

        else:
            escape = ""

        msplit = CLASS_MULTI_SPLIT(
            seps     = seps,
            esc_char = escape,
            strip    = True
        )

        listview_found = msplit(text)

        assert listview_wanted == listview_found
