import os
import re
import savefile_structure
import datasheets
import time
from pynput.keyboard import Key, Controller, Listener
import keyboard
from win32gui import GetWindowText, GetForegroundWindow


def get_savefile_path() -> str:
    """
    Returns the path to the relevant Elden Ring save file.

    :return: Path as string
    """
    # return os.getcwd() + '\\test\ER0000_flail_in_chest.sl2'
    return os.getcwd() + '\\test\ER0000_Talismans.sl2'
    # return os.getcwd() + '\\test\ER0000_125_windhalberds_mooninhands_claymore_chest.sl2'
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
    names = [data[x: y].decode('utf-16') for x, y in names_ranges]

    for i, name in enumerate(names):
        if name == '\x00' * 16:
            names[i] = None
        else:
            names[i] = name.split('\x00')[0]

    return names


def endian_turn(hex: str) -> str:
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


def item_id_as_hex(item_id: str, max_length: int) -> str:
    """

    :param item_id:
    :return:
    """

    hex_big_endian = hex(int(item_id))[2:]
    if len(hex_big_endian) % 2 == 1:
        hex_big_endian = '0' + hex_big_endian
    hex_little_endian = endian_turn(hex_big_endian)
    hex_little_endian += (max_length - len(hex_little_endian)) * '0'

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


def get_equipment_in_inventory():
    """
    code keeper
    :return:
    """

    slot_number: int = 1
    save_file_path = get_savefile_path()
    slot_data = get_slot_data(save_file_path, slot_number)
    slot_name = get_slot_names(save_file_path)[slot_number - 1]

    # Looking for all equipment mentioned in save-file, whatever quantity
    # and position in inventory or chest.
    slot_data_for_equipment_search = slot_data[:0x00030000]
    all_equipment_having = []
    for weapon in datasheets.weapons():
        weapon_id = weapon[1]
        weapon_name = weapon[2]
        if bytes.fromhex(weapon_id) in slot_data_for_equipment_search:
            all_equipment_having.append([weapon_name, weapon_id, 'Weapon'])

    for armor in datasheets.armor():
        armor_id = armor[1]
        armor_name = armor[2]
        if bytes.fromhex(armor_id) in slot_data_for_equipment_search:
            all_equipment_having.append([armor_name, armor_id, 'Armor'])

    # Looking for many instances of each equipment. In save-file structure
    # is like this: [inventory instances]-[separator]-[chest instances]
    # We need only inventory instances, so first we need to find the separator.

    instances_range = savefile_structure.equipment_instances_search_range(slot_data, slot_name)
    data_for_instances_search = slot_data[instances_range[0]:
                                          instances_range[1]]
    separator = savefile_structure.inventory_and_chest_separator()
    separator_pos = data_for_instances_search.find(separator)

    inventory_list = []
    for equipment in all_equipment_having:
        equipment_name = equipment[0]
        equipment_id = equipment[1]
        equipment_type = equipment[2]
        equipment_mark = '8080'
        if equipment_type == 'Armor':
            equipment_mark = '8090'

        # In save-file we're looking for lines like: ID ID 80 MM WW WW WW (WW)
        # Where:
        #   ID ID - ID of specific instance of equipment.
        #   80 MM - mark of equipment. "80 80" for weapon, "80 90" for armor.
        #   WW WW WW (WW) - equipment ID. Weapon has 4 pieces, armor has 3.
        # Each line represents an instance of equipment.
        id_for_reg = bytes.fromhex(equipment_mark + equipment_id)
        id_for_reg = add_escaping_character_to_byte_reg(id_for_reg)
        reg_expression = b'.{2}(?=' + id_for_reg + b')'

        result = re.finditer(reg_expression,
                             slot_data[:instances_range[0] + separator_pos])

        for match in result:

            instance_id = match.group() + bytes.fromhex(equipment_mark)
            instance_position = data_for_instances_search.find(instance_id)
            if instance_position < 0:
                continue

            # As we found instance's ID, we can see, in what part this ID
            # is located. If it's in inventory part, then that's it.
            if instance_position > separator_pos:
                continue

            instance_id = instance_id.hex(' ').replace(' ', '')
            position_in_file = hex(instances_range[0]
                                   + instance_position
                                   + savefile_structure.range_before_save_slots())

            # We have to learn in what order equipment is placed in inventory.
            # Instance's ID is located in line that looks like:
            # ID ID 80 80 XX XX XX XX NN NN
            # Where:
            #   ID ID - instance's ID
            #   80 80 XX XX XX XX - not interesting data
            #   NN NN - additional ID that can be used to learn what order in
            #           inventory this instance has.
            inventory_order_id = data_for_instances_search[
                                 instance_position + 8:
                                 instance_position + 10]
            inventory_order_id = inventory_order_id.hex(' ').replace(' ', '')

            # Order ID has two HEX numbers ("f1 21") but actual order goes
            # on mirrored numbers ("21 f1", "21 f2", "21 f3" etc.)
            inventory_order_id = inventory_order_id[2:4] \
                                 + inventory_order_id[:2]

            # We need to check what type of armor an instance has.
            if equipment_type == 'Armor':
                equipment_id_decimal = str(int(endian_turn(equipment_id), 16))
                if equipment_id_decimal.endswith('000'):
                    equipment_type += '_Head'
                elif equipment_id_decimal.endswith('100'):
                    equipment_type += '_Torso'
                elif equipment_id_decimal.endswith('200'):
                    equipment_type += '_Hands'
                elif equipment_id_decimal.endswith('300'):
                    equipment_type += '_Legs'

            instance_dict = {}
            instance_dict.setdefault('equipment_type', equipment_type)
            instance_dict.setdefault('equipment_name', equipment_name)
            instance_dict.setdefault('equipment_id', equipment_id)
            instance_dict.setdefault('instance_id', instance_id)
            instance_dict.setdefault('inventory_order_id', inventory_order_id)
            instance_dict.setdefault('position', position_in_file)
            inventory_list.append(instance_dict)

    # Ta lismans are located in save-file simmilar to armor and weapons, but
    # not identical.
    # Talisman line looks like: XX XX 00A001000000 NN NN, where
    #   XX XX - talisman ID.
    #   00A001000000 - always identical part
    #   NN NN - order ID.
    #
    # Inventory/Chest search is identical to weapons and armor.
    # Talismans don't have instances, you can only have one.
    talisman_mark = '00A001000000'
    for talisman in datasheets.talismans():
        talisman_id = talisman[1]
        talisman_name = talisman[2]

        talisman_search = bytes.fromhex(talisman_id + talisman_mark)
        talisman_position = data_for_instances_search.find(talisman_search)
        if talisman_position < 0:
            continue

        if talisman_position > separator_pos:
            continue

        position_in_file = hex(instances_range[0]
                               + talisman_position
                               + savefile_structure.range_before_save_slots())

        inventory_order_id = data_for_instances_search[
                             talisman_position + 8:
                             talisman_position + 10]
        inventory_order_id = inventory_order_id.hex(' ').replace(' ', '')
        inventory_order_id = inventory_order_id[2:4] \
                             + inventory_order_id[:2]

        instance_dict = {}
        instance_dict.setdefault('equipment_type', 'Talisman')
        instance_dict.setdefault('equipment_name', talisman_name)
        instance_dict.setdefault('equipment_id', talisman_id)
        instance_dict.setdefault('instance_id', '')
        instance_dict.setdefault('inventory_order_id', inventory_order_id)
        instance_dict.setdefault('position', position_in_file)
        inventory_list.append(instance_dict)

    print(*sorted(inventory_list,
                  key=lambda x: (x['equipment_type'],
                                 int(x['inventory_order_id'], 16))),
          sep='\n')

    return inventory_list


