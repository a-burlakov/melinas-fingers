import os
import re

import datasheets

def get_savefile_path() -> str:
    """
    Returns the path to the relevant Elden Ring save file.

    :return: Path as string
    """
    return os.getcwd() + '\\test\ER0000_before.sl2'
    # return os.getcwd() + '\\test\ER0000_flail_in_chest.sl2'


def get_slot_data(filepath: str, save_slot_number: int) -> bytes:
    """
    Returns hex data of save file related to specific save slot.

    :param filepath: path to savefile
    :param save_slot_number: number of specific save slot (begins with "1")
    :return:
    """
    with open(filepath, "rb") as fh:
        dat = fh.read()

        # TODO: difference between slots is always 2621456. Make it using this. And check!

        intervals = ((0x0000000, 0x0280310),
                     # (0x0000310, 0x0280310)
                     (0x0280320, 0x0500320),
                     (0x0500330, 0x0780330),
                     (0x0780340, 0x0A00340),
                     (0x0A00350, 0x0C80350),
                     (0x0C80360, 0x0F00360),
                     (0x0F00370, 0x1180370),
                     (0x1180380, 0x1400380),
                     (0x1400390, 0x1680390),
                     (0x16803A0, 0x1900400))

        slot_interval = intervals[save_slot_number - 1]

        return dat[slot_interval[0]:slot_interval[1]]


def get_slot_names(file) -> list:
    try:
        with open(file, "rb") as fh:
            data = fh.read()

    except FileNotFoundError as e:
        return False

    names = [data[0x1901d0e:0x1901d0e + 32].decode('utf-16'),
             data[0x1901f5a:0x1901f5a + 32].decode('utf-16'),
             data[0x19021a6:0x19021a6 + 32].decode('utf-16'),
             data[0x19023f2:0x19023f2 + 32].decode('utf-16'),
             data[0x190263e:0x190263e + 32].decode('utf-16'),
             data[0x190288a:0x190288a + 32].decode('utf-16'),
             data[0x1902ad6:0x1902ad6 + 32].decode('utf-16'),
             data[0x1902d22:0x1902d22 + 32].decode('utf-16'),
             data[0x1902f6e:0x1902f6e + 32].decode('utf-16'),
             data[0x19031ba:0x19031ba + 32].decode('utf-16')]

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


def add_weapon_hex_mark(weapon_id: str) -> str:
    """
    Put two '80' hex codes in front of weapon ID.
    It's needed because you can find weapons used by character using this mark.

    :param weapon_id: id like "F0EF1000"
    :return: string like "8080F0EF1000"
    """

    return '8080' + weapon_id


if __name__ == '__main__':

    slot_number: int = 1
    path = get_savefile_path()
    slot_data = get_slot_data(path, slot_number)

    weapons = datasheets.weapons_data()
    all_character_weapons = []
    slot_data_for_search_all = slot_data[0x00000740:0x0000e590]
    for weapon_data in weapons:
        weapon_name = weapon_data[0]
        weapon_id = weapon_data[1]

        search_string = bytes.fromhex(add_weapon_hex_mark(weapon_id))
        count = slot_data_for_search_all.count(search_string)
        if count > 0:
            all_character_weapons.append([weapon_name, weapon_id])
            print([weapon_name, weapon_id])

    pass

    slot_for_search_slot = slot_data[0x0000A500:0x00013900]
    for name, id in all_character_weapons:

        # We look for a construction like that: XX XX 80 80 WW WW WW WW
        # W - weapon ID
        # 80 - weapon mark
        # X - unique ID for a specific weapon
        search_string = bytes.fromhex(add_weapon_hex_mark(id))
        try:
            result = re.findall(b'.{8}(?<=' + search_string + b')', slot_data)
            # print(result)
            for hex_slot_weapon in result:
                if hex_slot_weapon[:4] in slot_for_search_slot:
                    print(str(hex_slot_weapon) + ' ' + name + " " + id)
        except:
            print(name, id)
