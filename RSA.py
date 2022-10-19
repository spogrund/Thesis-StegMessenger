import rsa

def gen_keys(name):
    (public_key, private_key) = rsa.newkeys(1024)

    with open(f"keys/{name}publicKey.pem", 'wb') as p:
        p.write(public_key.save_pkcs1('PEM'))


    return private_key

def encrypt(text, name):
    with open(f"keys/{name}publicKey.pem", 'rb') as p:
        public_key = rsa.PublicKey.load_pkcs1(p.read())

    encryptedTxt = rsa.encrypt(text.encode('ascii'), public_key)
    return encryptedTxt

def decrypt(text, key):

    decryptedTxt = rsa.decrypt(text, key)

    return decryptedTxt.decode()