keyboard_input = Controller()


def on_press(key):
    current_window = (GetWindowText(GetForegroundWindow()))
    if 'ELDEN' in current_window:

        while keyboard.is_pressed('u'):
            execute_key_macross('esc|pause10|e|e')
            go_to_beginning_of_list()
            execute_key_macross(keyline_to_find_item_number(13), 0.02)
            execute_key_macross('e|esc|y')

        while keyboard.is_pressed('i'):
            execute_key_macross('esc|pause10|e|r|esc|esc|e|e|pause10') # reopen, fast
            execute_key_macross(keyline_to_find_item_number(8), 0.02)
            execute_key_macross('e|esc|ctrl')

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

def sort_all_lists() -> None:
    """

    :return:
    """

    execute_key_macross(keyline_to_sort_all_lists())


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


def trying_to_invade() -> None:
    """

    :return:
    """

    tries = 3
    for _ in range(tries):
        execute_key_macross(keyline_to_invade_as_bloody_finger())
        time.sleep(4)
        execute_key_macross(keyline_to_invade_as_recusant())
        time.sleep(4)


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

    keyline += '|e|esc/'

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
    # TODO: опытным путем подобрать 0.4 на что-то по возможности меньшее
    time4all = max(0.4, max_amount_c * 0.017)
    time.sleep(0.01)
    time_start = time.time()
    execute_key_macross('c|' * (max_amount_c - 1) + 'c')
    time_finish = time.time()
    print(time_finish - time_start)
    time_remain = time4all - (time_finish - time_start)
    if time_remain > 0:
        time.sleep(time_remain)
    keyboard_input.release(Key.left)
    time.sleep(0.01)


def execute_key_macross(keyline: str, sleep_time: float = 0.05) -> None:
    """
    Parses a line into a keys and simulates key presses.
    Additional pause can be made with 'pauseN', where N is one hundredth sec.
    :param keyline: line of keys divided with '|'
    :param sleep_time:
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
            keyboard_input.press(Key[key_press])
            time.sleep(0.02)
            keyboard_input.release(Key[key_press])
        else:
            keyboard_input.press(key_press)
            time.sleep(0.02)
            keyboard_input.release(key_press)

        time.sleep(sleep_time)


if __name__ == '__main__':

    get_equipment_in_inventory()

    # # For catching keyboard presses.
    # with Listener(on_press=on_press) as listener:
    #     listener.join()

