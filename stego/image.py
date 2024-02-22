import itertools
from PIL import Image
from . import utility

# Define a dictionary mapping image modes to their corresponding channel count
IMAGE_MODE_CHANNELS = {
    "L": 1,
    "LA": 1,
    "RGB": 3,
    "RGBA": 3
}

def write_data(image:Image.Image,
               data:bytes,
               eod_marker:bytes,
               lsb_count:int=3) -> Image.Image:
    """
    Write data into an image using least significant bit (LSB) substitution method.

    Args:
        image (Image.Image): The input image.
        data (bytes): The data to be hidden in the image.
        eod_marker (bytes): The end-of-data marker.
        lsb_count (int, optional): Number of LSBs to replace in each pixel component. Defaults to 3.

    Returns:
        Image.Image: The modified image with hidden data.
    """

    # Validate image mode
    channel_count = IMAGE_MODE_CHANNELS.get(image.mode, None)
    assert channel_count is not None, f"Image mode {image.mode} not supported. Try converting the image first."

    # Validate image format
    assert image.format == "PNG", "Input image is not in PNG format"

    # TODO: Validate image size to ensure data will fit
    
    # Create a copy of the image to preserve the original
    image_copy = image.copy()

    # Convert data and end-of-data marker to bitstring
    bits = utility.bytes_to_bitstring(data+eod_marker)

    # Get pixel data from the image
    pixels = image_copy.load()

    # Initialize flag for loop termination
    finished = False

    # Iterate over each pixel in the image
    for (x, y) in itertools.product(range(image_copy.size[0]), range(image_copy.size[1])):
        colour = pixels[x, y]
        new_colour = list(colour)

        # Iterate over each channel in the pixel
        for channel_index in range(channel_count):
            value = colour[channel_index]

            # Extract bits from the bitstring to be inserted into the pixel
            insert_bits = bits[:lsb_count].rjust(lsb_count, '0')
            bits = bits[lsb_count:]

            # Replace the least significant bits in the pixel with the extracted bits
            new_value = utility.replace_last_bits(value, insert_bits, lsb_count)
            new_colour[channel_index] = new_value

            # Check if all data has been embedded
            if len(bits) == 0:
                finished = True
                break
        
        # Update the pixel with the modified colour
        pixels[x, y] = tuple(new_colour)

        # Check if embedding process is finished
        if finished:
            break

    # Return the modified image
    return image_copy

def read_data(image:Image.Image,
              eod_marker:bytes,
              lsb_count:int=3) -> bytes:
    """
    Read data from an image using least significant bit (LSB) substitution method.

    Args:
        image (Image.Image): The input image.
        eod_marker (bytes): The end-of-data marker.
        lsb_count (int, optional): Number of LSBs to read in each pixel component. Defaults to 3.

    Returns:
        bytes: The data that was hidden in the input image.
    """

    # Validate image mode
    channel_count = IMAGE_MODE_CHANNELS.get(image.mode, None)
    assert channel_count is not None, f"Image mode {image.mode} not supported. Try converting the image first."

    # Validate image format
    assert image.format == "PNG", "Input image is not in PNG format"
    
    # Convert end-of-data marker to bitstring
    eod_bits = utility.bytes_to_bitstring(eod_marker)
    eod_length = len(eod_bits)

    # Access pixel data
    pixels = image.load()

    # Initialize variables
    bits = ""
    finished = False

    # Iterate over each pixel in the image
    for (x, y) in itertools.product(range(image.size[0]), range(image.size[1])):
        colour = pixels[x, y]
        
        # Iterate over each channel in the pixel
        for channel_index in range(channel_count):
            value = colour[channel_index]

            # Extract the specified number of least significant bits
            last_bits = utility.get_last_bits(value, lsb_count)
            for bit in last_bits:
                bits += bit

                # Check if the end-of-data marker is found
                if bits[-eod_length:] == eod_bits:
                    finished = True
                    break
            
            if finished:
                break # Exit inner loop if end-of-data marker is found
        
        if finished:
            break # Exit outer loop if end-of-data marker is found

    # Convert the bitstring to bytes and remove end-of-data marker
    return utility.bitstring_to_bytes(bits[:-eod_length])