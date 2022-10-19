"""

"""
import time
from pynput.keyboard import Key, Controller
import keyboard
from savefile import SaveSlot
from win32gui import GetWindowText, GetForegroundWindow

keyboard_input = Controller()

def available_hotkey_buttons() -> tuple:
    """
    List of keyboard buttons that can be used for hotkey assign.
    """

    return (
        "F1",
        "F2",
        "F3",
        "F4",
        "F5",
        "F6",
        "F7",
        "F8",
        "F9",
        "F10",
        "F11",
        "F12",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "0",
        "Num0",
        "Num1",
        "Num2",
        "Num3",
        "Num4",
        "Num5",
        "Num6",
        "Num7",
        "Num8",
        "Num9",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
        "Tab",
        "Space",
        "Backspace",
        "Enter",
        "Home",
        "PageUp",
        "End",
        "PageDown",
        "Insert",
        "Delete",
        "Ctrl",
        "Shift",
        "Alt"
    )

class Macro:
    """

    """

    def __init__(self):
        self.id: int = 0
        self.name: str = ''
        self.type: str = ''
        self.save_slot: SaveSlot = SaveSlot()
        self.hotkey: str = ''
        self.hotkey_ctrl: bool = False
        self.hotkey_shift: bool = False
        self.hotkey_alt: bool = False
        self.interrupted: bool = False
        self.interrupt_hotkey: str = ''
        self.pause_time: int = 20
        self.settings = {
            'equipment': {

            },
            'magic': {

            },
            'built-in': {
                'macro_name': ''
            },
            'diy': {
                'macro': ''
            }
        }
        self.macro_keyline: str = ''

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

    def form_keyline(self):
        """
        Forms a keyline string from macro settings to be executed to
        'execute' fuction
        """

        if self.type == 'Equipment':
            pass
        elif self.type == 'Magic':
            pass
        elif self.type == 'Built-in':
            built_in_macro_name = self.settings['built-in']['macro_name']
            built_in_macro = next(x for x in built_in_macros() if x['name'] == built_in_macro_name)
            self.macro_keyline = built_in_macro['keyline']
        elif self.type == 'DIY':
            commands_list = self.settings['diy']['macro'].strip().split('\n')
            keyline_list = []
            for command in commands_list:

                keyline = ''
                command = command.strip().lower()

                if not command:
                    continue

                mult = 0
                pause_time = 0
                press_time = 0

                if '*' in command:
                    parts = command.partition('*')
                    mult = int(parts[2].strip())
                    command = parts[0].strip()

                if '_pause' in command:
                    parts = command.partition('_pause')
                    pause_time = int(parts[2].strip())
                    command = parts[0].strip()

                if '_press' in command:
                    parts = command.partition('_press')
                    press_time = int(parts[2].strip())
                    command = parts[0].strip()

                # Searching in plain buttons...
                if command in game_control_keys()\
                        or command in available_hotkey_buttons():
                    keyline = command

                # Searching in built-in macros...
                if keyline == '':
                    macro = next((x for x in built_in_macros() if x['name'].lower() == command), None)
                    if macro is not None:
                        keyline = macro['keyline']

                # Searching in other macroses in this save-file
                if keyline == '':
                    macro = next((x for x in self.save_slot.macros if x.name.lower() == command), None)
                    if macro is not None:
                        macro.form_keyline()
                        keyline = macro.macro_keyline

                if keyline == '':
                    self.interrupted = True
                    break

                if pause_time:
                    keyline += f'|pause{pause_time}'

                if press_time:
                    keyline += f'_press{press_time}'

                if mult:
                    keyline_mult = []
                    for _ in range(mult):
                        keyline_mult.append(keyline)
                    keyline = '|'.join(keyline_mult)

                keyline_list.append(keyline)

            self.macro_keyline = '|'.join(keyline_list)

    def execute(self):
        """

        """

        # current_window_text: str = (GetWindowText(GetForegroundWindow()))
        # if 'elden' not in current_window_text.lower() \
        #         and 'melina' not in current_window_text.lower():
        #     return

        if self.interrupt_hotkey:
            keyboard.add_hotkey(self.interrupt_hotkey,
                                self.set_macro_interrupted,
                                suppress=True)

        self.form_keyline()
        self.execute_keyline()


    def execute_keyline(self) -> None:
        """
        Parses a line into a keys and simulates key presses.
        Additional pause can be made with 'pauseN', where N is one hundredth sec.
        """

        sleep_time = self.pause_time / 1000
        keyline = self.macro_keyline

        key_presses = keyline.split('|')
        press_time = sleep_time

        # TODO: допилить или удалить
        # # Check if this keyline will even work (everything can be in DIY macro,
        # # or there's can be no needed control assign in Elden Ring).
        # for key_press in key_presses:
        #
        #     if key_press.startswith('pause'):
        #         pause_time = key_press.replace('pause', '')
        #         if pause_time.isdigit():
        #             continue
        #
        #     if '_press' in keyline:
        #         parts = key_press.partition('_press')
        #         key_press = parts[0]
        #
        #     if key_press in self.save_slot.game_controls.keys() \
        #             or key_press in available_hotkey_buttons() \
        #             or key_press in non_letter_keys()\
        #             or (len(key_press) == 1 and key_press.isalpha()):
        #         continue
        #
        #     # Check failed.
        #     return

        # Execution.
        for key_press in key_presses:

            if self.interrupted:
                break

            # Additional pauses.
            if key_press.startswith('pause'):
                pause_time = int(key_press.replace('pause', ''))
                time.sleep(pause_time / 1000)
                continue

            # Additional press time.
            if '_press' in key_press:
                parts = key_press.partition('_press')
                key_press = parts[0]
                press_time = parts[2]

            # Turn actions ("guard", "strong_attack" etc.) to actions' keys.
            if key_press in self.save_slot.game_controls.keys():
                key_press = self.save_slot.game_controls[key_press].lower()

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

        self.interrupted = False


    def set_macro_interrupted(self) -> None:
        """

        """
        self.interrupted = True

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
        {'name': 'Sort all: Asc. Order of Acquisition',
         'keyline': keyline_to_sort_all_lists(),
         'comment': 'commentary ha ha ha'},
        {'name': 'Crouch attack',
         'keyline': 'crouch|attack',
         'comment': 'commentary'},
        {'name': 'Stance attack',
         'keyline': 'crouch|skill|attack',
         'comment': 'commentary'},
        {'name': 'Stance strong attack',
         'keyline': 'crouch|skill|strong_attack',
         'comment': 'commentary'},
        {'name': 'Two hand a weapon',
         'keyline': 'use|attack',
         'comment': 'commentary'},
        {'name': 'Two hand a weapon (left)',
         'keyline': 'use|guard',
         'comment': 'commentary'},
        {'name': 'Next weapon (right)',
         'keyline': keyline_to_choose_next_weapon(),
         'comment': 'commentary'},
        {'name': 'Previous weapon (right)',
         'keyline': keyline_to_choose_previous_weapon(),
         'comment': 'commentary'},
        {'name': 'Next weapon (left)',
         'keyline': keyline_to_choose_next_weapon(left_hand=True),
         'comment': 'commentary'},
        {'name': 'Previous weapon (left)',
         'keyline': keyline_to_choose_previous_weapon(left_hand=True),
         'comment': 'commentary'},
        {'name': 'Endless invasion attempts (wide)',
         'keyline': f'{keyline_to_invade_as_bloody_finger(True)}|pause4000|{keyline_to_invade_as_recusant(True)}|pause4000' * 50,
         'comment': 'commentary'},
        {'name': 'Endless invasion attempts (local)',
         'keyline': f'{keyline_to_invade_as_bloody_finger()}|pause4000|{keyline_to_invade_as_recusant()}|pause4000' * 50,
         'comment': 'commentary'},
        {'name': 'Reverse backstep',
         'keyline': 'jump',
         'comment': 'commentary'},
        {'name': 'Neutral long jump',
         'keyline': 'jump',
         'comment': 'commentary'},
        {'name': 'Backward jump',
         'keyline': 'jump',
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

    keyline = 'esc|e|e|t|down|e|pause300|q|pause300|' \
              'down|down|e|t|down|e|pause300|q|pause300|' \
              'down|e|t|down|e|pause300|q|pause300|' \
              'q|pause300|down|down|e|t|down|e|pause300|esc'

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


# def go_to_beginning_of_list(list_length: int = 50) -> None:
#     """
#
#     :param list_length:
#     :return:
#     """
#
#     max_amount_c = list_length // 25
#
#     keyboard_input.press(Key.left)
#     # TODO: убрать это дело вообще, но подумать, действительно ли оно не нужно
#     time4all = max(0.4, max_amount_c * 0.017)
#     time.sleep(0.01)
#     time_start = time.time()
#     execute_key_macros('c|' * (max_amount_c - 1) + 'c')
#     time_finish = time.time()
#     print(time_finish - time_start)
#     time_remain = time4all - (time_finish - time_start)
#     if time_remain > 0:
#         time.sleep(time_remain)
#     keyboard_input.release(Key.left)
#     time.sleep(0.01)
