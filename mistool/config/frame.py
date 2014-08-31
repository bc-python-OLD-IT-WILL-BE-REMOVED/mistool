#!/usr/bin/env python3

# The following ugly variables were automatically build.

_ABREVS_FRAMES = {
    'corner': {
        'leftdown': 'ld',
        'leftup': 'lu',
        'rightdown': 'rd',
        'rightup': 'ru'
    },
    'rule': {
        'down': 'd',
        'left': 'l',
        'right': 'r',
        'up': 'u'
    }
}

_KEYS_FRAME = {
    'corner': {'rightup', 'ru', 'rightdown', 'leftdown', 'ld', 'leftup', 'rd',
    'lu'},
    'rule': {'left', 'd', 'l', 'right', 'up', 'u', 'r', 'down'}
}

FRAMES_FORMATS = {}

FRAMES_FORMATS['c_basic'] = {
    'corner': {
        'leftup': '/',
        'rightdown': '/'
    },
    'rule': {
        'down': '*',
        'left': '*',
        'right': '*',
        'up': '*'
    }
}

FRAMES_FORMATS['c_pretty'] = {
    'corner': {
        'leftdown': '* ',
        'leftup': '/* ',
        'rightdown': ' */',
        'rightup': ' *'
    },
    'rule': {
        'down': '-',
        'left': '--',
        'right': '--',
        'up': '-'
    }
}

FRAMES_FORMATS['pyba_part_nb'] = {
    'rule': {
        'down': '*',
        'up': '*'
    }
}

FRAMES_FORMATS['pyba_part_no_nb'] = {
    'rule': {
        'down': ':',
        'up': ':'
    }
}

FRAMES_FORMATS['pyba_title_nb'] = {
    'rule': {
        'down': '=',
        'up': '='
    }
}

FRAMES_FORMATS['pyba_title_no_nb'] = {
    'rule': {
        'down': '-',
        'up': '-'
    }
}

FRAMES_FORMATS['python_basic'] = {
    'rule': {
        'down': '#',
        'left': '#',
        'right': '#',
        'up': '#'
    }
}

FRAMES_FORMATS['python_pretty'] = {
    'extra': {
        'rule': {
            'left': '#',
            'right': '#'
        }
    },
    'rule': {
        'down': '-',
        'left': '--',
        'right': '--',
        'up': '-'
    }
}

FRAMES_FORMATS['unittest_basic'] = {
    'rule': {
        'down': '*',
        'left': '*',
        'right': '*',
        'up': '*'
    }
}

FRAMES_FORMATS['unittest_problem'] = {
    'extra': {
        'rule': {
            'down': '*',
            'left': '*',
            'right': '*',
            'up': '*'
        }
    },
    'rule': {
        'down': '*',
        'left': '* ---->>',
        'right': '<<---- *',
        'up': '*'
    }
}
