import os
import tempfile
from PIL import Image
import stego

# Define the end-of-data marker
EOD_BYTES = b"ohq.843$14s!d"

try:
    # Load the input image
    input_image_path = "test.png"
    input_image = Image.open(input_image_path)

    # Generate random data to hide in the image
    data_size = int(64 * 64 * 3 * 3 / 8 - len(EOD_BYTES))  # Calculate the maximum data size based on image size
    hidden_data = os.urandom(data_size)

    # Hide the data in the image and save the result to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_output_file:
        output_image = stego.image.write_data(input_image, hidden_data, EOD_BYTES, lsb_count=3)
        output_image.save(temp_output_file.name)

        # Display the path of the output image
        print(f"Output image saved to: {temp_output_file.name}")

        # Read the hidden data from the output image
        recovered_data = stego.image.read_data(output_image, EOD_BYTES, lsb_count=3)

        # Print the recovered data
        print("Recovered data matched?", recovered_data == hidden_data)

except FileNotFoundError:
    print("Error: Input image file not found.")
except Exception as e:
    print("An error occurred:", e)