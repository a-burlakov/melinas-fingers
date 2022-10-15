"""
TODO: need to describe a save-file map
"""


def range_before_save_slots() -> int:
    """
    Returns an amount of symbols in HEX-save-file that goes before
    first save-slot information starts.
    """
    return 0x0000310


def slot_ranges(save_slot_number: int = 0) -> tuple | list:
    """
    Returns hex interval for the save slot in save file.
    If save_slot_number is 0, returns a list of all 10 intervals.
    """

    between_slots = 16
    save_slot_width = 2621456

    intervals = [(range_before_save_slots(), 0x0280310)]  # First save file.
    for _ in range(9):
        last_interval = intervals[-1]
        new_interval_begin = last_interval[1] + between_slots
        new_interval_end = last_interval[1] + save_slot_width
        intervals.append((new_interval_begin, new_interval_end))

    if save_slot_number == 0:
        return intervals
    else:
        return intervals[save_slot_number - 1]


def slot_names_ranges() -> tuple:
    """
    Returns HEX-ranges of places in save-file that keeps save slot names
    (characters names).
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


def instances_search_range(slot_data: bytes,
                           slot_name: str) -> tuple:
    """
    Seeks for a range in which can be found instances of equipment in specific
    save slot data. Minimal range is a position of slot data name.
    Max range can't be calculated and is taken with a margin.
    """

    slot_name_hex = bytes(slot_name, 'utf-8')
    slot_name_hex_bytes = [bytes.fromhex(hex(x)[2:]) for x in slot_name_hex]
    slot_name_hex_bytes = [x + bytes.fromhex('00') for x in
                           slot_name_hex_bytes]
    slot_name_hex = b''.join(slot_name_hex_bytes)

    slot_name_position = slot_data.find(slot_name_hex)

    range_max = 0x00035000

    return slot_name_position, range_max


def inventory_and_chest_separator() -> bytes:
    """
    Returns a HEX-string that separates inventory and chest block for
    weapon searching.
    """
    return bytes.fromhex('ffffffff00000000') * 6
