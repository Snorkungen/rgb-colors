import utils
import math
from os import path
from filedependency import ensure_file_exists, OUT_DIR
from io import TextIOWrapper

color_of_intrest = "#1a0000"
color_of_intrest2 = "#00001a"
color_of_intrest3 = "#00005b"

colors = {}
max_colors = 32
width = 25
header_height = width / 2

font_size = int(width / 3.2)
font_size_medium = font_size / 1.95
font_size_small = font_size / 1.45
page_width = 100
view_box_width = 3 * page_width
row_len = int(page_width / width)
view_box_height = int(max(width * 2, (math.ceil(max_colors / row_len) / row_len) * 100))

filename = f"color-{color_of_intrest[1:]}.csv"
ensure_file_exists(filename, ["bucket.py", color_of_intrest[1:]])


def create_sort_func(color_of_intrest: str):
    rgb = utils.hex_to_rgb(color_of_intrest)
    hue, _, _ = utils.rgb_to_hsl(*rgb)

    def closest_hue(hex: str) -> int:
        h, _, _ = utils.rgb_to_hsl(*utils.hex_to_rgb(hex))
        return hue - h if hue >= h else h - hue

    # return lambda hex: ([*utils.hex_to_rgb(hex)][0])

    return closest_hue


def init_contrasting_colors(
    color_of_intrest: str, color_file: TextIOWrapper
) -> list[str]:
    tmp = color_file.readlines()
    tmp.sort(key=create_sort_func(color_of_intrest), reverse=False)
    return tmp[:max_colors]


with open(path.join(OUT_DIR, filename), "r") as file:
    colors[color_of_intrest] = init_contrasting_colors(color_of_intrest, file)

filename = f"color-{color_of_intrest2[1:]}.csv"
ensure_file_exists(filename, ["bucket.py", color_of_intrest2[1:]])

with open(path.join(OUT_DIR, filename), "r") as file:
    colors[color_of_intrest2] = init_contrasting_colors(color_of_intrest2, file)

filename = f"color-{color_of_intrest3[1:]}.csv"
ensure_file_exists(filename, ["bucket.py", color_of_intrest3[1:]])

with open(path.join(OUT_DIR, filename), "r") as file:
    colors[color_of_intrest3] = init_contrasting_colors(color_of_intrest3, file)


def create_group(fg: str, bg: str, xoffset, yoffset, width, height):
    # <rect fill="{bg.strip()}" stroke="none" stroke-width="0" width="{width}" height="{height}" x="{xoffset}" y="{yoffset}" />
    ratio = utils.get_contrast_ratio(
        utils.rgb_relative_luminance(*utils.hex_to_rgb(fg)),
        utils.rgb_relative_luminance(*utils.hex_to_rgb(bg)),
    )
    return f"""<g>
        <text fill="{fg.strip()}" font-size="{font_size_small}" x="{xoffset + width / 2}" y="{yoffset+  font_size / 2}" text-anchor="middle" dominant-baseline="hanging" >{fg.strip()}</text>
        <text fill="{fg.strip()}" font-size="{font_size}" x="{xoffset + width / 2}" y="{yoffset+height/2}" text-anchor="middle" dominant-baseline="middle" >{ratio:.2f}</text>
    </g>"""


def create_header(bg: str, fg: str, xoffset):
    # <rect width="{view_box_width}" stroke-width="0" stroke="none" height="{1}" fill="{fg}" y="{header_height - 1}" />
    return f"""<g>
<rect x="{xoffset}" width="{page_width}" stroke-width="0" stroke="none" height="{header_height}" fill="{bg}" />
<text x="{xoffset + page_width/2}" y="{header_height/2}" fill="{fg}" font-size="{font_size}" text-anchor="middle" dominant-baseline="middle">{bg}</text>
<text x="{xoffset + page_width - font_size_medium}" y="{header_height}" fill="{fg}" font-size="{font_size_medium}" text-anchor="end" dominant-baseline="text-after-edge">Lum:{utils.rgb_relative_luminance(*utils.hex_to_rgb(bg)):.5f}</text>
</g>"""


create_background = (
    lambda color, xoffset: f'<rect x="{xoffset}" y="{header_height}" width="{page_width}" height="{view_box_height}" fill="{color}" stroke="none" stroke-width="0" />'
)


def create_color_page(color: str, contrasting_colors: list, xoffset) -> str:
    groups = ""

    for i, hex in enumerate(contrasting_colors):
        groups += create_group(
            hex,
            color,
            (xoffset) + (i % row_len) * width,
            header_height + int(i / row_len) * width,
            width,
            width,
        )

    return f"""<g>
        {create_header(color, contrasting_colors[0], xoffset)}
        {create_background(color,xoffset)}
        {groups}
</g>"""


def create_svg(bg: str):
    return f"""<svg version="1.1"
        width="100%"
        xmlns="http://www.w3.org/2000/svg"
        font-family="monospace"
        viewBox="0 0 {view_box_width} {view_box_height + header_height}">
        {create_color_page(color_of_intrest,colors[color_of_intrest], 0)}
        {create_color_page(color_of_intrest2,colors[color_of_intrest2], page_width)}
        {create_color_page(color_of_intrest3,colors[color_of_intrest3], page_width + page_width)}
</svg>"""  # .replace("\n", "")


test = create_svg(color_of_intrest)

print(test)
