import random

import steg
import RSA
import encryption
import matplotlib.pyplot as plt
import numpy as np
import wave, sys
import threading
import diffie

if __name__ == "__main__":
    msg = "hello word"
    p = diffie.get_prime()
    print(p)
    r = random.randint(1,50)
    a = random.randint(1,50)
    b = random.randint(1,50)
    A = diffie.calc_pub_key(p,r,a)
    B = diffie.calc_pub_key(p,r,b)

    k1 = diffie.calc_secret_key(p, B, a)
    k2 = diffie.calc_secret_key(p,A,b)
    k3 = encryption.gen_sym_key()


    print(k2)
    print(k3)
    enc = encryption.encrypt_text(msg, k1)
    print(enc)
    dec = encryption.decrypt_text(enc,k1)
    print(dec)
    if k1 == k2:
        print("matching")


