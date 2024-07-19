import os
from hashlib import sha256

def transaction(message):
    source, target, amount = message[0], message[1], message[2]

    index = 1
    current_folder = os.listdir(".")
    if "1.txt" not in current_folder:
        with open("1.txt", "w") as f:
            f.write("Sha 256 of previous block: None(first block)\n")
            f.write("Next block: None\n")
            f.write(f"{source}, {target}, {amount}\n")
        return

    while f"{index + 1}.txt" in current_folder:
        index += 1

    with open(f"{index}.txt", "r") as f:
        current_file = f.readlines()

    if len(current_file) == 7:
        with open(f"{index}.txt", "w") as f:
            f.write(current_file[0])
            f.write(f"Next block: {index + 1}.txt\n")
            for i in range(2, 7):
                f.write(current_file[i])

        sha256_hash = sha256()
        with open(f"{index}.txt", "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
            hash_value = sha256_hash.hexdigest()

        with open(f"{index + 1}.txt", "w") as f:
            f.write(f"Sha 256 of previous bolck: {hash_value}\n")
            f.write("Next block: None\n")
            f.write(f"{source}, {target}, {amount}\n")
    else:
        with open(f"{index}.txt", "a") as f:
            f.write(f"{source}, {target}, {amount}\n")