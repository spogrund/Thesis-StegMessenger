"""
PGRSAM001
EEE4022S
Final year project
Diffie-Hellman key exchange module
"""

import hashlib
import random
from sympy import *

"""
initial acquisition of suitable primes for the key exchange
min = 2**2048
primes = []
with open("primes.txt", "w") as file:
    for i in range(100):
        prime = nextprime(min)
        min = prime
        primes.append(prime)
        file.write(f"{str(prime)}\n")
        print(i)
    print(primes)
"""

#get a suitable prime from the pre acquired list
def get_prime():
    with open("primes.txt", "rb") as file:
        for i in range(random.randint(0,100)):
            p = file.readline()
        p = int((p.decode()))
        return p

#method to calculate public key from a private value, prime and root
def calc_pub_key(p, r, a):
    return r**a % p

#method to calculate secret key from prime, public key and private value
def calc_secret_key(p,A,b):
    key = A**b % p
    key = hashlib.sha256(str(key).encode()).hexdigest()
    key = key[:len(key)//2]
    return key.encode()

