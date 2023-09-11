from os import path
from progressbar import Progressbar
import csv

filename = path.join("data", "colors-with-contrasting-color-test.csv")

thing = dict()


contrasting_colors = list()

COLOR_OF_INTREST = "#2020ff"


with open(filename, "r") as file:
    reader = csv.reader(file)
    next(reader)

    rows = list (reader)
    pgbar = Progressbar(len(rows),prefix="")


    for row in rows:
        hex, rlum, light, clum = row
        thing[hex] = {"rlum": rlum, "light": light, "clum": clum, "lst": list()}
        break

    for key in thing:
        d = thing[key]
        dl = d["light"]

        # pgbar.update(0)

        
        for hex, rlum, light, clum in reader:
            pgbar.increment()


            # TODO THE Logic below is broken
            if dl == "False" and float(rlum) < float(d["clum"]):
                continue
            if dl == "True" and float(rlum) > float(d["clum"]):                
                continue

            thing[key]["lst"].append(hex)
        pgbar.end()


with open(path.join("data", "thing.yaml?"), "w") as file:
    for key in thing:
        file.write(f"{key}:\n")
        for hex in thing[key]["lst"]:
            file.write(f"\t{hex}\n")
