from os import path, mkdir
from typing import Final
import csv
from utils import *

OUT_DIR: Final = "data"
OUT_FILE: Final = "colors-with-contrasting-color-test.csv"
MIN_CONTRAST_RATIO: Final = 7.3
COLOR_FACTORY_SIMPLE_INC: Final = 16

# create data directory
if not path.exists(OUT_DIR):
    mkdir(OUT_DIR)

from color_factory import ColorFactorySimple
from progressbar import Progressbar


with open(path.join(OUT_DIR, OUT_FILE), "w", newline="") as csv_out_file:
    writer = csv.writer(csv_out_file)
    writer.writerow(["hex", "rel_lum", "light", "contrast_lum"])

    cfac = ColorFactorySimple(inc=COLOR_FACTORY_SIMPLE_INC)
    pgbar = Progressbar(cfac.total(), "computing")

    for color in cfac:
        pgbar.increment()
        rlum = rgb_relative_luminance(*color)
        clum = get_darker_lum(rlum, MIN_CONTRAST_RATIO)

        is_light = clum > 0 and clum < 1

        if not is_light:
            clum = get_lighter_lum(rlum, MIN_CONTRAST_RATIO)

            if clum > 0 and clum < 1:
                is_light = False
            else:
                continue

        writer.writerow([rgb_to_hex(*color), rlum, is_light, clum])
    pgbar.end()
