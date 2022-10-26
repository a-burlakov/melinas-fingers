"""

"""
import time
from pynput.keyboard import Key, Controller
import keyboard
from savefile import SaveSlot
from win32gui import GetWindowText, GetForegroundWindow

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
        # TODO: Need to find a way to use this numpad buttons, may be with pynput library.
        # "Num0",
        # "Num1Num1",
        # "Num2",
        # "Num3",
        # "Num4",
        # "Num5",
        # "Num6",
        # "Num7",
        # "Num8",
        # "Num9",
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
        '[',
        ']',
        ';',
        '\'',
        ',',
        '.',
        '/',
        '-',
        '=',
        # "~" somehow tilda causing problems
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
                                   'name': '', 'position': 0, 'current_position': 0},
                'weapon_right_2': {'action': 'skip', 'not_enough_stats': False,
                                   'name': '', 'position': 0, 'current_position': 0},
                'weapon_right_3': {'action': 'skip', 'not_enough_stats': False,
                                   'name': '', 'position': 0, 'current_position': 0},
                'weapon_left_1': {'action': 'skip', 'not_enough_stats': False,
                                  'name': '', 'position': 0, 'current_position': 0},
                'weapon_left_2': {'action': 'skip', 'not_enough_stats': False,
                                  'name': '', 'position': 0, 'current_position': 0},
                'weapon_left_3': {'action': 'skip', 'not_enough_stats': False,
                                  'name': '', 'position': 0, 'current_position': 0},
                'armor_head': {'action': 'skip', 'not_enough_stats': False,
                               'name': '', 'position': 0, 'current_position': 0},
                'armor_chest': {'action': 'skip', 'not_enough_stats': False,
                                'name': '', 'position': 0, 'current_position': 0},
                'armor_arms': {'action': 'skip', 'not_enough_stats': False,
                                'name': '', 'position': 0, 'current_position': 0},
                'armor_legs': {'action': 'skip', 'not_enough_stats': False,
                               'name': '', 'position': 0, 'current_position': 0},
                'talisman_1': {'action': 'skip', 'not_enough_stats': False,
                               'name': '', 'position': 0, 'current_position': 0},
                'talisman_2': {'action': 'skip', 'not_enough_stats': False,
                               'name': '', 'position': 0, 'current_position': 0},
                'talisman_3': {'action': 'skip', 'not_enough_stats': False,
                               'name': '', 'position': 0, 'current_position': 0},
                'talisman_4': {'action': 'skip', 'not_enough_stats': False,
                               'name': '', 'position': 0, 'current_position': 0}
            },
            'magic': {
                'spell_number': 1,
                'current_number': 0,
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

        # TODO: не забыть вернуть
        current_window_text: str = (GetWindowText(GetForegroundWindow()))
        # if 'elden' not in current_window_text.lower():  # \
        #     # and 'melina' not in current_window_text.lower():
        #     return

        self.interrupted = False
        time_start = time.time()
        print('=' * 40)
        print('Macro:   ',
              f'#{self.id} ({self.type}) ({self.hotkey_string()}) {self.name}')
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
        actions_after_cell = ['right', 'right', 'right|down',
                              'right', 'right', 'right|down',
                              'right', 'right', 'right', 'right|down',
                              'right', 'right', 'right', 'right|down']
        for cell, action_after in zip(cells.keys(), actions_after_cell):
            cells[cell]['action_after'] = action_after
            cells[cell]['keyline'] = ''

        # TODO: комментарии подправить
        # Plan is simple, that's a Swiss f*cking watch:
        #   0. if we're on "Auto" search mode, then firstly we clear all cells
        #       to 'remove' or 'equip'; press "Q; press "E" again to return;
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
        if search_mode != 'auto':
            are_there_cells_to_clear = False
            for name, value in cells.items():
                if value['action'] == 'equip' and not value['current_position']:
                    cells[name]['keyline'] = 'r'
                    are_there_cells_to_clear = True
            if are_there_cells_to_clear:
                keys_list.append(self.keyline_for_cells(cells))

                # Re-enter to inventory.
                keys_list.append('esc|esc|e')

        # 1-2. Performing actions for cells.
        self.assign_keylines_to_cells(cells, search_mode)
        keys_list.append(self.keyline_for_cells(cells))

        # Quit menu.
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

        # Seeking first cell to handle in full list and try to shrink
        # a path from beginning to first cell if it's possible. It's handy
        # if we handle far cells only, like 'talisman_3'.
        path_to_first_cell = []
        for key, value in cells.items():
            if key == first_cell_key_to_handle:
                break
            if value['action_after']:
                path_to_first_cell.append(value['action_after'])

        path_to_first_cell = '|'.join(path_to_first_cell)

        # TODO: Сделать так, чтобы пропускались первые правое 2 и 3 оружие, если надо
        # TODO: ошибка с тем, что я не учитываю стрелы с права
        # TODO: ошибка с тем, что первые ячейки не работают
        # TODO: расходится порядок в броне...

        # Shinking the path to 'talisman_1' from 13 to 3 press.
        path_to_first_cell = path_to_first_cell.replace(
            'right|right|right|down|'
            'right|right|right|down|'
            'right|right|right|right|down',
            'down|down|down'
        )
        # Shinking the path to 'armor_head' from 8 to 2 presses.
        #                   or 'weapon_left_1' from 4 to 1 press.
        path_to_first_cell = path_to_first_cell.replace(
            'right|right|right|down',
            'down'
        )

        # Replacing first sequence of not relevant cells to short path to first
        # relevant one, if we can.
        if path_to_first_cell:
            keys_list.append(path_to_first_cell)
            cells = {k: v for i, (k, v) in enumerate(cells.items())
                     if i >= first_cell_index_to_handle}

        # Gather keylines from relevant cells and keys to move further.
        for key, value in cells.items():
            if value['keyline']:
                keys_list.append(value['keyline'])
            if key == last_cell_key_to_handle:
                break
            keys_list.append(value['action_after'])

        return '|'.join(keys_list)

    @staticmethod
    def assign_keylines_to_cells(cells: dict, search_mode: str) -> None:
        """
        Generates a keyline to each cell in dict concidering it's inner
        settins. Puts a keyline to cell's 'keyline' key.
        """

        for key, value in cells.items():

            if value['action'] == 'skip':
                continue
            elif value['action'] == 'remove':
                cells[key]['keyline'] = 'r'
                continue

            # Handling 'equip' action.
            keys_list = []

            current_position = 1  # Standard position for auto mode

            # If we're in "semi-manual" mode, we don't need to change items
            # if we already have it in our cell slots.
            if search_mode != 'auto':
                current_position = value['current_position']
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
                value['current_position'] = current_position

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
                    or command in available_hotkey_buttons() \
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

            # We'll just skip empty keys to not get to exception.
            if key_press.strip() == '':
                continue

            # TODO: need to understand, why 'keyboard' can't press arrows
            #  in game but 'pynput' can. Using two separate methods for input
            #  makes me feel silly.

            # Key presses execution.
            keys_for_pynput = {'up': 72, 'left': 75, 'right': 80, 'down': 77}
            if key_press in keys_for_pynput:
                key_press = keyboard.key_to_scan_codes(key_press)
            #     if key_press in non_letter_keys():
            #         key_press = Key[key_press]
            #     pynput_in.press(key_press)
            #     time.sleep(press_time)
            #     pynput_in.release(key_press)
            # else:
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
         'comment': 'Favourite UGS players\' button before 1.07.'},
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
         'keyline': 'roll|pause5|move_down',
         'comment': 'Performs reverse backstep. Good for mixups and acting cool in PvP.\n'
                    '\n'
                    'Be like your favourite YouTube player without\n'
                    'practicing this finger breaking shit since DS3 beta.'},
        {'name': 'Next weapon (right)',
         'keyline': keyline_to_choose_next_weapon(),
         'comment': 'Chooses next weapon in list for right hand.\n'
                    '\n'
                    'Acts like mouse wheel in old school shooters.'},
        {'name': 'Previous weapon (right)',
         'keyline': keyline_to_choose_previous_weapon(),
         'comment': 'Chooses previous weapon in list for right hand.\n'
                    '\n'
                    'Acts like mouse wheel in old school shooters.'},
        {'name': 'Next weapon (left)',
         'keyline': keyline_to_choose_next_weapon(left_hand=True),
         'comment': 'Chooses next weapon in list for left hand.\n'
                    '\n'
                    'Acts like mouse wheel in old school shooters.'},
        {'name': 'Previous weapon (left)',
         'keyline': keyline_to_choose_previous_weapon(left_hand=True),
         'comment': 'Chooses previous weapon in list for left hand.\n'
                    '\n'
                    'Acts like mouse wheel in old school shooters.'},
        # TODO: Посмотреть, можно ли уменьшить 4000
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
    ]

    # Use item macros.
    for i in range(1, 11):
        macros_list.append({
            'name': f'Switch to quick item {str(i)}',
            'keyline': f'switch_item_press600{"|switch_item|pause10" * (i - 1)}|use_item',
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
