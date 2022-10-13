def slot_ranges(save_slot_number: int = 0) -> tuple | list:
    """
    Returns hex interval for the save slot in save file.
    If save_slot_number is 0, returns list of all intervals.

    :param save_slot_number: number of specific save slot (begins with "1")
    :return:
    """

    between_slots = 16
    width = 2621456
    intervals = [(0x0000310, 0x0280310)]  # first save file interval
    for _ in range(9):
        last_interval = intervals[-1]
        intervals.append(
            (last_interval[1] + between_slots, last_interval[1] + width)
        )

    if save_slot_number == 0:
        return intervals
    else:
        return intervals[save_slot_number - 1]


def slot_names_ranges() -> tuple:
    """
    Returns HEX-ranges of places in save-file that keeps save slot names
    (characters names).
    :return:
    """

    return ((0x1901d0e, 0x1901d0e + 32),
            (0x1901f5a, 0x1901f5a + 32),
            (0x19021a6, 0x19021a6 + 32),
            (0x19023f2, 0x19023f2 + 32),
            (0x190263e, 0x190263e + 32),
            (0x190288a, 0x190288a + 32),
            (0x1902ad6, 0x1902ad6 + 32),
            (0x1902d22, 0x1902d22 + 32),
            (0x1902f6e, 0x1902f6e + 32),
            (0x19031ba, 0x19031ba + 32))


def weapon_instances_search_range() -> tuple:
    """

    :return:
    """
    return (0x00010000, 0x00030000)


def inventory_and_chest_separator() -> bytes:
    """
    Returns a HEX-string that separates inventory and chest block for
    weapon searching.
    :return:
    """
    return bytes.fromhex('ffffffff00000000') * 6
