#!/usr/bin/env python3

import re


# ----------- #
# -- WORDS -- #
# ----------- #

FR_ACCENTUED_LETTERS = "âàéèêëîïôùüç"

PATTERNS_WORDS = {
# Natural language
    'en': re.compile("([a-zA-Z]+)"),
    'fr': re.compile(
        "([a-z{0}A-Z{1}]+)".format(
            FR_ACCENTUED_LETTERS,
            FR_ACCENTUED_LETTERS.upper()
        )
    ),
# Coding
    'var': re.compile("([a-zA-Z][\d_a-zA-Z]*)"),
}
