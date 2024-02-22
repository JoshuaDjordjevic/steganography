def bytes_to_bitstring(data:bytes) -> str:
    """
    Convert bytes to a binary string representation.

    Args:
        data (bytes): The input bytes.

    Returns:
        str: The binary string representation.
    """
    bitstring = ''.join(format(byte, '08b') for byte in data)
    return bitstring

def bitstring_to_bytes(bitstring:str) -> bytes:
    """
    Convert a binary string representation to bytes.

    Args:
        bitstring (str): The input binary string.

    Returns:
        bytes: The bytes representation.
    """
    bytes_list = [int(bitstring[i:i+8], 2) for i in range(0, len(bitstring), 8)]
    return bytes(bytes_list)

def int_to_bitstring(integer:int, width:int=8) -> str:
    """
    Convert an integer to a binary string representation.

    Args:
        integer (int): The input integer.
        width (int, optional): The width of the binary string. Defaults to 8.

    Returns:
        str: The binary string representation.
    """
    return bin(integer)[2:].zfill(width)

def bitstring_to_int(bitstring:str) -> int:
    """
    Convert a binary string representation to an integer.

    Args:
        bitstring (str): The input binary string.

    Returns:
        int: The integer representation.
    """
    result = 0
    for bit in bitstring:
        result = (result << 1) | int(bit)
    return result

def replace_last_bits(integer:int, bits:str, count:int=None) -> int:
    """
    Replace the last bits of an integer with the specified bits.

    Args:
        integer (int): The input integer.
        bits (str): The bits to replace.
        count (int, optional): The number of bits to replace. Defaults to None.

    Returns:
        int: The modified integer.
    """
    count = count or len(bits)
    return bitstring_to_int(int_to_bitstring(integer)[:-count]+bits)

def get_last_bits(integer:int, count:int=1) -> str:
    """
    Get the last bits of an integer as a binary string.

    Args:
        integer (int): The input integer.
        count (int, optional): The number of bits to retrieve. Defaults to 1.

    Returns:
        str: The binary string representation of the last bits.
    """
    return int_to_bitstring(integer)[-count:]