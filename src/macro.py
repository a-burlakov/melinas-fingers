"""

"""
import sys
import traceback
import time
from win32gui import GetWindowText, GetForegroundWindow
import keyboard
from pynput.keyboard import Key, Controller
from savefile import SaveSlot

pynput_in = Controller()


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
        'event_action'
    )


def available_buttons_with_codes() -> dict:
    """
    Dict of keyboard buttons that can be used for hotkey assign.
    Values are VK codes used by 'pynput'.
    """

    return {
        "F1": 112,
        "F2": 113,
        "F3": 114,
        "F4": 115,
        "F5": 116,
        "F6": 117,
        "F7": 118,
        "F8": 119,
        "F9": 120,
        "F10": 121,
        "F11": 122,
        "F12": 123,
        "1": 49,
        "2": 50,
        "3": 51,
        "4": 52,
        "5": 53,
        "6": 54,
        "7": 55,
        "8": 56,
        "9": 57,
        "0": 48,
        "Num0": 96,
        "Num1": 97,
        "Num2": 98,
        "Num3": 99,
        "Num4": 100,
        "Num5": 101,
        "Num6": 102,
        "Num7": 103,
        "Num8": 104,
        "Num9": 105,
        "A": 65,
        "B": 66,
        "C": 67,
        "D": 68,
        "E": 69,
        "F": 70,
        "G": 71,
        "H": 72,
        "I": 73,
        "J": 74,
        "K": 75,
        "L": 76,
        "M": 77,
        "N": 78,
        "O": 79,
        "P": 80,
        "Q": 81,
        "R": 82,
        "S": 83,
        "T": 84,
        "U": 85,
        "V": 86,
        "W": 87,
        "X": 88,
        "Y": 89,
        "Z": 90,
        "[": 219,
        "]": 221,
        ";": 186,
        "'": 222,
        "\\": 220,
        ",": 188,
        ".": 190,
        "/": 191,
        "-": 189,
        "=": 187,
        "~": 192,
        "Tab": 9,
        "Space": 32,
        "Backspace": 8,
        "Enter": 13,
        "Home": 36,
        "PageUp": 33,
        "PageDown": 34,
        "End": 35,
        "Insert": 45,
        "Delete": 46,
        "Ctrl": 162,
        "Shift": 160,
        "Alt": 164
    }


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
                'instant_action': '',
                'weapon_right_1': {'action': 'skip', 'not_enough_stats': False,
                                   'name': '', 'position': 0},
                'weapon_right_2': {'action': 'skip', 'not_enough_stats': False,
                                   'name': '', 'position': 0},
                'weapon_right_3': {'action': 'skip', 'not_enough_stats': False,
                                   'name': '', 'position': 0},
                'weapon_left_1': {'action': 'skip', 'not_enough_stats': False,
                                  'name': '', 'position': 0},
                'weapon_left_2': {'action': 'skip', 'not_enough_stats': False,
                                  'name': '', 'position': 0},
                'weapon_left_3': {'action': 'skip', 'not_enough_stats': False,
                                  'name': '', 'position': 0},
                'armor_head': {'action': 'skip', 'not_enough_stats': False,
                               'name': '', 'position': 0},
                'armor_chest': {'action': 'skip', 'not_enough_stats': False,
                                'name': '', 'position': 0},
                'armor_arms': {'action': 'skip', 'not_enough_stats': False,
                               'name': '', 'position': 0},
                'armor_legs': {'action': 'skip', 'not_enough_stats': False,
                               'name': '', 'position': 0},
                'talisman_1': {'action': 'skip', 'not_enough_stats': False,
                               'name': '', 'position': 0},
                'talisman_2': {'action': 'skip', 'not_enough_stats': False,
                               'name': '', 'position': 0},
                'talisman_3': {'action': 'skip', 'not_enough_stats': False,
                               'name': '', 'position': 0},
                'talisman_4': {'action': 'skip', 'not_enough_stats': False,
                               'name': '', 'position': 0}
            },
            'magic': {
                'spell_number': 1,
                'instant_cast_right': False,
                'instant_cast_left': False
            },
            'built-in': {
                'macro_name': built_in_macros()[0]['name']
            },
            'diy': {
                'macro': ''
            }
        }

    @staticmethod
    def standard_name():
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

        # current_window_text: str = (GetWindowText(GetForegroundWindow()))
        # if 'elden' not in current_window_text.lower():
        #     print('Hotkey not started because Elden Ring is not open.')
        #     return

        self.interrupted = False
        time_start = time.time()
        print('=' * 40)
        print('Macro:   ', f'#{self.id} ({self.type}) ({self.hotkey_string()}) {self.name}')
        print('Start:   ', time.ctime(time_start))

        # Nobody knows what can happen inside keylines mechanism
        # (especially with DIYs), so we need exceptions catch.
        try:
            self.form_keyline()
            self.execute_keyline()
        except Exception as e:
            print('Exception: ', e)
            print(traceback.format_exc())

        time_end = time.time()
        print('End:     ', time.ctime(time_end))
        print('Duration:', round(time_end - time_start, 5))

    def form_keyline(self):
        """
        Forms a keyline string from macro settings to be executed to
        'execute' function.
        """

        if self.type == 'Equipment':
            self.form_keyline_equipment()
        elif self.type == 'Magic':
            self.form_keyline_magic()
        elif self.type == 'Built-in':
            self.form_keyline_builtin()
        elif self.type == 'DIY':
            self.form_keyline_diy()

    def form_keyline_equipment(self):

        keys_list = []  # list to be turned to keyline

        settings = self.settings['equipment']
        search_mode = self.saveslot.search_mode_equipment

        cells = ['weapon_right_1', 'weapon_right_2', 'weapon_right_3',
                 'weapon_left_1', 'weapon_left_2', 'weapon_left_3',
                 'armor_head', 'armor_chest', 'armor_arms', 'armor_legs',
                 'talisman_1', 'talisman_2', 'talisman_3', 'talisman_4']

        cells = {x: settings[x] for x in cells}

        # Actions to do after cell is passed to get to next cell.
        # Also put a key 'keyline' which will keep a keyline to handle a cell.
        actions_after_cell = ['right', 'right', 'left|left|down',
                              'right', 'right', 'left|left|down',
                              'right', 'right', 'right', 'right|down',
                              'right', 'right', 'right', 'right|down']
        for cell, action_after in zip(cells.keys(), actions_after_cell):
            cells[cell]['action_after'] = action_after
            cells[cell]['keyline'] = ''

        # Plan is simple, that's a Swiss f*cking watch:
        #   0. firstly we clear all cells to 'remove' or 'equip' if needed
        #   1. cycle through all cells and if it's 'remove' or 'equip', perform
        #       corresponding action;
        #   2. when 'remove' and 'equip' cells are out, we're pressing "Esc";
        #   3. if we have instant action - performing it.

        keys_list.append('esc|e')  # Open inventory.

        # 0. Preliminary clearing if "Auto" search mode.
        if search_mode == 'auto':

            for name, value in cells.items():
                if value['action'] in ['equip', 'remove']:
                    cells[name]['keyline'] = 'r'

            keys_list.append(self.keyline_for_cells(cells))

            # Re-enter to inventory.
            keys_list.append('esc|esc|e')

        # 0.1. If we're in manual mode, but have some cells to 'equip' having
        # no current position, that means we need to clear them to put to
        # position 1.
        currents = self.saveslot.current_equipment
        if search_mode != 'auto':
            are_there_cells_to_clear = False
            for name, value in cells.items():
                if value['action'] == 'equip' and not currents[name]:
                    cells[name]['keyline'] = 'r'
                    are_there_cells_to_clear = True
                    break
            if are_there_cells_to_clear:
                keys_list.append(self.keyline_for_cells(cells))
                keys_list.append('esc|esc|e')  # Re-enter to inventory.

        # 1. Performing actions for cells.
        self.assign_keylines_to_cells(cells, search_mode, currents)
        keys_list.append(self.keyline_for_cells(cells))

        # Making last cell handling little quicker if we can.
        last_cell_keyline = keys_list[-1]
        if last_cell_keyline.endswith('|q|pause200'):
            keys_list[-1] = keys_list[-1].replace('|q|pause200', '')

        # 2. Quiting menu.
        keys_list.append('esc')

        # 3. Instant action.
        if settings['instant_action']:
            if settings['instant_action'] == 'stance_attack':
                keys_list.append('skill|attack')
            elif settings['instant_action'] == 'stance_strong_attack':
                keys_list.append('skill|strong_attack')
            else:
                keys_list.append(settings['instant_action'])

        self.macro_keyline = '|'.join(keys_list)

    @staticmethod
    def keyline_for_cells(cells: dict) -> str:
        """
        Forms a general keyline for an ordered dict of inventory cells with
        their local keylines in ('keyline' key).
        """

        keys_list = []
        cells_to_handle = {}
        first_cell_key_to_handle = ''
        first_cell_index_to_handle = 0
        last_cell_key_to_handle = ''
        for key, value in cells.items():
            if value['keyline']:
                last_cell_key_to_handle = key
                if not first_cell_key_to_handle:
                    first_cell_key_to_handle = key
                cells_to_handle[key] = value
            if not first_cell_key_to_handle:
                first_cell_index_to_handle += 1

        # Shrinking a path if we have some big and frequent gaps of not-handling.
        # We call it "костыль" ("crutch") in Russia.
        # But here is important crutch.

        # Ignoring 2 and 3 weapon slots if they're not to equip.
        if cells['weapon_right_2']['keyline'] == '' \
                and cells['weapon_right_3']['keyline'] == '':
            cells['weapon_right_1']['action_after'] = 'down'
            cells['weapon_right_2']['action_after'] = ''
            cells['weapon_right_3']['action_after'] = ''

        if cells['weapon_left_2']['keyline'] == '' \
                and cells['weapon_left_3']['keyline'] == '':
            cells['weapon_left_1']['action_after'] = 'down'
            cells['weapon_left_2']['action_after'] = ''
            cells['weapon_left_3']['action_after'] = ''

        # Ignoring 2, 3 and 4 armor slots if they're not to equip.
        if cells['armor_chest']['keyline'] == '' \
                and cells['armor_arms']['keyline'] == '' \
                and cells['armor_legs']['keyline'] == '':
            cells['armor_head']['action_after'] = 'down'
            cells['armor_chest']['action_after'] = ''
            cells['armor_arms']['action_after'] = ''
            cells['armor_legs']['action_after'] = ''

        # Ignoring 2, 3 and 4 talisman slots if they're not to equip.
        if cells['talisman_2']['keyline'] == '' \
                and cells['talisman_3']['keyline'] == '' \
                and cells['talisman_4']['keyline'] == '':
            cells['talisman_1']['action_after'] = ''
            cells['talisman_2']['action_after'] = ''
            cells['talisman_3']['action_after'] = ''
            cells['talisman_4']['action_after'] = ''

        # Gather keylines from relevant cells and keys to move further.
        # TODO: дает пустую строку, когда 1 предмет в инвентаре
        for key, value in cells.items():
            if value['keyline']:
                keys_list.append(value['keyline'])
            if key == last_cell_key_to_handle:
                break
            if value['action_after']:
                keys_list.append(value['action_after'])

        return '|'.join(keys_list)

    @staticmethod
    def assign_keylines_to_cells(cells: dict, search_mode: str, currents: dict) -> None:
        """
        Generates a keyline to each cell in dict concidering it's inner
        settins. Puts a keyline to cell's 'keyline' key.
        """

        count = len(cells)
        pos_in_dict = 0

        for key, value in cells.items():

            pos_in_dict += 1

            if value['action'] == 'skip':
                continue
            elif value['action'] == 'remove':
                cells[key]['keyline'] = 'r'
                continue

            # Handling 'equip' action.
            keys_list = []

            if search_mode == 'auto':
                current_position = 1  # Standard position for "auto" mode.
            else:
                # If we're in "semi-manual" mode, we don't need to change items
                # if we already have it in our cell slots.
                current_position = currents[key]
                if current_position == value['position']:
                    continue

            goal_position = value['position']
            if not goal_position:
                continue   # Something strange happened, ignoring cell.

            # Forming a way from current position to goal position.
            # +1 cel:      right; -1 cell:    left
            # +5 cell:     down;  -5 cell:    up;
            # +25 cell:    v;    -25 cell:    c.
            path_list = []
            key_25_amount = key_5_amount = key_1_amount = 0
            key_25, key_5, key_1 = 'v', 'down', 'right'
            if goal_position < current_position:
                key_25, key_5, key_1 = 'c', 'up', 'left'

            diff = abs(goal_position - current_position)
            if diff // 25 > 0:
                key_25_amount = diff // 25
                diff = diff - key_25_amount * 25
            if diff // 5 > 0:
                key_5_amount = diff // 5
                diff = diff - key_5_amount * 5
            if diff > 0:
                key_1_amount = diff

            for _ in range(key_25_amount):
                path_list.append(key_25)
            for _ in range(key_5_amount):
                path_list.append(key_5)
            for _ in range(key_1_amount):
                path_list.append(key_1)

            # Entering cell.
            keys_list.append('e')

            # Going to goal cell.
            keys_list.append('|'.join(path_list))

            # Choosing equip.
            keys_list.append('e')
            if value['not_enough_stats']:
                keys_list.append('pause50|e|pause50')

            # Quiting cell.
            keys_list.append('q|pause200')

            cells[key]['keyline'] = '|'.join(keys_list)

            # Remembering current position in "semi-manual" mode.
            if search_mode != 'auto':
                currents[key] = goal_position

    def form_keyline_magic(self):
        settings = self.settings['magic']
        if not settings['spell_number']:
            return

        search_mode = self.saveslot.search_mode_magic
        cur_spell = self.saveslot.current_spell
        goal_spell = settings['spell_number']
        total_spells = len(self.saveslot.spells)
        print('Search mode -', search_mode)
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
            # But this nice thing is for semi-manual mode only.
            if search_mode == 'semi-manual' and cur_spell:
                needed_switches = goal_spell - cur_spell
                if cur_spell > goal_spell:
                    needed_switches = total_spells - cur_spell + goal_spell
                self.macro_keyline = '|switch_spell|pause10' * needed_switches
            else:
                # In auto mode we find first spell by pressing a button for
                # little bit and not bother.
                self.macro_keyline = f'switch_spell_press600{"|switch_spell|pause10" * (goal_spell - 1)}'

        # Add instant actions.
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
                    or command in available_buttons_with_codes() \
                    or command in non_letter_keys() \
                    or len(command) == 1 and command.isalpha() \
                    or command in []:
                keyline = command

            # Searching in built-in macros...
            if keyline == '':
                macro = next((x for x in built_in_macros() if
                              x['name'].lower() == command), None)
                if macro is not None:
                    keyline = macro['keyline']

            # Searching in other macros in this save-file...
            if keyline == '':
                for macro in self.saveslot.macros:
                    name = macro.name
                    if command.lower() == name.lower():
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

    def execute_keyline(self) -> None:
        """
        Parses a line into a keys and simulates key presses.
        Additional pause can be made with 'pauseN', where N is one thousandth sec.
        Additional press time can be made with 'pressN'.
        """

        window_title_before_executing = GetWindowText(GetForegroundWindow())

        keyline = self.macro_keyline
        print('Keyline: ', keyline)
        key_presses = keyline.split('|')

        # Execution.
        for i, key_press in enumerate(key_presses):

            sleep_time = self.pause_time / 1000

            # Checking every several keypress was window changed or not.
            # If changed: it's better to stop executing.
            if i % 4:
                window_title = GetWindowText(GetForegroundWindow())
                if window_title_before_executing != window_title:
                    print('Window changed. Macro execution was broken.')
                    break

            if self.interrupted:
                break

            # Additional pauses.
            if key_press.startswith('pause'):
                pause_time = int(key_press.replace('pause', ''))
                time.sleep(pause_time / 1000)
                continue

            # Pause after command.
            if '_pause' in key_press:
                    parts = key_press.partition('_pause')
                    sleep_time = int(parts[2].strip()) / 1000
                    key_press = parts[0].strip()

            # Additional press time.
            press_time = sleep_time
            if '_press' in key_press:
                parts = key_press.partition('_press')
                key_press = parts[0]
                press_time = int(parts[2]) / 1000

            # Turn actions ("guard", "strong_attack" etc.) to actions' keys.
            if key_press in self.savefile.game_controls.keys():
                key_for_message = key_press
                key_press = self.savefile.game_controls[key_press].lower()
                if key_for_message and not key_press:
                    print(f'Key "{key_for_message}" was not found in ER controls. Check Melina\'s Fingers settings.')
                    break

            # We'll just skip empty keys to not get to exception.
            if key_press.strip() == '':
                continue

            # TODO: need to understand, why 'keyboard' can't press arrows
            #  in game but 'pynput' can. Using two separate methods for input
            #  makes me feel silly.

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


