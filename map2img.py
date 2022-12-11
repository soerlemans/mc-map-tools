#!/usr/bin/python3


# Libraries:
import sys
import nbtlib

from wand.drawing import Drawing
from wand.image import Image
from wand.color import Color

# Local modules:
import map_colors


# Start of script
# Argument checking
if len(sys.argv) < 2:
    print('Missing vile argument!')
    exit(1)

# NBT file manipulation
nbt_file = nbtlib.load(sys.argv[1])

# print('nbt_file:', nbt_file)
# print('colors:', nbt_file['data']['colors'])

colors = nbt_file['data']['colors']
base_colors = list(map_colors.base_colors.values())
# print('base_colors:', base_colors)

# Draw the map to an image
with Drawing() as draw:
    # Draw the map to an image
    for i, value in enumerate(colors):
        # print(i, '=', value)

        # TODO: For now just ignore negative values
        index = abs(int(value))
        if index < len(base_colors):
            r, g, b = base_colors[index]
            hex_str = f'#{r:02x}{g:02x}{b:02x}'

            # print(index)
            # print('hex_str', hex_str)
        else:
            # For now just ignore out of bounds colors
            value = 0

        # Draw a rough sketch of the map
        draw.alpha = 255 if value != 0 else 0
        draw.fill_color = Color(hex_str)

        x = i % 128
        y = int(i / 128)
        print(f'x: {x}, y: {y}')
        draw.point(x, y)

    with Image(width=128, height=128) as img:
        draw(img)
        img.save(filename='map.png')

def img2map():
    pass
