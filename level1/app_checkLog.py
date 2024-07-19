import os
import sys

user = sys.argv[1]

index = 1
current_folder = os.listdir(".")
while f"{index}.txt" in current_folder:
    with open(f"{index}.txt", "r") as f:
        current_file = f.readlines()
        for l in current_file[2: ]:
            source, target, amount = l.split(", ")
            amount = amount[: -1]

            if source == user or target == user:
                print(l, end = "")
    index += 1