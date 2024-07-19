def overwrite(content):
    record = eval(content)

    for k, v in record.items():
        with open(k, "w") as f:
            f.write(v)