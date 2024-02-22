# Steganography

Small personal tests related to the concept of Steganography, such as putting and retreiving data into / from simple image files (PNGs). More code will be added to this repository as I continue testing things.

# Requirements

This code repository requires `PIL (Python Imaging Library (Fork))`, which can be installed via pip using `pip install pillow`, or downloaded from [pypi](https://pypi.org/project/pillow/ "Pillow Pypi page"). See the [Pillow installation guide](https://pillow.readthedocs.io/en/latest/installation.html) if you run into any trouble!

# How To Use

## stego.image - Example Usage

This example covers how you can use `stego.image` to read and write byte data to and from a PNG image:

Let's get the required imports out of the way first.

```python
from PIL import Image
import stego
```

Now we'll declare our "end of data" bytes, which is how the reading system knows where our data ends. This can be any string of bytes, so we'll just mash the keyboard a little, but practically it would be better to use `os.urandom()` and save the bytestring somewhere we'll remember.

```python
EOD_BYTES = b"oasd8934oj;"
```

Next, we can define our data to embed. For this example we'll just embed some plaintext in the form of a bytestring (Denoted with the `b""` syntax), but note that you can just as easily use any other byte data, such as a file's raw content.

```python
data_to_embed = b"This text will be completely hidden!"
```

Now we can do the fun stuff! Opening up our image and putting the data in.

```python
image = Image.open("./test.png")
output_image = stego.image.write_data(image, data_to_embed, EOD_BYTES)
```

Optionally, you could also save this image if you'd like to take a close look at it in an editor.

```python
output_image.save("./test_with_data.png")
```

Now let's make sure our data was properly written into our image by reading it back out and printing it.

```python
recovered_data = stego.image.read_data(output_image, EOD_BYTES)
print(recovered_data)
```

Putting all of this together, our final script looks like:

```python
# Required imports
from PIL import Image
import stego

# This can be whatever you want, just make sure you
# remember or save it for reading the data back!
EOD_BYTES = b"oasd8934oj;"

# For this example we're simply hiding some plaintext in the form
# of bytes (Denoted with the b"" syntax, but you can just as easily
# hide any kind of bytes, like a file's content!)
data_to_embed = b"This text will be completely hidden!"

# Open the image we want to hide data inside of
image = Image.open("./test.png")

# Write the data bytes to our image using stego.image.write_data,
# which returns a new Image.Image instance that we can save to disk
output_image = stego.image.write_data(image, data_to_embed, EOD_BYTES)

# Save the image so we can check it out visually
output_image.save("./test_with_data.png")

# Just to be sure everything worked, we can read the data right back
recovered_data = stego.image.read_data(output_image, EOD_BYTES)

# Display the recovered data to the user
print(recovered_data)
```
