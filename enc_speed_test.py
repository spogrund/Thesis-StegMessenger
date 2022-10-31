import encryption
import string
import random
import time
import pandas as pd
enc_times = []
string_lengths = []
dec_times = []
enc_avg_times = []
dec_avg_times = []
key = encryption.gen_sym_key()
for i in range(1, 47):
    for j in range(20):
        msg = ''.join(random.choice(string.ascii_letters) for m in range(i*5000))
        enc_start = time.time()
        msg_enc = encryption.encrypt_text(msg, key)
        enc_end = time.time()
        msg_dec = encryption.decrypt_text(msg_enc, key)
        dec_end = time.time()
        enc_times.append(enc_end - enc_start)
        dec_times.append(dec_end - enc_end)

    enc_times.pop(0)
    enc_times.pop(0)
    enc_times.pop(len(enc_times)-1)
    enc_times.pop(len(enc_times)-1)
    dec_times.pop(0)
    dec_times.pop(0)
    dec_times.pop(len(dec_times)-1)
    dec_times.pop(len(dec_times)-1)
    string_lengths.append(str(i*5000))
    enc_avg = sum(enc_times)/len(enc_times)
    dec_avg = sum(dec_times)/len(dec_times)

    enc_avg_times.append(enc_avg)
    dec_avg_times.append(dec_avg)

dicti = {'length of string': string_lengths, 'avg encryption time': enc_avg_times, 'avg decryption time': dec_avg_times}

df = pd.DataFrame(dicti)
df.to_csv('Average times.csv')



