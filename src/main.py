import datasheets

def get_savefile_path() -> str:
    """
    Returns the path to the relevant Elden Ring save file.
    :return: Path as string
    """
    # return 'C:\PythonProjects\EldenRingHardSwapper\src\\test_savefiles\ER0000_before.sl2'
    return 'C:\PythonProjects\EldenRingHardSwapper\src\\test_savefiles\ER0000_flail_in_chest.sl2'


def get_slot_data(filepath: str, save_slot_number: int) -> bytes:
    """
    Returns hex data of save file related to specific save slot
    :param filepath: path to savefile
    :param save_slot_number: number of specific save slot (begins with "1")
    :return:
    """
    with open(filepath, "rb") as fh:
        dat = fh.read()

        intervals = ((0x0000310, 0x028030F + 1), (0x0280320, 0x050031F + 1),
                     (0x0500330, 0x078032F + 1), (0x0780340, 0x0A0033F + 1),
                     (0x0A00350, 0x0C8034F + 1), (0x0C80360, 0x0F0035F + 1),
                     (0x0F00370, 0x118036F + 1), (0x1180380, 0x140037F + 1),
                     (0x1400390, 0x168038F + 1), (0x16803A0, 0x190039F + 1))

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
        if name == '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            names[i] = None
        else:
            # name looks like this: 'wete\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
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


def add_weapon_hex_mark(hex: str) -> str:
    """

    :param hex:
    :return:
    """

    return '8080' + hex


if __name__ == '__main__':
    slot_number: int = 1
    path = get_savefile_path()
    a = get_slot_names(path)
    slot_data = get_slot_data(path, slot_number)


    weapons = datasheets.weapons_data()

    for weapon_data in weapons:
        weapon_name = weapon_data[0]
        weapon_id = weapon_data[1]

        search_string = bytes.fromhex(add_weapon_hex_mark(weapon_id))
        count = slot_data.count(search_string)
        if count > 0:
            print(f'{weapon_name} - {count}')

    pass
