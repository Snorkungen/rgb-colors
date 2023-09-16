from os import path
from progressbar import Progressbar
import utils
import csv
import sys
from filedependency import ensure_file_exists, OUT_DIR

dependency_filename = "colors-with-contrasting-color.csv"

ensure_file_exists(
    dependency_filename,
    ["generate_contrasting_colors.py"]
)

filename = path.join(OUT_DIR, dependency_filename)


COLOR_OF_INTREST =  "2020ff"
if len(sys.argv) > 1:
    COLOR_OF_INTREST = sys.argv[1]

CONTRAST_RATIO = 7.05  # Because floats are toootally accurate
contrasting_colors = list()

# compute values for intresting color
relative_luminance = utils.rgb_relative_luminance(*utils.hex_to_rgb(COLOR_OF_INTREST))

contrast_luminance = utils.get_darker_lum(relative_luminance, CONTRAST_RATIO)
is_light = utils.is_relative_luminance_valid(contrast_luminance)

if not is_light:
    contrast_luminance = utils.get_lighter_lum(relative_luminance, CONTRAST_RATIO)
    if not utils.is_relative_luminance_valid(contrast_luminance):
        raise ValueError("Color of intrest does not have a valid contrasting color")


with open(filename, "r") as file:
    reader = csv.reader(file)
    next(reader)

    rows = list(reader)
    pgbar = Progressbar(len(rows), prefix=f"computing for {COLOR_OF_INTREST}")
    for hex, rlum, _, _ in rows:
        pgbar.increment()
        if not is_light and float(rlum) < contrast_luminance:
            continue
        elif is_light and float(rlum) > contrast_luminance:
            continue

        contrasting_colors.append(hex)
    pgbar.end()

with open(path.join("data", f"color-{COLOR_OF_INTREST}.csv"), "w") as file:
    for hex in contrasting_colors:
        file.write(hex + "\n")
