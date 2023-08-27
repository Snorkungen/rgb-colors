from plot import read_csv
import json

rows = read_csv("./data/colors.csv")

with open("./data/colors.json", "w") as outfile:
    json.dump(rows, outfile)