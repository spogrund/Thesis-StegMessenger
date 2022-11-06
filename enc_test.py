"""
PGRSAM001
EEE4022S
Final year project
Encryption entropy test module
"""

import encryption
import random
import pandas as pd
import string
from math import log

#method to calculate the shannon entropy of a text and calculate the maximum possible entropy
def shannon(string):
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
max_entropies = []
random_entropies1 = []
lengths = []
random_entropies2 = []
#generate increasing length of strings to test their entropy.
for j in range(1, 100):
    msg = ''
    for i in range(j*10):
        msg += wordsList[random.randint(0, len(wordsList)-1)] + ' '
    lengths.append(len(msg))
    msg2 = ''.join(chr(random.randint(0, 128)) for m in range(len(msg)))
    msg3 = ''.join(chr(random.randint(0, 128)) for m in range(len(msg)*100))
    key = encryption.gen_sym_key()
    msg_enc = encryption.encrypt_text(msg, key)
    entropy, max_entropy = shannon(msg_enc.decode())
    entropies.append(entropy)
    max_entropies.append(max_entropy)
    rnd_entropy, max_entropy = shannon(msg2)
    random_entropies1.append(rnd_entropy)
    rnd_entropy, max_entropy = shannon(msg3)
    random_entropies2.append(rnd_entropy)
print(entropies)
print(max_entropies)
print(random_entropies1)
print(random_entropies2)
dicti = {'length of string': lengths, 'avg entropy': entropies, 'avg entropy of same length': random_entropies1, 'average entropy of lenght x 100': random_entropies2}
df = pd.DataFrame(dicti)
df.to_csv('entropy.csv')


