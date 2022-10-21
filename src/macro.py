"""

"""
import time
from pynput.keyboard import Key, Controller
import keyboard
from savefile import SaveSlot
from win32gui import GetWindowText, GetForegroundWindow

pynput_in = Controller()

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
        "Alt",
        "~"
    )

class Macro:
    """

    """

    def __init__(self, saveslot: SaveSlot = SaveSlot()):
        self.saveslot: SaveSlot = saveslot
        self.set_id()
        self.name = self.standard_name()
        self.type: str = ''
        self.savefile = self.saveslot.savefile
        self.hotkey: str = ''
        self.hotkey_ctrl: bool = False
        self.hotkey_shift: bool = False
        self.hotkey_alt: bool = False
        self.interrupted: bool = False
        self.recovery_hotkey: str = ''
        self.pause_time: int = 20
        self.macro_keyline: str = ''
        self.settings = {
            'equipment': {

            },
            'magic': {
                'spell_number': 0,
                'current_number': 0,
                'instant_cast_right': False,
                'instant_cast_left': False
            },
            'built-in': {
                'macro_name': ''
            },
            'diy': {
                'macro': ''
            }
        }

    def standard_name(self):
        return '< name >'

    def set_id(self):
        """
        Sets an id to macro. Format is like '7023', where '7' is saveslot number
        and 23 - plain macro order number.
        """

        self.id = 0

        if not self.saveslot.name:
            return

        saveslot_macros = self.saveslot.macros
        if saveslot_macros:
            max_id = max(saveslot_macros, key=lambda macro: macro.id).id
            self.id = max_id + 1
        else:
            self.id = self.saveslot.number * 1000 + 1

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

        # TODO: не забыть вернуть
        current_window_text: str = (GetWindowText(GetForegroundWindow()))
        # if 'elden' not in current_window_text.lower(): # \
        #         # and 'melina' not in current_window_text.lower():
        #     return

        # # TODO: подумать, что делать с интерраптом
        # if self.recovery_hotkey:
        #     keyboard.add_hotkey(self.recovery_hotkey,
        #                         what,
        #                         suppress=True)

        self.interrupted = False
        time_start = time.time()
        print('='*40)
        print('Macro:   ', f'#{self.id} ({self.type}) ({self.hotkey_string()}) {self.name}')
        print('Start:   ', time.ctime(time_start))

        # Nobody knows what can happen inside keylines mechanism
        # (especially with DIYs), so we need exceptions catch.
        try:
            self.form_keyline()
            self.execute_keyline()
        except Exception as e:
            print('Exception!')
            print(e)

        time_end = time.time()
        print('End:     ', time.ctime(time_end))
        print('Duration:', round(time_end - time_start, 5))

    def form_keyline(self):
        """
        Forms a keyline string from macro settings to be executed to
        'execute' function.
        """

        def form_keyline_equipment(self):
            pass

        def form_keyline_magic(self):
            settings = self.settings['magic']
            if not settings['spell_number']:
                return

            cur_spell = self.saveslot.current_spell
            goal_spell = settings['spell_number']
            total_spells = len(self.saveslot.spells)
            print('Total spells -', total_spells)
            print('Current spell -', cur_spell)
            print('Goal spell -', goal_spell)
            # If current spell is spell we need, then we just need to
            # check "instant cast" afterwards.
            spells_equal = False
            if cur_spell == goal_spell:
                self.macro_keyline = ' '
                spells_equal = True

            if not spells_equal:
                # If we know what spell we're having right now then we save
                # time if not pressing 'switch_spell' for half sec and
                # calculate amount of keypresses to just switch to spell from macro.
                if cur_spell:
                    needed_switches = goal_spell - cur_spell
                    if cur_spell > goal_spell:
                        needed_switches = total_spells - cur_spell + goal_spell
                    self.macro_keyline = '|switch_spell|pause10' * needed_switches
                else:
                    self.macro_keyline = f'switch_spell_press600{"|switch_spell|pause10" * (goal_spell - 1)}'

            if settings['instant_cast_right']:
                self.macro_keyline += '|attack'

            if settings['instant_cast_left']:
                self.macro_keyline += '|guard'

            # Set current number for next macro uses.
            self.saveslot.current_spell = settings['spell_number']
            print('Current spell now -', self.saveslot.current_spell)

        def form_keyline_builtin(self):
            built_in_macro_name = self.settings['built-in']['macro_name']
            built_in_macro = next(x for x in built_in_macros() if
                                  x['name'] == built_in_macro_name)
            self.macro_keyline = built_in_macro['keyline']

        def form_keyline_diy(self):
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

                if 'pause' in command:
                    digits = command.replace('pause', '')
                    if digits.isdigit():
                        keyline = command

                # Searching in plain buttons...
                if command in game_control_keys() \
                        or command in available_hotkey_buttons() \
                        or command in non_letter_keys() \
                        or len(command) == 1 and command.isalpha()\
                        or command in []:
                    keyline = command

                # Searching in built-in macros...
                if keyline == '':
                    macro = next((x for x in built_in_macros() if
                                  x['name'].lower() == command), None)
                    if macro is not None:
                        keyline = macro['keyline']

                # Searching in other macroses in this save-file
                if keyline == '':
                    macro = next((x for x in self.saveslot.macros if
                                  x.name.lower() == command), None)
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

        if self.type == 'Equipment':
            form_keyline_equipment(self)
        elif self.type == 'Magic':
            form_keyline_magic(self)
        elif self.type == 'Built-in':
            form_keyline_builtin(self)
        elif self.type == 'DIY':
            form_keyline_diy(self)

    def execute_keyline(self) -> None:
        """
        Parses a line into a keys and simulates key presses.
        Additional pause can be made with 'pauseN', where N is one thousandth sec.
        Additional press time can be made with 'pressN'.
        """

        sleep_time = self.pause_time / 1000
        keyline = self.macro_keyline
        print('Keyline: ', keyline)
        key_presses = keyline.split('|')

        # Execution.
        for key_press in key_presses:

            if self.interrupted:
                break

            if key_press.strip() == '':
                continue

            # Additional pauses.
            if key_press.startswith('pause'):
                pause_time = int(key_press.replace('pause', ''))
                time.sleep(pause_time / 1000)
                continue

            # Additional press time.
            press_time = sleep_time
            if '_press' in key_press:
                parts = key_press.partition('_press')
                key_press = parts[0]
                press_time = int(parts[2]) / 1000

            # Turn actions ("guard", "strong_attack" etc.) to actions' keys.
            if key_press in self.savefile.game_controls.keys():
                key_press = self.savefile.game_controls[key_press].lower()

            # TODO: need to understand, why 'keyboard' can't press arrows
            # but 'pynput' can. Using two separate methods for input
            # makes me feel silly.

            # Key presses execution.
            keys_for_pynput = ['up', 'left', 'right', 'down']
            if key_press in keys_for_pynput:
                if key_press in non_letter_keys():
                    key_press = Key[key_press]
                pynput_in.press(key_press)
                time.sleep(press_time)
                pynput_in.release(key_press)
            else:
                keyboard.press(key_press)
                time.sleep(press_time)
                keyboard.release(key_press)

            time.sleep(sleep_time)

        self.interrupted = False

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
        'move_forward',
        'move_back',
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
        'event_action'
    )