def built_in_macros() -> list:
    """

    """

    macros_list = [
        {'name': 'Sort all: Asc. Acquisition',
         'keyline': keyline_to_sort_all_lists(),
         'comment': 'Sorts all lists that are used by Melina\'s Fingers to\n'
                    '"Order of Acquisition", ascended.\n'
                    '\n'
                    'It\'s very important hotkey due to the fact that equipment hotkeys\n'
                    'just won\'t work if lists are ordered differently.\n'
                    '\n'
                    'Press it once in the beginning of gaming session\n'
                    'and everything will be fine.\n'
                    '\n'
                    'By the way, "Order of Acquisition", Asc. is chosen due to two reasons:\n'
                    '   1) that\'s easiest order to be calculated via save file;\n'
                    '   2) it allows to pick up new weapons in PvE as new weapons go to\n'
                    '      the end of the list.'},
        {'name': 'Crouch attack',
         'keyline': 'crouch|attack',
         'comment': 'Everyone\'s hated button except UGS players before 1.07.'},
        {'name': 'Stance attack',
         'keyline': 'skill|attack',
         'comment': 'Goes to stance, then immediately perform an attack.'},
        {'name': 'Stance strong attack',
         'keyline': 'skill|strong_attack',
         'comment': 'Goes to stance, then immediately perform a strong attack.'},
        {'name': 'Fast katana stance attacks',
         'keyline': 'skill_press300|attack_pause1250|crouch_press20|crouch',
         'comment': 'Performs a skill attack and crouch to cancel a recovery\n'
                    'animation. It makes consecutive stance attacks much faster\n'
                    'and dangerous.\n'
                    '\n'
                    'How to use:\n'
                    '   - press a hotkey;\n'
                    '   - after stance attack is performed, press hotkey two times;\n'
                    '   - next stance attack will start as fast as possible.\n'
                    '\n'
                    'They hated you because you\'re Moonveil user, but now\n'
                    'you actually deserve this.'},
        {'name': 'Fast katana stance attacks (strong)',
         'keyline': 'skill_press300|strong_attack_pause1250|crouch_press20|crouch',
         'comment': 'Performs a strong skill attack and crouch to cancel a recovery\n'
                    'animation. It makes consecutive stance attacks much faster\n'
                    'and dangerous.\n'
                    '\n'
                    'How to use:\n'
                    '   - press a hotkey;\n'
                    '   - after stance attack is performed, press hotkey two times;\n'
                    '   - next stance attack will start as fast as possible.\n'
                    '\n'
                    'They hated you because you\'re Moonveil user, but now\n'
                    'you actually deserve this.'},
        {'name': 'Reverse backstep',
         'keyline': 'roll|pause15|move_down',
         'comment': 'Performs reverse backstep. Good for mixups and acting cool in PvP.\n'
                    '\n'
                    'Be like your favourite YouTube player without\n'
                    'practicing this finger breaking shit since DS3 beta.'},
        {'name': 'Next weapon (right)',
         'keyline': keyline_to_choose_next_weapon(),
         'comment': 'Chooses next weapon in list for right hand.\n'
                    '\n'
                    'You can choose 3 weapons for Right Hand Armament 1 slot\n'
                    'and play like Dante in classic weapon-juggling Devil May Cry style.'},
        {'name': 'Previous weapon (right)',
         'keyline': keyline_to_choose_previous_weapon(),
         'comment': 'Chooses previous weapon in list for right hand.\n'
                    '\n'
                    'You can choose 3 weapons for Right Hand Armament 1 slot\n'
                    'and play like Dante in classic weapon-juggling Devil May Cry style.'},
        {'name': 'Next weapon (left)',
         'keyline': keyline_to_choose_next_weapon(left_hand=True),
         'comment': 'Chooses next weapon in list for left hand.\n'
                    '\n'
                    'You can choose 3 weapons for Left Hand Armament 1 slot\n'
                    'and play like Vergil in classic weapon-juggling Devil May Cry style.'},
        {'name': 'Previous weapon (left)',
         'keyline': keyline_to_choose_previous_weapon(left_hand=True),
         'comment': 'Chooses previous weapon in list for left hand.\n'
                    '\n'
                    'You can choose 3 weapons for Left Hand Armament 1 slot\n'
                    'and play like Vergil in classic weapon-juggling Devil May Cry style.'},
        # TODO: Can I decrease pause4000?
        {'name': 'Six invasion attempts (wide)',
         'keyline': f'{keyline_to_invade_as_bloody_finger(True)}|pause4000|{keyline_to_invade_as_recusant(True)}|pause4000|' * 3,
         'comment': 'Performs an attempt to invade as bloody finger,\n'
                    'then attempt to invade as recusant, and so three times.\n'
                    '\n'
                    'Usually that\'s enough to invade even with mediocre connection\n'
                    'and get a snack from kitchen.\n'
                    '\n'
                    'Cannot be interrupted. Invades over all map.'},
        {'name': 'Six invasion attempts (local)',
         'keyline': f'{keyline_to_invade_as_bloody_finger()}|pause4000|{keyline_to_invade_as_recusant()}|pause4000' * 3,
         'comment': 'Performs an attempt to invade as bloody finger,\n'
                    'then attempt to invade as recusant, and so three times.\n'
                    '\n'
                    'Usually that\'s enough to invade even with mediocre connection\n'
                    'and get a snack from kitchen.\n'
                    '\n'
                    'Cannot be interrupted. Invades locally.'},
        {'name': 'Fast quit to main menu',
         'keyline': 'esc|up|e|z|e|left|e',
         'comment': 'Quits to main menu very fast.\n'
                    '\n'
                    'Useful if you lost to gravity but still want to cheat death.'}
    ]

    # Use item macros.
    for i in range(1, 11):
        macros_list.append({
            'name': f'Switch to quick item {str(i)}',
            'keyline': f'switch_item_press600{"|switch_item|pause10" * (i - 1)}',
            'comment': f'Selects item {i} from quick item list.'
        })

    # Switch to spell macros.
    for i in range(1, 13):
        macros_list.append({
            'name': f'Switch to spell {str(i)}',
            'keyline': f'switch_spell_press600{"|switch_spell|pause10" * (i - 1)}',
            'comment': f'Selects spell {i} from spell list.'
        })

    # 6 gestures.
    for i in range(1, 7):
        downs = (i - 1) // 2
        rights = (i - 1) % 2
        macros_list.append({
            'name': f'Gesture {str(i)}',
            'keyline': f'esc|right|down|down|down{"|down" * downs}{"|right" * rights}|e|esc',
            'comment': f'Performs gesture {i}.'
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
              'down|e|t|down|e|pause300|esc'
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


def keyline_to_choose_next_weapon(weapons_pass: int = 0,
                                  left_hand=False) -> str:
    """
    Returns a macro keyline that chooses next weapon.
    :param weapons_pass: how many weapons will be passed before choosing.
    """

    right_amount = weapons_pass + 1

    keyline = f'esc|e|{"down|" if left_hand else ""}e|{"right|" * right_amount}pause20|e|esc'
    return keyline


def keyline_to_choose_previous_weapon(weapons_pass: int = 0,
                                      left_hand=False) -> str:
    """
    Returns a macro keyline that chooses previous weapon.
    :param weapons_pass: how many weapons will be passed before choosing.
    """

    left_amount = weapons_pass + 1

    keyline = f'esc|e|{"down|" if left_hand else ""}e|{"left|" * left_amount}pause20|e|esc'

    return keyline
