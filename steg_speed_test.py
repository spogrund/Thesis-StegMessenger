"""
PGRSAM001
EEE4022S
Final year project
Steg speed test module
"""
import csv
import pandas as pd
import steg
import os
import string
import time
import random
import wave
"""
different files with increasing sizes to be used depending on the input length
file0 = wave.open('audios/0.wav', mode="rb")
file1 = wave.open('audios/1.wav', mode="rb")
file2 = wave.open('audios/2.wav', mode='rb')
file3 = wave.open('audios/3.wav', mode='rb')
file4 = wave.open('audios/4.wav', mode='rb')
file5 = wave.open('audios/5.wav', mode='rb')
file6 = wave.open('audios/6.wav', mode='rb')
emb_times = []
ext_times = []
for i in range(36, 1000):
    for j in range(20):
        msg = ''.join(random.choice(string.ascii_letters) for m in range(i*5000))
        emb_start = time.time()
        filename = steg.embedTxt(msg, 'audios/6.wav')
        emb_end = time.time()
        msg2 = steg.extract(filename)
        ext_end = time.time()
        emb_times.append(emb_end - emb_start)
        ext_times.append(ext_end - emb_end)
    emb_times.pop(0)
    emb_times.pop(0)
    emb_times.pop(len(emb_times)-1)
    emb_times.pop(len(emb_times)-1)
    ext_times.pop(0)
    ext_times.pop(0)
    ext_times.pop(len(ext_times)-1)
    ext_times.pop(len(ext_times)-1)
    avg = sum(emb_times)/len(emb_times)
    avg2 = sum(ext_times)/len(ext_times)
    extfile = open('Average extraction times', 'a')
    embfile = open('Average embedding times', 'a')
    extfile.write(f"average extraction time of string length {str(i*5000)}: {avg2}s \n")
    embfile.write(f"average embedding time of string length of {str(i*5000)}: {avg}s \n")
"""
if __name__ == "__main__":
    string_lengths = []
    times = []
    times2 = []
    with open("timing tests/Average embedding times", 'r') as file:
        for line in file:
            str_length = line[line.find("length")+10:line.find(":")]
            string_lengths.append(str_length)                               #times were written to a txt file in error, so they needed to be read and transferred to csv for easier analysis
            time = float(line[line.find(":") + 2:].strip(" \n").strip("s"))
            times.append(time)
    file2 = open("timing tests/Average extraction times", 'r')
    for line in file2:
        time = float(line[line.find(":") + 2:].strip(" \n").strip("s"))
        times2.append(time)
    print(times2)
    print(string_lengths)
    dicti = {'length of string': string_lengths, 'avg embedding time': times,'avg decryption time': times2}
    df = pd.DataFrame(dicti)
    df.to_csv('Steg times.csv')
