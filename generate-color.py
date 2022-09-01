from main import *
from random import randint

# https://www.geogebra.org/solver?i=(1%2B0.05)%2F(x%2B0.05)%3D8.59
# https://www.symbolab.com/solver?or=gms&query=(x%2B0.05)%2F(0%2B0.05)%3D21
CONTRAST_RATIO_NUM = 0.05


def contrast_ratio(lum1, lum2):
    light = max(lum1, lum2)
    dark = min(lum1, lum2)
    return (light + CONTRAST_RATIO_NUM) / (dark + CONTRAST_RATIO_NUM)


def derrive_lum_using_dark(ratio, dark_lum):
    # (x + 0.05 ) / ( 0 + 0.05 ) = 21
    return round(ratio * (dark_lum + CONTRAST_RATIO_NUM) - CONTRAST_RATIO_NUM,
                 10)


def derrive_lum_using_light(ratio, light_lum):
    # ( 1 + 0.05 ) / ( X + 0.05 ) = 21
    s = 1 / (light_lum + CONTRAST_RATIO_NUM)
    d = 1 / ratio - s * CONTRAST_RATIO_NUM
    return d / s


def derrive_lum(ratio, lum):
    result = derrive_lum_using_dark(ratio, lum)
    if round(result) > 1 + CONTRAST_RATIO_NUM:
        result = derrive_lum_using_light(ratio, lum)
    return result


def generate_contrasting_color(color, ratio=4.5):
    color_lum = rgb_relative_luminance(*color)

    derrived_lum = derrive_lum(ratio, color_lum)

    if derrived_lum < 0.001: return [0, 0, 0]
    if derrived_lum > 1.00001: return [255, 255, 255]

    contrasting_color_is_dark = color_lum > derrived_lum
    min_lum = derrived_lum if contrasting_color_is_dark == False else 0
    max_lum = derrived_lum if contrasting_color_is_dark else 1

    min_sum = 0
    max_sum = 255 * 3

    if max_lum < 0.01: max_sum = 12
    elif max_lum < 0.05: max_sum = 140
    elif max_lum < 0.1: max_sum = 280
    elif max_lum < 0.2: max_sum = 380
    elif max_lum < 0.3: max_sum = 460
    elif max_lum < 0.4: max_sum = 515
    elif max_lum < 0.5: max_sum = 565

    if min_lum > 0.9: min_sum = 760
    elif min_lum > 0.8: min_sum = 700
    elif min_lum > 0.7: min_sum = 650
    elif min_lum > 0.6: min_sum = 600
    elif min_lum > 0.5: min_sum = 540
    elif min_lum > 0.4: min_sum = 500
    elif min_lum > 0.3: min_sum = 450
    elif min_lum > 0.2: min_sum = 380
    elif min_lum > 0.1: min_sum = 235

    MAX_ATTEMPTS = 100
    cc_val = round((max_sum - min_sum + min_sum) / 3)
    for attempt in range(MAX_ATTEMPTS):
        if (max_sum - min_sum < 0):
            print("Yikes I failed")
            break

        # I do some random logic that creates a nice colour within the constraints.
        cc_val = round((max_sum - min_sum + min_sum) / 3)
        red = cc_val
        green = cc_val
        blue = cc_val

        # RANDOM LOGIC 1 
        # The best solution that i think is possible 
        if contrasting_color_is_dark:
            calc_val = lambda num: randint(0, min(num, 255))
            blue = calc_val(max_sum)
            red = calc_val(max_sum - blue)
            green = calc_val(max_sum - blue - red)
        else:
            calc_val = lambda num: randint(round(min_sum / 3), 255)
            blue = calc_val(min_sum)
            red = calc_val(min_sum - blue)
            green = calc_val(min_sum - blue - red)

        # red = randint(round(min_sum / 3), round(max_sum / 3))
        # green = randint(round(min_sum / 3), round(max_sum / 3))
        # blue = randint(round(min_sum / 3), round(max_sum / 3))

        if contrast_ratio(color_lum, rgb_relative_luminance(red, green,
                                                            blue)) > ratio:
            return [red, green, blue]

    return [cc_val, cc_val, cc_val]

