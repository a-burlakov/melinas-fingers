def full_slot_intervals(save_slot_number: int = 0) -> tuple | list:
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

def inventory_and_chest_separator() -> bytes:
    """
    Returns a HEX-string that separates inventory and chest block for
    weapon seatching.
    :return:
    """
    return bytes.fromhex('ffffffff00000000') * 6
    # return b'\xff\xff\xff\xff\x00\x00\x00\x00' * 6