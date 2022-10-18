"""

"""
import time
from pynput.keyboard import Key, Controller, Listener
import keyboard
from win32gui import GetWindowText, GetForegroundWindow

keyboard_input = Controller()

class Macro:
    """

    """

    def __init__(self):
        self.id: int = 0
        self.name: str = ''
        self.type: str = ''
        self.hotkey: str = ''
        self.hotkey_ctrl: bool = False
        self.hotkey_shift: bool = False
        self.hotkey_alt: bool = False

    def __str__(self):
        return f'id: {self.id}, name: {self.name}, hotkey: {self.hotkey}'

    def hotkey_string(self):

        hotkey_list = []
        hotkey = ''
        if self.hotkey:
            if self.hotkey_ctrl:
                hotkey_list.append('ctrl')
            if self.hotkey_shift:
                hotkey_list.append('shift')
            if self.hotkey_alt:
                hotkey_list.append('alt')
            hotkey_list.append(self.hotkey)
            hotkey = '+'.join(hotkey_list)

        return hotkey

    def execute(self):
        """

        """

        current_window_text: str = (GetWindowText(GetForegroundWindow()))
        if 'elden' not in current_window_text.lower() \
                and 'melina' not in current_window_text.lower():
            return

        # TODO: Если поймали кнопку, отвечающую за блок алгоритма, то нажимаем ее. Возможно, установить булево значение какое-нибудь в макрос.


        print(self.id, self.name, self.hotkey_string())

def on_press(key):
    """


    """

    while keyboard.is_pressed('u'):
        execute_key_macros('esc|pause10|e|e')
        go_to_beginning_of_list()
        execute_key_macros(keyline_to_find_item_number(13), 0.02)
        execute_key_macros('e|esc|y')

    while keyboard.is_pressed('i'):
        execute_key_macros('esc|pause10|e|r|esc|esc|e|e|pause10')
        execute_key_macros(keyline_to_find_item_number(8), 0.02)
        execute_key_macros('e|esc|ctrl')


def non_letter_keys() -> tuple:
    """

    """
    return ('alt', 'alt_l', 'alt_r', 'alt_gr', 'backspace', 'caps_lock', 'cmd',
            'cmd_r', 'ctrl', 'ctrl_l', 'ctrl_r', 'delete', 'down', 'end',
            'enter', 'esc', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8',
            'f9', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17',
            'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'home', 'left',
            'page_down', 'page_up', 'right', 'shift', 'shift_r', 'space',
            'tab', 'up', 'media_play_pause', 'media_volume_mute',
            'media_volume_down', 'media_volume_up', 'media_previous',
            'media_next', 'insert', 'menu', 'num_lock', 'pause',
            'print_screen', 'scroll_lock')


def game_control_keys() -> tuple:
    """

    """

    return (
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
        'event_action'
    )

def built_in_macros() -> list:
    """

    """

    macros_list = [
        {'name': 'Sort all lists: Asc. Order of Acquisition',
         'macro': keyline_to_sort_all_lists(),
         'comment': 'commentary'},
        {'name': 'Crouch attack',
         'macro': 'crouch|attack',
         'comment': 'commentary'},
        {'name': 'Stance attack',
         'macro': 'crouch|skill|attack',
         'comment': 'commentary'},
        {'name': 'Stance strong attack',
         'macro': 'crouch|skill|strong_attack',
         'comment': 'commentary'},
        {'name': 'Two hand a weapon',
         'macro': 'use|attack',
         'comment': 'commentary'},
        {'name': 'Two hand a weapon (left)',
         'macro': 'use|guard',
         'comment': 'commentary'},
        {'name': 'Next weapon (right)',
         'macro': keyline_to_choose_next_weapon(),
         'comment': 'commentary'},
        {'name': 'Previous weapon (right)',
         'macro': keyline_to_choose_previous_weapon(),
         'comment': 'commentary'},
        {'name': 'Next weapon (left)',
         'macro': keyline_to_choose_next_weapon(left_hand=True),
         'comment': 'commentary'},
        {'name': 'Previous weapon (left)',
         'macro': keyline_to_choose_previous_weapon(left_hand=True),
         'comment': 'commentary'},
        {'name': 'Endless invasion attempts (wide)',
         'macro': f'{keyline_to_invade_as_bloody_finger(True)}|pause400|{keyline_to_invade_as_recusant(True)}|pause400' * 50,
         'comment': 'commentary'},
        {'name': 'Endless invasion attempts (local)',
         'macro': f'{keyline_to_invade_as_bloody_finger()}|pause400|{keyline_to_invade_as_recusant()}|pause400' * 50,
         'comment': 'commentary'}
    ]

    # Use item macros.
    for i in range(1, 11):
        macros_list.append({
            'name': f'Use item #{str(i)}',
            'macro': f'switch_item_press200{"|switch_item" * (i - 1)}use_item|',
            'comment': 'commentary'
        })

    # Switch to spell macros.
    for i in range(1, 13):
        macros_list.append({
            'name': f'Switch to spell #{str(i)}',
            'macro': f'switch_spell_press200{"|switch_spell" * (i - 1)}',
            'comment': 'commentary'
        })

    return macros_list


