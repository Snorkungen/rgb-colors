from os import path
from progressbar import Progressbar
import csv

filename = path.join("data", "colors-with-contrasting-color-test.csv")

thing = dict()

with open(filename, "r") as file:
    reader = csv.reader(file)
    next(reader)

    pgbar = Progressbar(1)

    for row in reader:
        hex, rlum, light, clum = row
        thing[hex] = {"rlum": rlum, "light": light, "clum": clum, "lst": list()}
        break

    for key in thing:
        d = thing[key]
        pgbar.prefix = f"computing {key}"
        pgbar.update(0)
        for hex, rlum, light, clum in reader:
            pgbar.count += 1
            pgbar.increment()


            # TODO THE Logic below is broken
            if not bool(light) and float(rlum) > float(d["clum"]):
                pass
            if bool(light) and float(rlum) < float(d["clum"]):
                pass
            else:
                continue

            thing[key]["lst"].append(hex)


with open(path.join("data", "thing.yaml?"), "w") as file:
    for key in thing:
        file.write(f"{key}:\n")
        for hex in thing[key]["lst"]:
            file.write(f"\t{hex}\n")
