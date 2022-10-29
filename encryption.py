from Crypto.Cipher import AES
import base64, os

def gen_sym_key():
    AES_key_len = 16
    secret_key = os.urandom(AES_key_len)
    encoded_secret_key = base64.b64encode(secret_key)

    return encoded_secret_key

def encrypt_text(text, encoded_secret_key):
    secret_key = base64.b64decode(encoded_secret_key)
    cipher = AES.new(secret_key)
    key_length = len(secret_key)
    msg_padded = text + ((16-len(text))%16 * '$')
    msg_encrypted = cipher.encrypt(msg_padded)
    msg_encrypted_encoded = base64.b64encode(msg_encrypted)

    return msg_encrypted_encoded

def decrypt_text(msg_encrypted_encoded, encoded_secret_key):
    secret_key = base64.b64decode(encoded_secret_key)
    msg_encrypted = base64.b64decode(msg_encrypted_encoded)
    cipher = AES.new(secret_key)
    msg_padded = cipher.decrypt(msg_encrypted).decode()
    msg = msg_padded.rstrip('$')

    return msg

