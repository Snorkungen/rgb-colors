def rgb_to_hex(red, green, blue):

    def decimal_to_hex(dec):
        pad = ""
        if dec == 0: pad += "0"
        if dec < 16: pad += "0"
        return pad + hex(dec).lstrip("0x").rstrip("L")

    return f"#{decimal_to_hex(red)}{decimal_to_hex(green)}{decimal_to_hex(blue)}"


def rgb_relative_luminance(red, green, blue):

    def linear(num):
        return num / 12.92 if num <= .04045 else pow((num + .055) / 1.055, 2.4)

    red /= 255
    green /= 255
    blue /= 255

    return .2126 * linear(red) + .7152 * linear(green) + .07222 * linear(blue)


def print_color_line(red, green, blue):
    print(
        f"({red} {green} {blue}),{rgb_to_hex(red,green,blue)},{round(rgb_relative_luminance(red,green,blue),6)}"
    )


# CSV Headers rgb, hex ,rel_lum
print("rgb,hex,rel_lum")

for r in range(256):
    for g in range(256):
        for b in range(0,256,2):
            print_color_line(r,g,b)
