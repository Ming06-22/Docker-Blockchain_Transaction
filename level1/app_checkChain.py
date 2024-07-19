import os, sys
import hashlib

def hash_file(filename):
    h = hashlib.sha256()
    with open(filename, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            h.update(byte_block)
    return h.hexdigest()

currDir = os.listdir(".")
filename = "1.txt"

while filename and f"{filename}" in currDir:
    with open(filename, "r") as f:
        lines = f.readlines()

        hash_value = hash_file(filename)

        nxt_block = lines[1].split(": ")[-1][: -1]

        if filename == "1.txt":
            filename = nxt_block
            prev = hash_value
        else:
            sha = lines[0].split(": ")[-1][:-1]
            if sha == prev:
                filename = nxt_block
                prev = hash_value
            else:
                print("Error!", filename)
                exit()
print('OK!')