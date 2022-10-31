import encryption
import random
import string
words = []
file = open('word_list.txt', 'r')
wordsList = file.read().split("\n")
msg = ''
for i in range(500):
    msg += wordsList[random.randint(0,len(wordsList))] + ' '

key = encryption.gen_sym_key()


print(msg)
msg_enc = encryption.encrypt_text(msg, key)
file = open("encryptedText.txt", 'w')
file.write(msg_enc.decode())

