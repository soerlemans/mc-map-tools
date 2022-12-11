#!/usr/bin/python3


# Libraries:
import sys
import nbtlib

from wand.drawing import Drawing
from wand.image import Image
from wand.color import Color

# Local modules:
import utils
import map


def img2map(t_in, t_out='map.png'):
    '''Convert an image to a map file!'''
    # TODO: make exists a decorator
    utils.exists(t_in)
    # NBT file manipulation
    nbt = nbtlib.load(t_in)

    # print('nbt:', nbt)
    # print('colors:', nbt['data']['colors'])

    colors = nbt['data']['colors']
    base_colors = list(map.base_colors.values())

    # Draw the map to an image
    with Drawing() as draw:
        # Draw the map to an image
        for i, value in enumerate(colors):
            # TODO: For now just ignore negative values
            index = abs(int(value))
            if index < len(base_colors):
                r, g, b, a = base_colors[index]
                hex_str = f'#{r:02x}{g:02x}{b:02x}'
            else:
                # For now just ignore out of bounds colors
                value = 0

            # Draw a rough sketch of the map
            draw.alpha = a
            draw.fill_color = Color(hex_str)

            x = i % MAP_WIDTH
            y = int(i / MAP_HEIGHT)
            # print(f'x: {x}, y: {y}')
            draw.point(x, y)

            with Image(width=MAP_WIDTH, height=MAP_HEIGHT) as img:
                draw(img)
                img.save(filename=t_out)
            pass

if __name__ == '__main__':
    pass
