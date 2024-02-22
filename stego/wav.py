import wave
import io
from . import utility

def write_data(input_audio_bytes:bytes,
               data:bytes,
               eod_marker:bytes,
               lsb_count:int=3) -> bytes:
    """
    Write data into a wav file using least significant bit (LSB) substitution method.

    Args:
        input_audio_bytes (bytes): The input audio file's raw bytes.
        data (bytes): The data to be hidden in the audio.
        eod_marker (bytes): The end-of-data marker.
        lsb_count (int, optional): Number of LSBs to replace in each audio frame. Defaults to 3.

    Returns:
        bytes: The modified audio file's raw bytes. Can be written directly to a file open in "wb" mode.
    """

    # Convert data and end-of-data marker to bitstring
    bits = utility.bytes_to_bitstring(data+eod_marker)

    # Create a Wave_read instance with the input audio bytes
    with wave.open(io.BytesIO(input_audio_bytes), "rb") as wav_in:
        frame_count = wav_in.getnframes()
        sample_width = wav_in.getsampwidth()

        # Read all frames from this audio file
        frames = wav_in.readframes(frame_count)

        # Initialize variables
        edited_frames = b''
        i = -1

        # Iterate until all data has been embedded
        while len(bits) > 0:
            i += 1

            i_start = i*sample_width
            i_stop = (i+1)*sample_width

            # Extract bits from the bitstring to be inserted into the frame
            insert_bits = bits[:lsb_count].rjust(lsb_count, '0')
            bits = bits[lsb_count:]

            # Get the frame byte(s), then embed the required bits into the frame
            frame = frames[i_start:i_stop]
            frame_bits = utility.bytes_to_bitstring(frame)
            frame_bits_new = frame_bits[:-lsb_count] + insert_bits
            frame_new = utility.bitstring_to_bytes(frame_bits_new)
            
            # Save this new frame to the edited frames bytes
            edited_frames += frame_new
        
        # Overwrite any edited frames with their new values
        frames = edited_frames + frames[i_stop:]

        # Create the new audio file's bytes using a BytesIO instance
        output_audio_bytes = io.BytesIO()
        with wave.open(output_audio_bytes, "wb") as wav_out:
            wav_out.setparams(wav_in.getparams())
            wav_out.writeframes(frames)
    
    output_audio_bytes.seek(0)
    return output_audio_bytes.read()

def read_data(input_audio_bytes:bytes,
              eod_marker:bytes,
              lsb_count:int=3) -> bytes:
    """
    Read data from a wav file using least significant bit (LSB) substitution method.

    Args:
        input_audio_bytes (bytes): The input audio file's raw bytes.
        eod_marker (bytes): The end-of-data marker.
        lsb_count (int, optional): Number of LSBs to read in each audio frame. Defaults to 3.

    Returns:
        bytes: The data that was hidden in the input audio.
    """

    # Convert end-of-data marker to bitstring
    eod_bits = utility.bytes_to_bitstring(eod_marker)
    eod_length = len(eod_bits)

    # Create a Wave_read instance with the input audio bytes
    with wave.open(io.BytesIO(input_audio_bytes), "rb") as wav_in:
        frame_count = wav_in.getnframes()
        sample_width = wav_in.getsampwidth()
        frames = wav_in.readframes(frame_count)

        # Initialize variables
        bits = ""
        finished = False
        i = -1

        while not finished:
            i += 1

            i_start = i*sample_width
            i_stop = (i+1)*sample_width

            # Get the frame byte(s), and retrieve the corresponding least significant bits
            frame = frames[i_start:i_stop]
            frame_bits = utility.bytes_to_bitstring(frame)
            read_bits = frame_bits[-lsb_count:]
            
            # Append each bit to the output one by one and check if end-of-data marker is found
            for bit in read_bits:
                bits += bit

                # Check if the end-of-data marker is found
                if bits[-eod_length:] == eod_bits:
                    finished = True
                    break

    # Convert the bitstring to bytes and remove end-of-data marker
    return utility.bitstring_to_bytes(bits[:-eod_length])