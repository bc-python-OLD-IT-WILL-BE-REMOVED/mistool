#!/usr/bin/env python3

# --------------------- #
# -- SEVERAL IMPORTS -- #
# --------------------- #

from collections import OrderedDict
from pytest import fixture

from mistool.os_use import PPath
from orpyste.data import ReadBlock as READ


# ------------------- #
# -- MODULE TESTED -- #
# ------------------- #

from mistool import term_use


# ----------------------- #
# -- GENERAL CONSTANTS -- #
# ----------------------- #

THIS_DIR = PPath(__file__).parent

WITHFRAME_FUNCTION = term_use.withframe


# ----------------------- #
# -- DATAS FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = OrderedDict()

cfgdir = THIS_DIR / "default"

for ppath in cfgdir.walk(regpath = "file::**.txt"):
    style = '{0}_{1}'.format(
        ppath.parent.name,
        ppath.stem
    )

    THE_DATAS_FOR_TESTING[style] = READ(
        content = ppath,
        mode    = {
            "keyval:: =": "gene",
            "verbatim"  : ["frame", "text", "output"]
        }
    )

@fixture(scope="module")
def or_datas(request):
    for style, allinfos in THE_DATAS_FOR_TESTING.items():
        allinfos.build()

    def remove_extras():
        for style, allinfos in THE_DATAS_FOR_TESTING.items():
            allinfos.remove_extras()

    request.addfinalizer(remove_extras)


# ------------------- #
# -- CASE VARIANTS -- #
# ------------------- #

def test_term_use_frame(or_datas):
    for style, allinfos in THE_DATAS_FOR_TESTING.items():
        infos = allinfos.mydict("std nosep nonb")

        gene  = infos['gene']
        align = gene['align']

        if 'frame' in infos:
            frame = "\n".join(infos['frame'])

        else:
            frame = "term_use.ALL_FRAMES['{0}']".format(style)

        frame = eval(frame)

        text   = "\n".join(infos['text'])
        output = "\n".join(infos['output'])\
                    .replace("/:", "/")\
                    .replace(":/", "/")

        output_found = WITHFRAME_FUNCTION(
            text  = text,
            frame = frame,
            align = align
        )

        assert output == output_found
