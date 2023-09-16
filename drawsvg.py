import utils
import math
from os import path
from filedependency import ensure_file_exists, OUT_DIR
from io import TextIOWrapper
from svg_utils import MY_SVG_TAG_BUILDER

colors = {}
max_colors = 32

def create_sort_func(color_of_intrest: str):
    rgb = utils.hex_to_rgb(color_of_intrest)
    hue, _, _ = utils.rgb_to_hsl(*rgb)

    def closest_hue(hex: str) -> int:
        h, _, _ = utils.rgb_to_hsl(*utils.hex_to_rgb(hex))
        return hue - h if hue >= h else h - hue

    return lambda hex: ([*utils.hex_to_rgb(hex)][0])

    return closest_hue


def init_contrasting_colors(
    color_of_intrest: str, color_file: TextIOWrapper
) -> list[str]:
    tmp = color_file.readlines()
    tmp.sort(key=create_sort_func(color_of_intrest), reverse=False)
    return tmp[:max_colors]


def init_color_of_interest(hex: str) -> None:
    hex = utils.rgb_to_hex(*utils.hex_to_rgb(hex))

    filename = f"color-{hex[1:]}.csv"
    ensure_file_exists(filename, ["bucket.py", hex[1:]])

    with open(path.join(OUT_DIR, filename), "r") as file:
        colors[hex] = init_contrasting_colors(hex, file)

# INIT color pages
init_color_of_interest("001a00")
init_color_of_interest("00c3ea")
init_color_of_interest("00c30d")
init_color_of_interest("00b675")

width = 25
header_height = width

font_size = int(width / 3.2)
font_size_medium = font_size / 1.95
font_size_small = font_size / 1.45
page_width = 100
row_len = int(page_width / width)
view_box_width = page_width * len(colors)
view_box_height = int(max(width * 2, (math.ceil(max_colors / row_len) / row_len) * 100))

def create_group(fg: str, bg: str, xoffset, yoffset, width, height):
    # <rect fill="{bg.strip()}" stroke="none" stroke-width="0" width="{width}" height="{height}" x="{xoffset}" y="{yoffset}" />
    ratio = utils.get_contrast_ratio(
        utils.rgb_relative_luminance(*utils.hex_to_rgb(fg)),
        utils.rgb_relative_luminance(*utils.hex_to_rgb(bg)),
    )

    return MY_SVG_TAG_BUILDER(
        name="g",
        children=[
            MY_SVG_TAG_BUILDER(
                name="text",
                attributes={
                    "fill": fg.strip(),
                    "font-size": font_size_small,
                    "x": xoffset + width / 2,
                    "y": yoffset ,
                    "text-anchor": "middle",
                    "dominant-baseline": "hanging",
                },
                children=[fg.strip()],
            ),
            MY_SVG_TAG_BUILDER(
                name="text",
                attributes={
                    "fill": fg.strip(),
                    "font-size": font_size,
                    "x": xoffset + width / 2,
                    "y": yoffset + height / 2,
                    "text-anchor": "middle",
                    "dominant-baseline": "middle",
                },
                children=[f"{ratio:.2f}"],
            ),
        ],
    )


def create_header(bg: str, fg: str, xoffset):
    return MY_SVG_TAG_BUILDER(
        name="g",
        children=[
            MY_SVG_TAG_BUILDER(
                name="rect",
                attributes={
                    "x": xoffset,
                    "width": page_width,
                    "stroke-width": 0,
                    "stroke": "none",
                    "height": header_height,
                    "fill": bg,
                },
            ),
            MY_SVG_TAG_BUILDER(
                name="text",
                attributes={
                    "x": xoffset + page_width / 2,
                    "y": header_height / 2,
                    "fill": fg,
                    "font-size": font_size,
                    "text-anchor": "middle",
                    "dominant-baseline": "middle",
                },
                children=[bg],
            ),
            MY_SVG_TAG_BUILDER(
                name="text",
                attributes={
                    "x": xoffset + page_width - font_size_medium,
                    "y": header_height,
                    "fill": fg,
                    "font-size": font_size_medium,
                    "text-anchor": "end",
                    "dominant-baseline": "text-after-edge",
                },
                children=[
                    f"Lum: {utils.rgb_relative_luminance(*utils.hex_to_rgb(bg)):.5f}"
                ],
            ),
        ],
    )


create_background = lambda color, xoffset: MY_SVG_TAG_BUILDER(
    name="rect",
    attributes={
        "x": xoffset,
        "y": header_height,
        "width": page_width,
        "height": view_box_height,
        "fill": color,
        "stroke-width": 0,
        "stroke": "none",
    },
)


def create_color_page(
    color: str, contrasting_colors: list, xoffset
) -> MY_SVG_TAG_BUILDER:
    children = [
        create_header(color, contrasting_colors[0].strip(), xoffset),
        create_background(color, xoffset),
    ]

    for i, hex in enumerate(contrasting_colors):
        children.append(
            create_group(
                hex.strip(),
                color,
                (xoffset) + (i % row_len) * width,
                header_height + int(i / row_len) * width,
                width,
                width,
            )
        )

    return MY_SVG_TAG_BUILDER(
        name="g",
        children=children,
    )


def create_svg():
    pages = []

    for i, key in enumerate(colors):
        pages.append(create_color_page(key, colors[key], page_width * i))

    return MY_SVG_TAG_BUILDER(
        name="svg",
        attributes={
            "version": 1.1,
            "width": "100%",
            "height": "100%",
            "xmlns": "http://www.w3.org/2000/svg",
            "font-family": "monospace",
            "viewBox": f"0 0 {view_box_width} {view_box_height + header_height}",
        },
        children=pages,
    ).__str__()


test = create_svg()

print(test)
