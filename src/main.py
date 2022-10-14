import os
import re
import savefile_structure
import datasheets
import time
from pynput.keyboard import Key, Controller, Listener
import keyboard
import pyautogui

from win32gui import GetWindowText, GetForegroundWindow


def get_savefile_path() -> str:
    """
    Returns the path to the relevant Elden Ring save file.

    :return: Path as string
    """
    return os.getcwd() + '\\test\ER0000_freedom_13102022.sl2'
    # return os.getcwd() + '\\test\ER0000_freedom_all_weapoms_inventory.sl2'
    # return os.getcwd() + '\\test\ER0000_freedom_all_in_chest.sl2'
    # return os.getcwd() + '\\test\ER0000_freedom_something_in_inventory.sl2'


def get_slot_data(filepath: str, save_slot_number: int) -> bytes:
    """
    Returns hex data of save file related to specific save slot.

    :param filepath: path to savefile
    :param save_slot_number: number of specific save slot (begins with "1")
    :return:
    """
    with open(filepath, "rb") as fh:
        data = fh.read()
        slot_interval = savefile_structure.slot_ranges(save_slot_number)

        return data[slot_interval[0]:slot_interval[1]]


def get_slot_names(file) -> list:
    """

    :param file:
    :return:
    """
    try:
        with open(file, "rb") as fh:
            data = fh.read()

    except FileNotFoundError as e:
        return False

    names_ranges = savefile_structure.slot_names_ranges()
    names = [data[x: y].decode('utf-16') for x,y in names_ranges]

    for i, name in enumerate(names):
        if name == '\x00' * 16:
            names[i] = None
        else:
            names[i] = name.split('\x00')[0]

    return names


def endian_turnoff(hex: str) -> str:
    """
    Turns little-endian hex string to big-endian or visa versa,
    Example: 8097FA01 <-> 01FA9780

    :param hex: hex string
    :return: None
    """

    if len(hex) < 2:
        return hex

    if len(hex) % 2 == 1:
        return hex

    pairs = [hex[i:i + 2] for i in range(0, len(hex), 2)]

    return ''.join(reversed(pairs))


def item_id_as_hex(item_id: str) -> str:
    """

    :param item_id:
    :return:
    """

    needed_length = 8
    hex_big_endian = hex(int(item_id))[2:]
    if len(hex_big_endian) % 2 == 1:
        hex_big_endian = '0' + hex_big_endian
    hex_little_endian = endian_turnoff(hex_big_endian)
    hex_little_endian += (needed_length - len(hex_little_endian))*'0'

    return hex_little_endian


def add_escaping_character_to_byte_reg(reg_expression: bytes) -> bytes:
    """

    :param reg_expression:
    :return:
    """

    escaping_characters = [b'\\', b'[', b']', b'(', b')', b'|',
                           b'^', b'$', b'.', b'?', b'*', b'+']
    for ch in escaping_characters:
        reg_expression = reg_expression.replace(ch, b'\\' + ch)

    return reg_expression


