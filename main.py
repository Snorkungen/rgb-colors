import os
import csv

# create data directory
if not os.path.exists('data'):
    os.mkdir('data')


def decimal_to_hex(dec):
    pad = ""
    if dec == 0: pad += "00"
    elif dec < 16: pad += "0"
    return pad + hex(dec).lstrip("0x")


def rgb_to_hex(red, green, blue):
    return f"#{decimal_to_hex(red)}{decimal_to_hex(green)}{decimal_to_hex(blue)}"


def rgb_relative_luminance(red, green, blue):

    def linear(num):
        return num / 12.92 if num <= .04045 else pow((num + .055) / 1.055, 2.4)

    red /= 255
    green /= 255
    blue /= 255

    return .2126 * linear(red) + .7152 * linear(green) + .07222 * linear(blue)

# (LL + 0.05) / (LD + 0.05) = R

def get_darker_lum (lighter_lum, ratio):
    lhs = (lighter_lum + 0.05) - ratio * 0.05
    if lhs == 0:
        return lhs
    return lhs / ratio
def get_lighter_lum (darker_lum, ratio):
    return ratio* (darker_lum + 0.05) - 0.05

def rgb_to_hsl(red, green, blue):
    # https://css-tricks.com/converting-color-spaces-in-javascript/
    red /= 255
    green /= 255
    blue /= 255
    cmax = max(red, green, blue)
    cmin = min(red, green, blue)
    delta = cmax - cmin
    h = 0
    s = 0
    l = 0

    # Calculate hue
    if (delta == 0):
        h = 0
    elif (cmax == red):
        h = ((green - blue) / delta) % 6
    elif (cmax == green):
        h = (blue - red) / delta + 2
    else:
        h = (red - green) / delta + 4

    # Make negative hues positive behind 360°
    if (h < 0): h += 360

    # Calculate lightness
    l = (cmax + cmin) / 2

    # Calculate saturation
    s = 0 if delta == 0 else delta / (1 - abs(2 * l - 1))

    return [h, s, l]


# def hsl_to_rgb(h, s, l):
#     s /= 100


# CSV Headers rgb, hex ,rel_lum
def write_to_file(file_name, fn):
    with open("data/" + file_name, "w", newline='') as csvfile:
        file_writer = csv.writer(csvfile, delimiter=",", )
        file_writer.writerow(['rgb', 'hex', 'rel_lum'])
        fn(file_writer.writerow)


def create_row(red, green, blue):
    return [
        f"({red} {green} {blue})",
        rgb_to_hex(red, green, blue),
        rgb_relative_luminance(red, green, blue)
    ]


def write_gray_scale(write):
    for i in range(256):
        write(create_row(i, i, i))


def write_red_scale(write):
    for red in range(256):
        write(create_row(red, 0, 0))


def write_green_scale(write):
    for green in range(256):
        write(create_row(0, green, 0))


def write_blue_scale(write):
    for blue in range(256):
        write(create_row(0, 0, blue))


def write_yellow_scale(write):
    for y in range(256):
        write(create_row(y, y, 0))


def write_cyan_scale(write):
    for c in range(256):
        write(create_row(0, c, c))


def write_purple_scale(write):
    for p in range(256):
        write(create_row(p, 0, p))


write_to_file("gray.csv", write_gray_scale)
write_to_file("red.csv", write_red_scale)
write_to_file("green.csv", write_green_scale)
write_to_file("blue.csv", write_blue_scale)
write_to_file("yellow.csv", write_yellow_scale)
write_to_file("cyan.csv", write_cyan_scale)
write_to_file("purple.csv", write_purple_scale)


def colors(write):
    for r in range(16 + 1):
        for g in range(16 + 1):
            for b in range(16 + 1):
                write(
                    create_row(min(r * 16, 255), min(g * 16, 255),
                               min(b * 16, 255)))


write_to_file("colors.csv", colors)