def built_in_macros() -> list:
    """

    """

    macros_list = [
        {'name': 'Sort all: Asc. Acquisition',
         'keyline': keyline_to_sort_all_lists(),
         'comment': 'commentary ha ha ha'},
        {'name': 'Crouch attack',
         'keyline': 'crouch|attack',
         'comment': 'commentary'},
        {'name': 'Stance attack',
         'keyline': 'crouch|pause200|skill|attack',
         'comment': 'commentary'},
        {'name': 'Stance strong attack',
         'keyline': 'crouch|pause200|skill|strong_attack',
         'comment': 'commentary'},
        {'name': 'Reverse backstep',
         'keyline': 'roll|pause5|s',
         'comment': 'commentary'},
        {'name': 'Next weapon (right)',
         'keyline': keyline_to_choose_next_weapon(),
         'comment': 'commentarytst'},
        {'name': 'Previous weapon (right)',
         'keyline': keyline_to_choose_previous_weapon(),
         'comment': 'commentary'},
        {'name': 'Next weapon (left)',
         'keyline': keyline_to_choose_next_weapon(left_hand=True),
         'comment': 'commentary'},
        {'name': 'Previous weapon (left)',
         'keyline': keyline_to_choose_previous_weapon(left_hand=True),
         'comment': 'commentary'},
        {'name': 'Six invasion attempts (wide)',
         'keyline': f'{keyline_to_invade_as_bloody_finger(True)}|pause4000|{keyline_to_invade_as_recusant(True)}|pause4000|' * 3,
         'comment': 'commentary'},
        {'name': 'Six invasion attempts (local)',
         'keyline': f'{keyline_to_invade_as_bloody_finger()}|pause4000|{keyline_to_invade_as_recusant()}|pause4000' * 3,
         'comment': 'commentary'},
        {'name': 'Filthy teabagging',
         'keyline': '|'.join(['crouch|pause200']*17),
         'comment': 'Makes you feel good about yourself for maybe 8 seconds.'}
    ]

    # Use item macros.
    for i in range(1, 11):
        macros_list.append({
            'name': f'Use item #{str(i)}',
            'keyline': f'switch_item_press600{"|switch_item|pause10" * (i - 1)}|use_item',
            'comment': 'commentary'
        })

    # Switch to spell macros.
    for i in range(1, 13):
        macros_list.append({
            'name': f'Switch to spell #{str(i)}',
            'keyline': f'switch_spell_press600{"|switch_spell|pause10" * (i - 1)}',
            'comment': 'commentary'
        })

    # 6 gestures.
    for i in range(1, 7):
        downs = (i - 1) // 2
        rights = (i - 1) % 2
        macros_list.append({
            'name': f'Gesture #{str(i)}',
            'keyline': f'esc|right|down|down|down{"|down" * downs}{"|right" * rights}|e|esc',
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
              'down|e|t|down|e|pause300|q|pause300|'
              # 'q|pause300|down|down|e|t|down|e|pause300|esc'

    return keyline

def keyline_to_invade_as_bloody_finger(wide_invade: bool = True) -> str:
    """
    Returns a keyline for a macros that uses bloody finger.
    :return:
    """

    keyline = 'esc|up|up|e|up|up|e'

    if wide_invade:
        keyline += "|pause50|right"

    keyline += '|e|esc'

    return keyline


def keyline_to_invade_as_recusant(wide_invade: bool = True) -> str:
    """
    Returns a keyline for a macros that uses recusant finger.
    :return:
    """

    keyline = 'esc|up|up|e|up|up|right|e'

    if wide_invade:
        keyline += "|pause50|right"

    keyline += '|e|esc'

    return keyline


def keyline_to_choose_next_weapon(weapons_pass: int = 0, left_hand = False) -> str:
    """
    Returns a macro keyline that chooses next weapon.
    :param weapons_pass: how many weapons will be passed before choosing.
    """

    right_amount = weapons_pass + 1

    keyline = f'esc|e|{"down|" if left_hand else ""}e|{"right|" * right_amount}pause20|e|esc'
    return keyline


def keyline_to_choose_previous_weapon(weapons_pass: int = 0, left_hand = False) -> str:
    """
    Returns a macro keyline that chooses previous weapon.
    :param weapons_pass: how many weapons will be passed before choosing.
    """

    left_amount = weapons_pass + 1

    keyline = f'esc|e|{"down|" if left_hand else ""}e|{"left|" * left_amount}pause20|e|esc'

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
