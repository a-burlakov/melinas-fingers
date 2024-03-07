"""
Macros settings and execution.
"""

import traceback
import time
from win32gui import GetWindowText, GetForegroundWindow
import keyboard
from pynput import keyboard as pynput_keyboard

from constants.keyboard import game_control_keys, available_buttons_with_codes, non_letter_keys
from constants.macros import built_in_macros
from services.savefile import SaveSlot

pynput_in = pynput_keyboard.Controller()


class Macro:
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
        self.recovery_hotkey: str = ''
        self.pause_time: int = 20
        self.macro_keyline: str = ''
        self.settings = {
            'equipment': {
                'instant_action': '',
                'two_handing': '',
                'weapon_right_1': {
                    'action': 'skip',
                    'not_enough_stats': False,
                    'name': '',
                    'position': 0,
                },
                'weapon_right_2': {
                    'action': 'skip',
                    'not_enough_stats': False,
                    'name': '',
                    'position': 0,
                },
                'weapon_right_3': {
                    'action': 'skip',
                    'not_enough_stats': False,
                    'name': '',
                    'position': 0,
                },
                'weapon_left_1': {
                    'action': 'skip',
                    'not_enough_stats': False,
                    'name': '',
                    'position': 0,
                },
                'weapon_left_2': {
                    'action': 'skip',
                    'not_enough_stats': False,
                    'name': '',
                    'position': 0,
                },
                'weapon_left_3': {
                    'action': 'skip',
                    'not_enough_stats': False,
                    'name': '',
                    'position': 0,
                },
                'armor_head': {
                    'action': 'skip',
                    'not_enough_stats': False,
                    'name': '',
                    'position': 0,
                },
                'armor_chest': {
                    'action': 'skip',
                    'not_enough_stats': False,
                    'name': '',
                    'position': 0,
                },
                'armor_arms': {
                    'action': 'skip',
                    'not_enough_stats': False,
                    'name': '',
                    'position': 0,
                },
                'armor_legs': {
                    'action': 'skip',
                    'not_enough_stats': False,
                    'name': '',
                    'position': 0,
                },
                'talisman_1': {
                    'action': 'skip',
                    'not_enough_stats': False,
                    'name': '',
                    'position': 0,
                },
                'talisman_2': {
                    'action': 'skip',
                    'not_enough_stats': False,
                    'name': '',
                    'position': 0,
                },
                'talisman_3': {
                    'action': 'skip',
                    'not_enough_stats': False,
                    'name': '',
                    'position': 0,
                },
                'talisman_4': {
                    'action': 'skip',
                    'not_enough_stats': False,
                    'name': '',
                    'position': 0,
                },
            },
            'magic': {
                'spell_number': 1,
                'instant_cast_right': False,
                'instant_cast_left': False,
            },
            'items': {'item_number': 1, 'instant_use': False},
            'built-in': {'macro_name': built_in_macros()[0]['name']},
            'diy': {'macro': '', 'times_to_repeat': 1},
        }

    def __str__(self):

        return f'{self.name} ({self.hotkey_string()})'

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

    @staticmethod
    def standard_name():
        return '< hotkey name >'

    def set_id(self):
        """
        Sets an id to macro. Format is like '7023', where '7' is saveslot
        number and 23 - just macro order number.
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

    def execute(self):
        """
        That's a function that is called when assigned hotkey is pressed.
        It forms a keyline from macro settings and then turns this keyline
        to virtual keyboard presses.
        """

        time_start = time.time()

        self.savefile.make_journal_entry('=' * 40)
        self.savefile.make_journal_entry(f'Start: {self}')

        # Nobody knows what can happen inside keylines mechanism
        # (especially with DIYs), so we need exceptions catch.
        try:
            self.form_keyline()
            self.execute_keyline()
        except Exception:
            self.savefile.make_journal_entry(str(traceback.format_exc()))

        time_end = time.time()

        self.savefile.make_journal_entry(f'End: {self}')
        self.savefile.make_journal_entry(f'Duration: {str(round(time_end - time_start, 5))}')
        self.savefile.make_journal_entry('-' * 40)

    def form_keyline(self):
        """
        Forms a keyline string from macro settings to be executed in
        'execute_keyline' function.
        """

        if self.type == 'Equipment':
            self.form_keyline_equipment()
        elif self.type == 'Magic':
            self.form_keyline_magic()
        elif self.type == 'Items':
            self.form_keyline_items()
        elif self.type == 'Built-in':
            self.form_keyline_builtin()
        elif self.type == 'DIY':
            self.form_keyline_diy()

    def form_keyline_equipment(self):

        keys_list = []  # list to be turned to keyline

        settings = self.settings['equipment']
        search_mode = self.saveslot.search_mode_equipment

        cells = [
            'weapon_right_1',
            'weapon_right_2',
            'weapon_right_3',
            'weapon_left_1',
            'weapon_left_2',
            'weapon_left_3',
            'armor_head',
            'armor_chest',
            'armor_arms',
            'armor_legs',
            'talisman_1',
            'talisman_2',
            'talisman_3',
            'talisman_4',
        ]

        cells = {x: settings[x] for x in cells}
        if all(cell['action'] == 'skip' for cell in cells.values()):
            self.macro_keyline = ''
            return

        # Actions to do after cell is passed to get to next cell.
        # Also put a key 'keyline' which will keep a keyline to handle a cell.
        actions_after_cell = [
            'right',
            'right',
            'left|left|down',
            'right',
            'right',
            'left|left|down',
            'right',
            'right',
            'right',
            'right|down',
            'right',
            'right',
            'right',
            'right|down',
        ]
        for cell, action_after in zip(cells.keys(), actions_after_cell):
            cells[cell]['action_after'] = action_after
            cells[cell]['keyline'] = ''

        # Plan is simple, that's a Swiss f*cking watch:
        #   0. firstly we clear all cells to 'remove' or 'equip' if needed
        #   1. cycle through all cells and if it's 'remove' or 'equip', perform
        #       corresponding action;
        #   2. when 'remove' and 'equip' cells are out, we're pressing "Esc";
        #   3. if we have two-handing or instant action - performing it.

        keys_list.append('esc|e|pause50')  # Open inventory.

        # 0. Preliminary clearing if "Auto" search mode.
        if search_mode == 'auto':

            for name, value in cells.items():
                if value['action'] in ['equip', 'remove']:
                    cells[name]['keyline'] = 'r'

            keys_list.append(self.keyline_for_cells(cells))

            # Re-enter to inventory.
            keys_list.append('esc|esc|e|pause50')

        # 0.1. If we're in manual mode, but have some cells to 'equip' having
        # no current position, that means we need to clear them to put to
        # position 1.
        currents = self.saveslot.current_equipment
        if search_mode == 'semi-manual':
            are_there_cells_to_clear = False
            for name, value in cells.items():
                if value['action'] == 'equip' and not currents[name]:
                    cells[name]['keyline'] = 'r'
                    are_there_cells_to_clear = True

            if are_there_cells_to_clear:
                keys_list.append(self.keyline_for_cells(cells))
                keys_list.append('esc|esc|e|pause50')  # Re-enter to inventory.

        # Clearing keylines.
        for name in cells.keys():
            cells[name]['keyline'] = ''

        # 1. Performing actions for cells.
        self.assign_keylines_to_cells(cells, search_mode, currents)
        keys_list.append(self.keyline_for_cells(cells))

        # Making last cell handling little quicker if we can.
        last_quit_piece = '|q|pause200'
        last_cell_keyline = keys_list[-1]
        if last_cell_keyline.endswith(last_quit_piece):
            keys_list[-1] = keys_list[-1][: -len(last_quit_piece)]

        # 2. Quiting menu.
        keys_list.append('esc')

        # 3. Two-handing and instant action.
        if settings['two_handing'] == 'right_weapon':
            keys_list.append('event_action+attack')
        elif settings['two_handing'] == 'left_weapon':
            keys_list.append('event_action+guard')

        if settings['instant_action']:
            if settings['instant_action'] == 'stance_attack':
                instant_action = 'skill|attack'
            elif settings['instant_action'] == 'stance_strong_attack':
                instant_action = 'skill|strong_attack'
            else:
                instant_action = settings['instant_action']

            if instant_action:
                # Making a pause after two-handing a weapon to not perform
                # instant action during two-handing animation.
                if settings['two_handing']:
                    keys_list.append('pause200')
                keys_list.append(instant_action)

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

        # Shrinking a path if we have some big and frequent
        # gaps of not-handling.
        # We call it "костыль" ("crutch") in Russia.
        # But this crutch is important.

        # Ignoring 2 and 3 weapon slots if they're not to equip.
        if (
            cells['weapon_right_2']['action'] == 'skip'
            and cells['weapon_right_3']['action'] == 'skip'
        ):
            cells['weapon_right_1']['action_after'] = 'down'
            cells['weapon_right_2']['action_after'] = ''
            cells['weapon_right_3']['action_after'] = ''

        if (
            cells['weapon_left_2']['action'] == 'skip'
            and cells['weapon_left_3']['action'] == 'skip'
        ):
            cells['weapon_left_1']['action_after'] = 'down'
            cells['weapon_left_2']['action_after'] = ''
            cells['weapon_left_3']['action_after'] = ''

        # Ignoring 2, 3 and 4 armor slots if they're not to equip.
        if (
            cells['armor_chest']['action'] == 'skip'
            and cells['armor_arms']['action'] == 'skip'
            and cells['armor_legs']['action'] == 'skip'
        ):
            cells['armor_head']['action_after'] = 'down'
            cells['armor_chest']['action_after'] = ''
            cells['armor_arms']['action_after'] = ''
            cells['armor_legs']['action_after'] = ''

        # Ignoring 2, 3 and 4 talisman slots if they're not to equip.
        if (
            cells['talisman_2']['keyline'] == ''
            and cells['talisman_3']['keyline'] == ''
            and cells['talisman_4']['keyline'] == ''
        ):
            cells['talisman_1']['action_after'] = ''
            cells['talisman_2']['action_after'] = ''
            cells['talisman_3']['action_after'] = ''
            cells['talisman_4']['action_after'] = ''

        # Gather keylines from relevant cells and keys to move further.
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
        Generates a keyline inside each cell in ordered dict concidering
        cell's inner settings. Puts a keyline to cell's 'keyline' key.
        """

        count = len(cells)
        pos_in_dict = 0

        for key, value in cells.items():

            pos_in_dict += 1

            if value['action'] == 'skip':
                continue
            elif value['action'] == 'remove':
                cells[key]['keyline'] = 'r'
                if search_mode == 'semi-manual':
                    currents[key] = 0
                continue

            # Handling 'equip' action.
            keys_list = []

            current_position = 0

            # Standard position for "auto" mode is 1.
            if search_mode == 'auto':
                current_position = 1

            # If we're in "semi-manual" mode, we don't need to change items
            # if we already have it in our cell slots.
            if search_mode == 'semi-manual':
                goal_position = value['position']
                something_chosen_already = currents[key] > 0

                if something_chosen_already:
                    current_position = currents[key]
                else:
                    current_position = 1

                if something_chosen_already and current_position == goal_position:
                    continue

            goal_position = value['position']
            if not goal_position:
                continue  # Something strange happened, ignoring cell.

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
            keys_list.append('e|pause50')

            # Going to goal cell.
            keys_list.append('|'.join(path_list))

            # Choosing equip.
            keys_list.append('e')
            if value['not_enough_stats']:
                keys_list.append('pause50|e|pause200')

            # Quiting cell.
            keys_list.append('q|pause200')

            cells[key]['keyline'] = '|'.join(keys_list)

            # Remembering current position in "semi-manual" mode.
            if search_mode == 'semi-manual':
                currents[key] = goal_position

    def form_keyline_magic(self):

        settings = self.settings['magic']
        if not settings['spell_number']:
            return

        search_mode = self.saveslot.search_mode_magic.lower()
        cur_spell = self.saveslot.current_spell
        goal_spell = settings['spell_number']
        total_spells = len(self.saveslot.spells)
        self.savefile.make_journal_entry(
            f'Search mode - {search_mode}\n'
            f'Total spells - {total_spells}\n'
            f'Current spell - {cur_spell}\n'
            f'Goal spell - {goal_spell}'
        )

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
                self.macro_keyline = self.macro_keyline[1:]
            else:
                # In auto mode we find first spell by pressing a button for
                # little bit and not bother too much.
                self.macro_keyline = (
                    f'switch_spell_press600{"|switch_spell|pause10" * (goal_spell - 1)}'
                )

        # Add instant actions.
        if settings['instant_cast_right']:
            self.macro_keyline += '|attack'
        if settings['instant_cast_left']:
            self.macro_keyline += '|guard'

        # Set current number for next macro uses.
        if search_mode == 'semi-manual':
            self.saveslot.current_spell = settings['spell_number']

        self.savefile.make_journal_entry(f'Current spell now - {self.saveslot.current_spell}')

    def form_keyline_items(self):

        settings = self.settings['items']
        if not settings['item_number']:
            return

        search_mode = self.saveslot.search_mode_items.lower()
        cur_item = self.saveslot.current_item
        goal_item = settings['item_number']
        total_items = len(self.saveslot.items)
        self.savefile.make_journal_entry(
            f'Search mode - {search_mode}\n'
            f'Total items - {total_items}\n'
            f'Current item - {cur_item}\n'
            f'Goal item - {goal_item}'
        )

        # If current item is item we need, then we just need to
        # check "instant cast" afterwards.
        items_equal = False
        if cur_item == goal_item:
            self.macro_keyline = ' '
            items_equal = True

        if not items_equal:
            # If we know what item we're having right now then we save
            # time if not pressing 'switch_item' for half sec and
            # calculate amount of keypresses to just switch to item from macro.
            # But this nice thing is for semi-manual mode only.
            if search_mode == 'semi-manual' and cur_item:
                needed_switches = goal_item - cur_item
                if cur_item > goal_item:
                    needed_switches = total_items - cur_item + goal_item
                self.macro_keyline = '|switch_item|pause10' * needed_switches
            else:
                # In auto mode we find first item by pressing a button for
                # little bit and not bother too much.
                self.macro_keyline = (
                    f'switch_item_press600{"|switch_item|pause10" * (goal_item - 1)}'
                )

        # Add instant actions.
        if settings['instant_use']:
            self.macro_keyline += '|use_item'

        # Set current number for next macro uses.
        if search_mode == 'semi-manual':
            self.saveslot.current_item = settings['item_number']

        self.savefile.make_journal_entry(f'Current item now - {self.saveslot.current_item}')

    def form_keyline_builtin(self):

        built_in_macro_name = self.settings['built-in']['macro_name']
        built_in_macro = next(x for x in built_in_macros() if x['name'] == built_in_macro_name)

        self.macro_keyline = built_in_macro['keyline']

    def form_keyline_diy(self):

        commands_list = self.settings['diy']['macro'].strip().split('\n')
        keyline_list = []
        for command in commands_list:

            keyline = ''
            command = command.strip().lower()

            if not command:
                continue

            # Commentary.
            if command.startswith('#'):
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

            if len(command) > 1 and '+' in command:
                keyline = command

            # Searching in plain buttons...
            if (
                command in game_control_keys()
                or command in available_buttons_with_codes()
                or command in non_letter_keys()
                or len(command) == 1
                and command.isalpha()
                or command in []
            ):
                keyline = command

            # Searching in built-in macros...
            if keyline == '':
                macro = next((x for x in built_in_macros() if x['name'].lower() == command), None)
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

        if self.settings['diy']['times_to_repeat']:
            keyline_list = keyline_list * self.settings['diy']['times_to_repeat']

        self.macro_keyline = '|'.join(keyline_list)

    def execute_keyline(self) -> None:
        """
        Parses a line into a keys and simulates key presses.
        """

        keyline = self.macro_keyline
        self.savefile.make_journal_entry(f'Keyline: {keyline}')
        key_presses = keyline.split('|')
        key_presses = filter(lambda x: x.strip() != '', key_presses)
        window_title_before_executing = GetWindowText(GetForegroundWindow()).lower()

        game_is_open = False

        if (
            'elden' in window_title_before_executing
            and 'ring' in window_title_before_executing
            and len(window_title_before_executing) < 15
        ):
            game_is_open = True
        elif (
            'dark' in window_title_before_executing
            and 'souls' in window_title_before_executing
            and len(window_title_before_executing) < 15
        ):
            game_is_open = True

        if not game_is_open:
            self.savefile.make_journal_entry(
                f'Hotkey "{self}" not started because game is not open. ("{GetWindowText(GetForegroundWindow())}" is open.)'
            )
            return

        sleep_time = self.pause_time / 1000

        # Execution.
        for i, key_press in enumerate(key_presses):

            sleep_time = self.pause_time / 1000

            # Checking every several keypress was window changed or not.
            # If changed: it's better to stop executing.
            if i % 4:
                window_title = GetWindowText(GetForegroundWindow()).lower()
                if window_title_before_executing != window_title:
                    self.savefile.make_journal_entry(
                        f'Window changed to "{GetWindowText(GetForegroundWindow())}". Hotkey "{self}" execution was broken.'
                    )
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

            # If we have an expression like 'guard+a+home', that's a command
            # to press these keys simultaneously. We need to put these keys in
            # a list and handle them separately.
            keys_list = []
            if len(key_press) > 1 and '+' in key_press:
                keys_list = key_press.split('+')
            else:
                keys_list.append(key_press)

            # We'll just skip empty keys to not get to exception.
            for key_press in keys_list:
                if key_press.strip() == '':
                    self.savefile.make_journal_entry('Had an empty key press, so it was skipped.')
                    continue

            # Turn actions ("guard", "strong_attack" etc.) to actions' keys.
            for i, key_press in enumerate(keys_list):
                if key_press in self.savefile.game_controls.keys():
                    key_for_message = key_press
                    key_press = self.savefile.game_controls[key_press].lower()
                    if key_for_message and not key_press:
                        self.savefile.make_journal_entry(
                            f'Key "{key_for_message}" was not found in ER controls. Check Melina\'s Fingers settings.'
                        )
                        break
                    else:
                        keys_list[i] = key_press

            # Key presses execution.
            # Presses are made sometimes with 'keyboard' and sometimes with
            # 'pynput' as pynput can press more keys but do it less stable
            # stan 'keyboard', according to my feelings.
            keys_for_pynput = [
                'up',
                'left',
                'right',
                'down',
                'num0',
                'num1',
                'num2',
                'num3',
                'num4',
                'num5',
                'num6',
                'num7',
                'num8',
                'num9',
            ]

            for i, key_press in enumerate(keys_list):
                if key_press in keys_for_pynput:
                    if key_press in non_letter_keys():
                        keys_list[i] = pynput_keyboard.Key[key_press]
                    elif len(key_press) == 4 and key_press.startswith('num'):
                        num_number = int(key_press[-1])
                        keys_list[i] = pynput_keyboard.KeyCode(96 + num_number)

            for key_press in keys_list:
                if hasattr(key_press, 'vk') or (
                    hasattr(key_press, 'value') and hasattr(key_press, 'name')
                ):
                    pynput_in.press(key_press)
                else:
                    keyboard.press(key_press)

            time.sleep(press_time)

            for key_press in keys_list:
                if hasattr(key_press, 'vk') or (
                    hasattr(key_press, 'value') and hasattr(key_press, 'name')
                ):
                    pynput_in.release(key_press)
                else:
                    keyboard.release(key_press)

            time.sleep(sleep_time)

        time.sleep(sleep_time)
