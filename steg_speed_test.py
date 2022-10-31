import steg
import os
import string
import time
import random
import wave
file0 = wave.open('audios/0.wav', mode="rb")
file1 = wave.open('audios/1.wav', mode="rb")
file2 = wave.open('audios/2.wav', mode='rb')
file3 = wave.open('audios/3.wav', mode='rb')
file4 = wave.open('audios/4.wav', mode='rb')
file5 = wave.open('audios/5.wav', mode='rb')
file6 = wave.open('audios/6.wav', mode='rb')

frames0 = file0.getnframes()
ba0 = bytearray(list(file0.readframes(frames0)))
len0 = len(ba0)
frames1 = file1.getnframes()
ba1 = bytearray(list(file1.readframes(frames1)))
len1 = len(ba1)
frames2 = file2.getnframes()
ba2 = bytearray(list(file2.readframes(frames2)))
len2 = len(ba2)
frames3 = file3.getnframes()
ba3 = bytearray(list(file3.readframes(frames3)))
len3 = len(ba3)
frames4 = file4.getnframes()
ba4 = bytearray(list(file4.readframes(frames4)))
len4 = len(ba4)
frames5 = file5.getnframes()
ba5 = bytearray(list(file5.readframes(frames5)))
len5 = len(ba5)
frames6 = file6.getnframes()
ba6 = bytearray(list(file6.readframes(frames6)))
len6 = len(ba6)


print(len0, len1, len2, len3, len4, len5, len6)
encryption_times = []
dec_times = []
for i in range(33, 1000):
    for j in range(20):
        msg = ''.join(random.choice(string.ascii_letters) for m in range(i*5000))
        emb_start = time.time()
        filename = steg.embedTxt(msg, 'audios/6.wav')
        emb_end = time.time()
        msg2 = steg.extract(filename)
        ext_end = time.time()
        encryption_times.append(emb_end - emb_start)
        dec_times.append(ext_end - emb_end)

    encryption_times.pop(0)
    encryption_times.pop(0)
    encryption_times.pop(len(encryption_times)-1)
    encryption_times.pop(len(encryption_times)-1)
    dec_times.pop(0)
    dec_times.pop(0)
    dec_times.pop(len(dec_times)-1)
    dec_times.pop(len(dec_times)-1)

    avg = sum(encryption_times)/len(encryption_times)
    avg2 = sum(dec_times)/len(dec_times)

    extfile = open('Average extraction times', 'a')
    embfile = open('Average embedding times', 'a')

    extfile.write(f"average extraction time of string length {str(i*5000)}: {avg2}s \n")
    embfile.write(f"average embedding time of string length of {str(i*500)}: {avg}s \n")