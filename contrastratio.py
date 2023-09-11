
import sys
import utils

c1, c2 = sys.argv[1:]

lum1 = utils.rgb_relative_luminance(*utils.hex_to_rgb(c1))
lum2 = utils.rgb_relative_luminance(*utils.hex_to_rgb(c2))


ratio = utils.get_contrast_ratio(lum1, lum2)

print(f"Ratio is {ratio:.2f}")