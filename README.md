<div id="top"></div>

# About This Repo

I created this repository to experiment with a form of Steganography - Least significant bit substitution. If we'd like to know how this works under the hood we can take a look at the simplest example (see the explanation below). More code will be added to this repository as I continue testing things.

# Requirements

This code repository requires `PIL (Python Imaging Library (Fork))`, which can be installed via pip using `pip install pillow`, or downloaded from [pypi](https://pypi.org/project/pillow/ "Pillow Pypi page"). See the [Pillow installation guide](https://pillow.readthedocs.io/en/latest/installation.html) if you run into any trouble!

## LSB Substitution Explained

Say we have some binary data, `010`. Now, say we have some kind of "container", which in this case is an 8-bit number (0-255). For this example, let's say our number is `187`, which is `10111011` in binary. What we can do here is cut out the last couple bits from our number (in this case 3, since we've got 3 bits we want to store). We can then append our data to the end of the truncated original data, giving us `10111 + 010`, which upon converting back to base-10 gives us `186`.

That's the writing step done. We've successfully stored 3 of our own bits in some arbitrary number as a "container". The reading process is very simple as it is just the inverse.

Now how is this useful? All we've seen is storing 3 bits in a small number. That doesn't sound very exciting! Well, what if we used an image as our container instead? And we could use all the numbers from every pixel in the image over every channel (An RGB (red, green, blue) image has three channels to use, each of which is an 8-bit number). Now if this image was 1920x1080 pixels in size (the same size as most modern displays), we'd have 6220800 8-bit numbers to use for storing our own data. We can split up any large amount of bits into smaller n-size groups and replace the last n bits from each number with ours. If we were replacing 3 bits from every one of those 6.2 million 8-bit numbers, we'd have the equivalent storage space of 2.22MB! (The calculation for this is: Total Bits = Image Pixels * Channels * Replacement Bit Count... 1920 * 1080 * 3 * 3 bits ~= 2.3 million bytes ~= 2.2 thousand KB) (Funnily enough, that's actually more than enough space to store a smaller image inside!)

<p><a href="#top">🔼 Back To Top 🔼</a></p>

### Better Approaches To Hiding Precious Bytes

Now what about artifacting? Well, with LSB substitution, artifacts can appear my visible if the input image is very uniform or a repeating pattern. Say we used a plain white image as our input. We'd see all the slight colour variations after editing the bits of our image. If we plan on sending this image anywhere over the internet we wouldn't want people to easily see the data we're trying to hide, so it's more appropriate to use an original image (i.e. take a photo with your phone camera and use that as the input - This provides a layer of noise too which means artifacts will be hardly noticeable if at all!)

That's certainly one way to make sure potential attackers or bad actors can't see the data we've hidden, but remember, we're still storing our data as plain bytes, and presumably in some kind of retrievable order. This is no good, because a very simple program could easily crack this and retreive all our precious bytes.

A *slightly* better way of putting our data in the image or container would be first shuffling the order in which we do this, using a seeded shuffle algorithm. This means we can generate a list of indices (all the containers we'll use), shuffle that list, and then insert our data container by container. If we did this with an image, we'd see our data is all spread out over the pixels instead of inserted row by row or column by column.

Now that's all well and good (it's not), but our data still isn't secure. It's better practice to first encrypt our data using some modern encryption algorithm. If you'd like to read further into this I recommend checking out the python `Fernet` library [https://cryptography.io/en/latest/fernet/](https://cryptography.io/en/latest/fernet/ "Fernet (Symmetric Encryption), cryptography.io").

<p><a href="#top">🔼 Back To Top 🔼</a></p>

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

<p><a href="#top">🔼 Back To Top 🔼</a></p>