def keyline_to_sort_all_lists() -> str:
    """
    Returns a keyline for a macros that sorts all lists to "date get - up".
    Weapons, armor, talismans, items.
    :return:
    """

    # 1. Weapons.
    # 2. Armor.
    # 3. Talismans.
    # 4. Items.

    keyline = 'esc|e|e|t|down|e|pause30|q|pause30|' \
              'down|down|e|t|down|e|pause30|q|pause30|' \
              'down|e|t|down|e|pause30|q|pause30|' \
              'q|pause30|down|down|e|t|down|e|pause30|esc'

    return keyline

def keyline_to_invade_as_bloody_finger(wide_invade: bool = True) -> str:
    """
    Returns a keyline for a macros that uses bloody finger.
    :return:
    """

    keyline = 'esc|up|up|e|up|up|e'

    if wide_invade:
        keyline += "|right"

    keyline += '|e|esc'

    return keyline


def keyline_to_invade_as_recusant(wide_invade: bool = True) -> str:
    """
    Returns a keyline for a macros that uses recusant finger.
    :return:
    """

    keyline = 'esc|up|up|e|up|up|right|e'

    if wide_invade:
        keyline += "|right"

    keyline += '|e|esc'

    return keyline


def keyline_to_choose_next_weapon(weapons_pass: int = 0, left_hand = False) -> str:
    """
    Returns a macros keyline that chooses next weapon.
    :param weapons_pass: how many weapons will be passed before choosing.
    """

    right_amount = weapons_pass + 1

    keyline = f'esc|e|{"down|" if left_hand else ""}e|{"right|" * right_amount}|e|esc'
    return keyline


def keyline_to_choose_previous_weapon(weapons_pass: int = 0, left_hand = False) -> str:
    """
    Returns a macro keyline that chooses previous weapon.
    :param weapons_pass: how many weapons will be passed before choosing.
    """

    left_amount = weapons_pass + 1

    keyline = f'esc|e|{"down|" if left_hand else ""}e|{"left|" * left_amount}|e|esc'

    return keyline


def keyline_to_find_item_number(item_number: int) -> str:
    """
    Generates a keyline to get to item having a number from a
    beginning of the list.
    :param item_number:
    :return:
    """

    # TODO: Сделать так, чтобы можно было вперёд пройти на 5 раз,
    # назад на несколько. Но для этого нужен точный размер инвентаря,
    # а также учитывать, как работает кнопка V ближе к концу - она же
    # не всегда спускается на 25, она может спуститься в самый юго-запад...

    v_amount: int = 0  # going to 5 items
    right_amount: int = 0  # going to 1 item

    key_presses = []
    if item_number > 5:
        v_amount = item_number // 25

    right_amount = item_number - (v_amount * 25) - 1
    for _ in range(v_amount):
        key_presses.append('v')

    for _ in range(right_amount):
        key_presses.append('right')

    return '|'.join(key_presses)


def go_to_beginning_of_list(list_length: int = 50) -> None:
    """

    :param list_length:
    :return:
    """

    max_amount_c = list_length // 25

    keyboard_input.press(Key.left)
    # TODO: убрать это дело вообще, но подумать, действительно ли оно не нужно
    time4all = max(0.4, max_amount_c * 0.017)
    time.sleep(0.01)
    time_start = time.time()
    execute_key_macros('c|' * (max_amount_c - 1) + 'c')
    time_finish = time.time()
    print(time_finish - time_start)
    time_remain = time4all - (time_finish - time_start)
    if time_remain > 0:
        time.sleep(time_remain)
    keyboard_input.release(Key.left)
    time.sleep(0.01)


def execute_key_macros(keyline: str, sleep_time: float = 0.03) -> None:
    """
    Parses a line into a keys and simulates key presses.
    Additional pause can be made with 'pauseN', where N is one hundredth sec.
    :param keyline: line of keys divided with '|'
    :param sleep_time:
    :return:
    """

    key_presses = keyline.split('|')
    press_time = sleep_time

    for key_press in key_presses:

        # Additional pauses.
        if key_press.startswith('pause'):
            pause_time = int(key_press.replace('pause', ''))
            time.sleep(pause_time / 100)
            continue

        # Additional press time.
        if '_press' in key_press:
            parts = key_press.partition('_press')
            key_press = parts[0]
            press_time = parts[2]

        # TODO: сделать ветку на то, если key_press является командой игры, например "strong_attack".
        # Нужен список таких команд, проверка, является ли команда командой игры,
        # и поиск соответствия для нее команде из списка (командаигры - кнопка),
        # список есть в savefile.get_controls()

        if key_press in game_control_keys():
            key_press = ''

        # Key presses execution.
        if key_press in non_letter_keys():
            keyboard_input.press(Key[key_press])
            time.sleep(press_time)
            keyboard_input.release(Key[key_press])
        else:
            keyboard_input.press(key_press)
            time.sleep(press_time)
            keyboard_input.release(key_press)

        time.sleep(sleep_time)
