import os
import regex
import savefile_structure
import datasheets

def get_savefile_path() -> str:
    """
    Returns the path to the relevant Elden Ring save file.

    :return: Path as string
    """
    # return os.getcwd() + '\\test\ER0000_before.sl2'
    # return os.getcwd() + '\\test\ER0000_125_windhalberds_mooninhands_claymore_chest.sl2'
    return os.getcwd() + '\\test\ER0000_freedom_all_in_chest.sl2'


def get_slot_data(filepath: str, save_slot_number: int) -> bytes:
    """
    Returns hex data of save file related to specific save slot.

    :param filepath: path to savefile
    :param save_slot_number: number of specific save slot (begins with "1")
    :return:
    """
    with open(filepath, "rb") as fh:
        dat = fh.read()

        slot_interval = savefile_structure.full_slot_intervals(save_slot_number)

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
    all_weapons = []
    # TODO: рассчитывать и поиски для всех оружий тоже по той же схеме
    interval = savefile_structure.full_slot_intervals(slot_number)
    interval_for_search = slot_data[interval[0]:interval[1]]
    for weapon_data in weapons:
        weapon_name = weapon_data[0]
        weapon_id = weapon_data[1]

        search_string = bytes.fromhex(weapon_id)
        count = interval_for_search.count(search_string)
        if count > 0:
            all_weapons.append([weapon_name, weapon_id])
            # print([weapon_name, weapon_id])

    # Looking for many instances of each weapon.
    interval_for_search_instances = slot_data[0x0000000:0x00020000]
    for name, id in all_weapons:

        # We look for a construction like that: XX XX 80 80 WW WW WW WW
        # W - weapon ID
        # 80 - weapon mark
        # X - unique ID for a specific weapon
        search_string = bytes.fromhex(add_weapon_hex_mark(id))
        # print(name, id)
        try:
            # TODO: need to make it much faster
            escaping_characters = [b'\\', b'[', b']', b'}', b'{', b'(', b')', b'|']
            for ch in escaping_characters:
                search_string = search_string.replace(ch, b'\\' + ch)
            # search_string = search_string.replace(b'[', b'\\[')
            # search_string = search_string.replace(b']', b'\\]')
            # search_string = search_string.replace(b'}', b'\\}')
            # search_string = search_string.replace(b'}', b'\\}')
            # search_string = search_string.replace(b')', b'\\)')
            # search_string = search_string.replace(b'(', b'\\(')
            # search_string = search_string.replace(b'|', b'\\|')
            reg_expression = b'.{8}(?<=' + search_string + b')'

            result = regex.findall(reg_expression, slot_data)
            # print(result)
            for hex_slot_weapon in result:
                if hex_slot_weapon[:4] in interval_for_search_instances:
                  pass
                else:
                    print('Не был найден экземпляр', name, hex_slot_weapon)
                #       print(str(hex_slot_weapon))
                # print('')
        except:
            pass
            print('error', name, id)