def get_inventory_weapons():
    """
    code keeper
    :return:
    """

    slot_number: int = 1
    path = get_savefile_path()
    slot_data = get_slot_data(path, slot_number)

    # Looking for all weapons mentioned in save-file, whatever quantity
    # and position in inventory or chest.
    slot_data_for_weapons_search = slot_data[:]
    datasheet_weapons = datasheets.weapons()
    all_weapons_having = []
    for weapon in datasheet_weapons:
        weapon_id = weapon[1]
        weapon_name = weapon[2]

        # if 'Moonveil' not in weapon_name:
        #     continue

        if bytes.fromhex(weapon_id) in slot_data[:0x00030000]:
            all_weapons_having.append([weapon_name, weapon_id])

    # Looking for many instances of each weapon. In save-file structure
    # is like this: [inventory instances]-[separator]-[chest instances]
    # We need only inventory instances.
    instances_range = savefile_structure.weapons_search_range()
    data_for_instances_search = slot_data[instances_range[0]:
                                          instances_range[1]]
    separator = savefile_structure.inventory_and_chest_separator()
    separator_pos = data_for_instances_search.find(separator)

    inventory_list = []
    for weapon in all_weapons_having:
        weapon_name = weapon[0]
        weapon_id = weapon[1]

        # In save-file we're looking for lines like: ID ID 80 80 WW WW WW WW
        # Where:
        #   ID ID - ID of specific instance of a weapon
        #   80 80 - mark of a weapon
        #   WW WW WW WW - weapon ID
        # Each line represents an instance of a weapon.
        id_for_reg = bytes.fromhex('8080' + weapon_id)
        id_for_reg = add_escaping_character_to_byte_reg(id_for_reg)
        reg_expression = b'.{2}(?=' + id_for_reg + b')'

        result = re.finditer(reg_expression,
                             slot_data[:instances_range[0] + separator_pos])

        for match in result:

            instance_id = match.group() + bytes.fromhex('8080')
            instance_position = data_for_instances_search.find(instance_id)
            if instance_position < 0:
                continue

            # As we found instance's ID, we can see, in what part this ID
            # is located. If it's in inventory part, then that's it!
            if instance_position > separator_pos:
                continue

            instance_id = instance_id.hex(' ').replace(' ', '')
            position_in_file = hex(instances_range[0]
                                   + instance_position
                                   + savefile_structure.range_before_save_slots())

            # Instance's ID is located in line that looks like:
            # ID ID 80 80 XX XX XX XX NN NN
            # Where:
            #   ID ID - instance's ID
            #   80 80 XX XX XX XX - not interesting data
            #   NN NN - additional ID that can be used to learn what order in
            #   inventory this instance has.
            inventory_order_id = data_for_instances_search[
                                 instance_position + 8:
                                 instance_position + 10]
            inventory_order_id = inventory_order_id.hex(' ').replace(' ', '')

            # Order ID has two HEX numbers ("f1 21") but actual order goes
            # on mirrored numbers ("21 f1", "21 f2", "21 f3" etc.)
            inventory_order_id = inventory_order_id[2:4] \
                                 + inventory_order_id[:2]

            instance_dict = {}
            instance_dict.setdefault('weapon_name', weapon_name)
            instance_dict.setdefault('weapon_id', weapon_id)
            instance_dict.setdefault('instance_id', instance_id)
            instance_dict.setdefault('inventory_order_id', inventory_order_id)
            instance_dict.setdefault('position', position_in_file)
            inventory_list.append(instance_dict)

    print(*sorted(inventory_list,
                  key=lambda x: int(x['inventory_order_id'], 16)),
          sep='\n')

    return inventory_list

keyboard_in = Controller()

def on_press(key):

    current_window = (GetWindowText(GetForegroundWindow()))
    if 'ELDEN' in current_window:
        # print(f'{key} pressed')

        while keyboard.is_pressed('u'):

            execute_key_macross('esc|e|e|right|e|esc')
            break

    # except:
    #     print('something')
    #     pass

def on_release(key):
    pass
    # print(f'{key} released')
    # if key == Key.esc:
    #     return False

# Collect events until released

def non_letter_keys() -> tuple:
    """

    :return:
    """
    return ('alt',
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
            'scroll_lock')


def execute_key_macross(keyline: str) -> None:
    """
    Parses a line into a keys and simulates key presses.
    Additional pause can be made with 'pauseN', where N is one Hundredth sec.
    :param keyline: line of keys divided with '|'
    :return:
    """

    key_presses = keyline.split('|')

    for key_press in key_presses:

        # Additional pauses.
        if key_press.startswith('pause'):
            pause_time = int(key_press.replace('pause', ''))
            time.sleep(pause_time / 100)
            continue

        # Key presses execution.
        if key_press in non_letter_keys():
            keyboard_in.press(Key[key_press])
            time.sleep(0.05)
            keyboard_in.release(Key[key_press])
        else:
            keyboard_in.press(key_press)
            time.sleep(0.05)
            keyboard_in.release(key_press)

        time.sleep(0.05)

if __name__ == '__main__':

    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

    # listener = Listener(
    #     on_press=on_press,
    #     on_release=on_release)
    # listener.start()





