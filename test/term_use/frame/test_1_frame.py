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
# -- THE_DATAS_FOR_TESTING FOR TESTING -- #
# ----------------------- #

THE_DATAS_FOR_TESTING = OrderedDict()

cfgdir = THIS_DIR / "default"

for ppath in cfgdir.walk(regpath = "**.txt"):
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

    def remove():
        for style, allinfos in THE_DATAS_FOR_TESTING.items():
            allinfos.remove()

    request.addfinalizer(remove)


# ------------------- #
# -- CASE VARIANTS -- #
# ------------------- #

def test_term_use_frame(or_datas):
    for style, allinfos in THE_DATAS_FOR_TESTING.items():
        infos = allinfos.dico(
            nosep    = True,
            nonbline = True
        )

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
