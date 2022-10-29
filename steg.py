import wave
import string
import random

def embedTxt(text, file):
    audio = wave.open(file, mode="rb")
    msg = text
    frames = audio.getnframes()
    audio_bytes = audio.readframes(frames)
    audio_bytes_list = list(audio_bytes)
    audio_bytes_array = bytearray(audio_bytes_list)
    msg += (int((len(audio_bytes_array)-(len(msg)*64))/8))*'$'
    msg_bits = ''
    for letter in msg:
        letter_byte = bin(ord(letter))
        msg_bits += letter_byte[2:].rjust(8,'0')
    embedded_message_array = []
    for i, bit in enumerate(msg_bits):
        embedded_message_array.append((audio_bytes_array[i] & 254) | int(bit))
    embedded_byte_array = bytes(embedded_message_array)
    filename = ''.join(random.choice(string.ascii_letters) for i in range(10))
    filename = f"audios/{filename}.wav"
    embedded_audio = wave.open(filename, 'wb')
    embedded_audio.setparams(audio.getparams())
    embedded_audio.writeframes(embedded_byte_array)
    embedded_audio.close()
    return filename

def extract(filename):
    audio = wave.open(filename, "rb")
    frames = audio.getnframes()
    audio_bytes = audio.readframes(frames)
    audio_bytes_list = list(audio_bytes)
    audio_bytes_array = bytearray(audio_bytes_list)

    bitlist = []

    for i in range(len(audio_bytes_array)):
        bitlist.append(audio_bytes_array[i] & 1)

    m = []
    for i in range(0, len(bitlist), 8):
        m.append(bitlist[i:i + 8])

    message = ''
    m2 = []
    for i in range(len(m)):
        letter = "".join(map(str, (m[i])))
        message += chr(int(letter, 2))
    message = message.strip("$")

    return message


def embedTxtHist(text, file, sender_name, receiver_name):
    audio = wave.open(file, mode="rb")
    names = [sender_name, receiver_name]
    names.sort()
    msg = text
    frames = audio.getnframes()
    audio_bytes = audio.readframes(frames)
    audio_bytes_list = list(audio_bytes)
    audio_bytes_array = bytearray(audio_bytes_list)
    msg += (int((len(audio_bytes_array)-(len(msg)*64))/8))*'$'
    msg_bits = ''
    for letter in msg:
        letter_byte = bin(ord(letter))
        msg_bits += letter_byte[2:].rjust(8,'0')
    embedded_message_array = []
    for i, bit in enumerate(msg_bits):
        embedded_message_array.append((audio_bytes_array[i] & 254) | int(bit))
    embedded_byte_array = bytes(embedded_message_array)
    filename = f"audios/{names[0]},{names[1]}embedded.wav"
    embedded_audio = wave.open(filename, 'wb')
    embedded_audio.setparams(audio.getparams())
    embedded_audio.writeframes(embedded_byte_array)
    embedded_audio.close()
