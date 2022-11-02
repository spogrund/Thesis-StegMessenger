import encryption
import random

import string
from math import log

def shannon(string):


# if isinstance(string, unicode):
#   string = string.encode("ascii")
    ent = 0.0
    max_ent = 0.0
    if len(string) < 2:
        return ent, max_ent
    size = float(len(string))
    for b in range(128):
        max_ent = max_ent + (float(size/128)/size)*log((float(size/128)/size),2)
        freq = string.count(chr(b))
        if freq > 0:
            freq = float(freq) / size
            ent = ent + freq * log(freq, 2)

    return -ent, -max_ent

words = []
file = open('word_list.txt', 'r')
wordsList = file.read().split("\n")
msg = ''
entropies = []

for j in range(46):
    for i in range(j*100):
        msg += wordsList[random.randint(0,len(wordsList))] + ' '

    key = encryption.gen_sym_key()
    msg_enc = encryption.encrypt_text(msg, key)
    entropy, max_entropy = shannon(msg_enc.decode())
    entropies.append(entropy)
print(entropies)
print(max_entropy)


