import steg
import RSA
import encryption

if __name__ == "__main__":
    msg = "hello word"
    priv_key = RSA.gen_keys("shp")
    sym_key = encryption.gen_sym_key()
    sym_key_enc = RSA.encrypt(sym_key.decode(), "shp")
    msg_enc = encryption.encrypt_text(msg, sym_key)


    sym_key_dec = RSA.decrypt(sym_key_enc, priv_key)
    msg_dec = encryption.decrypt_text(msg_enc, sym_key_dec)


    print(msg_enc)
    print(msg_dec)
