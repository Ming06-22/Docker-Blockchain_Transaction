import os
import hashlib

from checkChain import checkChain

def hash_file(filename):
    h = hashlib.sha256()
    with open(filename, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            h.update(byte_block)
    return h.hexdigest()

def checkAllChains():
    check, m = checkChain()
    folder= os.listdir()
    i = 1
    while f"{i + 1}.txt" in folder:
        i += 1
    sha_value = hash_file(f"{i}.txt")

    i = 1
    record = {}
    folder = os.listdir()
    while f"{i}.txt" in folder:
        with open(f"{i}.txt", "r") as f:
            content = f.read()
        record[f"{i}.txt"] = content
        i += 1

    return check, sha_value, str(record)