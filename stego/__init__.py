"""
### Stego
Stego is a python library for simple steganography.

Currently Stego only supports LSB substitution, and
only in PNG images files and WAV audio files.

The library will be updated as time goes on to
include more options for hiding data in plain sight.
"""

from . import utility
from . import image
from . import wav