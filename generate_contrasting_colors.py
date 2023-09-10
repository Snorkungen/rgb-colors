from os import path, mkdir
from typing import Final
import csv


def decimal_to_hex(dec):
    pad = ""
    if dec == 0:
        pad += "00"
    elif dec < 16:
        pad += "0"
    return pad + hex(dec).lstrip("0x")


def rgb_to_hex(red, green, blue):
    return f"#{decimal_to_hex(red)}{decimal_to_hex(green)}{decimal_to_hex(blue)}"


def hex_to_rgb(hex) -> (int, int, int):
    if hex[0] == "#":
        hex = hex[1:]
    return (int(hex[:2], 16), int(hex[2:4], 16), int(hex[4:], 16))


def rgb_relative_luminance(red, green, blue):
    linear = (
        lambda num: num / 12.92 if num <= 0.04045 else pow((num + 0.055) / 1.055, 2.4)
    )

    red /= 255
    green /= 255
    blue /= 255

    return 0.2126 * linear(red) + 0.7152 * linear(green) + 0.07222 * linear(blue)


# (LL + 0.05) / (LD + 0.05) = R
def get_darker_lum(lighter_lum, ratio):
    lhs = (lighter_lum + 0.05) - ratio * 0.05
    if lhs == 0:
        return lhs
    return lhs / ratio


def get_lighter_lum(darker_lum, ratio):
    return ratio * (darker_lum + 0.05) - 0.05


OUT_DIR: Final = "data"
OUT_FILE: Final = "colors-with-contrasting-color-test.csv"
MIN_CONTRAST_RATIO: Final = 7

# create data directory
if not path.exists(OUT_DIR):
    mkdir(OUT_DIR)

from color_factory import ColorFactorySimple
from progressbar import Progressbar


with open(path.join(OUT_DIR, OUT_FILE), "w", newline="") as csv_out_file:
    writer = csv.writer(csv_out_file)
    writer.writerow(["hex", "rel_lum", "light"])

    cfac = ColorFactorySimple(inc=15)
    pgbar = Progressbar(cfac.total(), "computing")

    for color in cfac:
        pgbar.increment()
        rlum = rgb_relative_luminance(*color)
        dlum = get_darker_lum(rlum, MIN_CONTRAST_RATIO)

        is_light = dlum > 0 and dlum < 1

        if not is_light:
            llum = get_lighter_lum(rlum, MIN_CONTRAST_RATIO)

            if llum > 0 and llum < 1:
                is_light = False
            else:
                continue

        writer.writerow([rgb_to_hex(*color), rlum, is_light])
    pgbar.end()

