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
    if len(hex) == 3:
        hex = hex[0] * 2 + hex[1] * 2 + hex[2] * 2
    return (int(hex[:2], 16), int(hex[2:4], 16), int(hex[4:6], 16))


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


def is_relative_luminance_valid(lum: float) -> bool:
    return lum > 0.0 and lum <= 1.00002  # Floats are so great


def get_contrast_ratio(lum1: float, lum2: float) -> float:
    l, d = max(lum1, lum2), min(lum1, lum2)
    return (l + 0.05) / (d + 0.05)


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
    if delta == 0:
        h = 0
    elif cmax == red:
        h = ((green - blue) / delta) % 6
    elif cmax == green:
        h = (blue - red) / delta + 2
    else:
        h = (red - green) / delta + 4

    # Make negative hues positive behind 360°
    if h < 0:
        h += 360

    # Calculate lightness
    l = (cmax + cmin) / 2

    # Calculate saturation
    s = 0 if delta == 0 else delta / (1 - abs(2 * l - 1))

    return [h, s, l]
