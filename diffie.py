import hashlib
import random

from sympy import *
"""
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

def get_prime():
    with open("primes.txt", "rb") as file:
        for i in range(random.randint(0,100)):
            p = file.readline()
        p = int((p.decode()))
        return p

def calc_pub_key(p, r, a):
    return r**a % p

def calc_secret_key(p,A,b):
    key = A**b % p
    key = hashlib.sha256(str(key).encode()).hexdigest()
    key = key[:len(key)//2]
    return key.encode()

