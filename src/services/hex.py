"""
Contains some utility functions to manage HEX data.
"""


def endian_turn(hex_string: str) -> str:
    """
    Turns little-endian hex string to big-endian or visa versa.
    Example: 8097FA01 <-> 01FA9780
    """

    if len(hex_string) < 2:
        return hex_string

    if len(hex_string) % 2 == 1:
        return hex_string

    pairs = [hex_string[i : i + 2] for i in range(0, len(hex_string), 2)]

    return ''.join(reversed(pairs))


def item_id_from_dec_to_hex(item_id: str, max_length: int) -> str:
    """
    Turns decimal item id to hex version that's can be searched in save file.
    Example: 16000000 -> 0024f400
    """

    hex_big_endian = hex(int(item_id))[2:]
    if len(hex_big_endian) % 2 == 1:
        hex_big_endian = '0' + hex_big_endian
    hex_little_endian = endian_turn(hex_big_endian)
    hex_little_endian += (max_length - len(hex_little_endian)) * '0'

    return hex_little_endian


def add_escaping_symbols_to_byte_reg(reg_expression: bytes) -> bytes:
    """
    Adding escaping symbols to regular expression, so it can be
    performed on byte strings.
    """

    escaping_characters = [b'\\', b'[', b']', b'(', b')', b'|', b'^', b'$', b'.', b'?', b'*', b'+']
    for ch in escaping_characters:
        reg_expression = reg_expression.replace(ch, b'\\' + ch)

    return reg_expression
