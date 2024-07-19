import sys
import os

user = sys.argv[1]

index = 1
balance = 0
current_folder = os.listdir(".")
while f"{index}.txt" in current_folder:
    with open(f"{index}.txt", "r") as f:
        current_file = f.readlines()
        for l in current_file[2: ]:
            source, target, ammount = l.split(" ")
            source, target, ammount = source[: -1], target[: -1], float(ammount[: -1])

            if source == user:
                balance -= ammount
            elif target == user:
                balance += ammount
    index += 1

print(f"The balance of {user} is {balance}.")