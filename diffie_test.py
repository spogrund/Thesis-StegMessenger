"""
PGRSAM001
EEE4022S
Final year project
Key exchange test module
"""
import random
import encryption
import diffie

#generate 100 different keys using random values and check if they match
if __name__ == "__main__":
    num_success = 0
    num_failure = 0
    print("Beginning matching key test")
    for i in range(100):
        p = diffie.get_prime()
        r = random.randint(1,5000)
        a = random.randint(1,5000)
        b = random.randint(1,5000)
        A = diffie.calc_pub_key(p,r,a)
        B = diffie.calc_pub_key(p,r,b)

        k1 = diffie.calc_secret_key(p, B, a)
        k2 = diffie.calc_secret_key(p,A,b)
        k3 = encryption.gen_sym_key()
        if k1 == k2:
            num_success +=1
        else:
            num_failure +=1
    print("Test complete")
    print(f"NUmber of successes = {num_success}")
    print(f"number of failures = {num_failure}")


