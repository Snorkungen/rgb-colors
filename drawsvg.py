import utils
import math
from os import path
from filedependency import ensure_file_exists, OUT_DIR

color_of_intrest = "#2020ff"
filename = f"color-{color_of_intrest[1:]}.csv"

ensure_file_exists(filename, ["bucket.py"])

with open(path.join(OUT_DIR, filename), "r") as file:
    contrasting_colors = file.readlines()


width = 12.5
header_height = width / 2
font_size = int(width / 3.125)
page_width = 100
view_box_width = 100
row_len = int(view_box_width / width)
view_box_height = int(
    max(width * 2, (math.ceil(len(contrasting_colors) / row_len) / row_len) * 100)
)

def create_group(fg: str, bg: str, xoffset, yoffset, width, height):
    # <rect fill="{bg.strip()}" stroke="none" stroke-width="0" width="{width}" height="{height}" x="{xoffset}" y="{yoffset}" /> 
    ratio = (utils.get_contrast_ratio(utils.rgb_relative_luminance(*utils.hex_to_rgb(fg)),utils.rgb_relative_luminance(*utils.hex_to_rgb(bg))))
    return f"""<g>
        <text fill="{fg.strip()}" font-size="{font_size / 2}" x="{xoffset + width / 2}" y="{yoffset+  font_size / 2}" text-anchor="middle" dominant-baseline="hanging" >{fg.strip()}</text>
        <text fill="{fg.strip()}" font-size="{font_size}" x="{xoffset + width / 2}" y="{yoffset+height/2}" text-anchor="middle" dominant-baseline="middle" >{ratio:.2f}</text>
    </g>"""

def create_header(bg:str,fg:str, xoffset):
# <rect width="{view_box_width}" stroke-width="0" stroke="none" height="{1}" fill="{fg}" y="{header_height - 1}" />
    return f"""<g>
<rect x="{xoffset}" width="{view_box_width}" stroke-width="0" stroke="none" height="{header_height}" fill="{bg}" />
<text x="{xoffset + page_width/2}" y="{header_height/2}" fill="{fg}" font-size="{font_size}"  text-anchor="middle" dominant-baseline="middle">{bg}</text>
</g>"""

create_background = lambda xoffset: f'<rect x="{xoffset}" y="{header_height}" width="{page_width}" height="{view_box_height}" fill="{color_of_intrest}" stroke="none" stroke-width="0" />'

def create_color_page(color: str, contrasting_colors: list, xoffset) -> str:
    groups = ""

    for i, hex in enumerate(contrasting_colors):    
            groups += create_group(
                hex,
                color_of_intrest,
                (i % row_len) * width,
                header_height + int(i / row_len) * width,
                width,
                width,
            )
    
    return f"""<g>
        {create_header(color, contrasting_colors[0], xoffset)}
        {create_background(xoffset)}
        {groups}
</g>""" 

def create_svg(bg: str):
    return f"""<svg version="1.1"
        width="100%"
        xmlns="http://www.w3.org/2000/svg"
        font-family="monospace"
        viewBox="0 0 {view_box_width} {view_box_height + header_height}">
        {create_color_page(color_of_intrest,contrasting_colors, 0)}
</svg>"""#.replace("\n", "")


test = create_svg(color_of_intrest)

print(test)
