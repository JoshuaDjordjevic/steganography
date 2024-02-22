def bytes_to_bitstring(bytes:bytes):
    # Convert each byte to its binary representation and concatenate them
    bitstring = ''.join(format(byte, '08b') for byte in bytes)
    return bitstring

def bitstring_to_bytes(bitstring:str) -> bytes:
    # Group the bits into bytes and convert them back to integers
    bytes_list = [int(bitstring[i:i+8], 2) for i in range(0, len(bitstring), 8)]
    # Pack the integers into a bytes object
    bytestring = bytes(bytes_list)
    return bytestring

def int_to_bitstring(integer:int, width:int=8):
    return bin(integer)[2:].zfill(width)

def bitstring_to_int(bitstring:str):
    result = 0
    for bit in bitstring:
        result = (result << 1) | int(bit)
    return result

def replace_last_bits(integer:int, bits:str):
    count = len(bits)
    return bitstring_to_int(int_to_bitstring(integer)[:-count]+bits)