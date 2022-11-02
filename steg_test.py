import steg
import os
import subprocess
useless = 0
num_cracked = 0
num_not_cracked = 0

files = os.listdir('audios')

print("beginning steg file detection test")

for i in range(len(files)):
    com = f"~/AudioStego/build/hideme audios/{files[i]} -f"
    text = subprocess.check_output(com, shell=True)
    if "Failed to detect a hidden file" in text.decode():
        num_not_cracked += 1
    else:
        num_cracked += 1
print("test complete")
print(f"number of Steg files: {num_cracked}")
print(f"number of non steg files: {num_not_cracked}")