"""
Contains raw data about keyboard buttons information, relatable to game.
"""


def non_letter_keys() -> tuple:
    """
    Returns keys that are not letters. That distinction is important for
    key input with "pynput".
    """
    return (
        'alt',
        'alt_l',
        'alt_r',
        'alt_gr',
        'backspace',
        'caps_lock',
        'cmd',
        'cmd_r',
        'ctrl',
        'ctrl_l',
        'ctrl_r',
        'delete',
        'down',
        'end',
        'enter',
        'esc',
        'f1',
        'f2',
        'f3',
        'f4',
        'f5',
        'f6',
        'f7',
        'f8',
        'f9',
        'f10',
        'f11',
        'f12',
        'f13',
        'f14',
        'f15',
        'f16',
        'f17',
        'f18',
        'f19',
        'f20',
        'f21',
        'f22',
        'f23',
        'f24',
        'home',
        'left',
        'page_down',
        'page_up',
        'right',
        'shift',
        'shift_r',
        'space',
        'tab',
        'up',
        'media_play_pause',
        'media_volume_mute',
        'media_volume_down',
        'media_volume_up',
        'media_previous',
        'media_next',
        'insert',
        'menu',
        'num_lock',
        'pause',
        'print_screen',
        'scroll_lock',
    )


def game_control_keys() -> tuple:
    """
    Returns names of Elden Ring commands that are used in macros.
    """

    return (
        'move_up',
        'move_down',
        'move_left',
        'move_right',
        'roll',
        'jump',
        'crouch',
        'reset_camera',
        'switch_spell',
        'switch_item',
        'attack',
        'strong_attack',
        'guard',
        'skill',
        'use_item',
        'event_action',
    )


def available_buttons_with_codes() -> dict:
    """
    Dict of keyboard buttons that can be used for hotkey assign.
    Values are VK codes used by 'pynput'.
    """

    return {
        'F1': 112,
        'F2': 113,
        'F3': 114,
        'F4': 115,
        'F5': 116,
        'F6': 117,
        'F7': 118,
        'F8': 119,
        'F9': 120,
        'F10': 121,
        'F11': 122,
        'F12': 123,
        '1': 49,
        '2': 50,
        '3': 51,
        '4': 52,
        '5': 53,
        '6': 54,
        '7': 55,
        '8': 56,
        '9': 57,
        '0': 48,
        'Num0': 96,
        'Num1': 97,
        'Num2': 98,
        'Num3': 99,
        'Num4': 100,
        'Num5': 101,
        'Num6': 102,
        'Num7': 103,
        'Num8': 104,
        'Num9': 105,
        'A': 65,
        'B': 66,
        'C': 67,
        'D': 68,
        'E': 69,
        'F': 70,
        'G': 71,
        'H': 72,
        'I': 73,
        'J': 74,
        'K': 75,
        'L': 76,
        'M': 77,
        'N': 78,
        'O': 79,
        'P': 80,
        'Q': 81,
        'R': 82,
        'S': 83,
        'T': 84,
        'U': 85,
        'V': 86,
        'W': 87,
        'X': 88,
        'Y': 89,
        'Z': 90,
        '[': 219,
        ']': 221,
        ';': 186,
        "'": 222,
        '\\': 220,
        ',': 188,
        '.': 190,
        '/': 191,
        '-': 189,
        '=': 187,
        '~': 192,
        'Tab': 9,
        'Space': 32,
        'Backspace': 8,
        'Enter': 13,
        'Home': 36,
        'PageUp': 33,
        'PageDown': 34,
        'End': 35,
        'Insert': 45,
        'Delete': 46,
        'Ctrl': 162,
        'Shift': 160,
        'Alt': 164,
    }


def control_keys_values() -> dict:
    """
    Returns values for keys that are used in save-file to define what key
    is used for a control. Values are in decimal.
    For example, "Num4" ("144" dec.) would be "90" in HEX-file.
    """

    return {
        128: 'F1',
        129: 'F2',
        130: 'F3',
        131: 'F4',
        132: 'F5',
        133: 'F6',
        134: 'F7',
        135: 'F8',
        136: 'F9',
        137: 'F10',
        156: 'F11',
        157: 'F12',
        80: '0',
        71: '1',
        72: '2',
        73: '3',
        74: '4',
        75: '5',
        76: '6',
        77: '7',
        78: '8',
        79: '9',
        151: 'Num0',
        148: 'Num1',
        149: 'Num2',
        150: 'Num3',
        144: 'Num4',
        145: 'Num5',
        146: 'Num6',
        140: 'Num7',
        141: 'Num8',
        142: 'Num9',
        99: 'A',
        117: 'B',
        115: 'C',
        101: 'D',
        87: 'E',
        102: 'F',
        103: 'G',
        104: 'H',
        92: 'I',
        105: 'J',
        106: 'K',
        107: 'L',
        119: 'M',
        118: 'N',
        93: 'O',
        94: 'P',
        85: 'Q',
        88: 'R',
        100: 'S',
        89: 'T',
        91: 'U',
        116: 'V',
        86: 'W',
        114: 'X',
        90: 'Y',
        113: 'Z',
        84: 'Tab',
        111: 'Shift',
        123: 'Shift',
        98: 'Ctrl',
        226: 'Ctrl',
        83: 'Backspace',
        126: 'Space',
        97: 'Enter',
        225: 'Enter',
        125: 'Alt',
        268: 'Home',
        188: 'PageUp',
        194: 'End',
        196: 'PageDown',
        197: 'Insert',
        198: 'Delete',
        190: 'Up',
        192: 'Left',
        195: 'Down',
        193: 'Right',
    }


def available_game_control_buttons() -> tuple:
    """
    List of keyboard buttons that can be used to assign in Elden Ring
    and are used on control panel on "Settings" page.
    """

    return (
        '1',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '0',
        'Num0',
        'Num1',
        'Num2',
        'Num3',
        'Num4',
        'Num5',
        'Num6',
        'Num7',
        'Num8',
        'Num9',
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H',
        'I',
        'J',
        'K',
        'L',
        'M',
        'N',
        'O',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        'V',
        'W',
        'X',
        'Y',
        'Z',
        'Tab',
        'Space',
        'Backspace',
        'Enter',
        'Home',
        'PageUp',
        'End',
        'PageDown',
        'Insert',
        'Delete',
        'Ctrl',
        'Shift',
        'Alt',
        'Up',
        'Left',
        'Down',
        'Right',
    )