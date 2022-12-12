#!/usr/bin/python3


# Libraries:
import sys
import nbtlib

from wand.drawing import Drawing
from wand.image import Image
from wand.color import Color

# Local modules:
import utils

from map_prop import *


def map2img(t_in, t_out='map.png') -> None:
    '''Convert a map to an image!'''
    # TODO: make exists a decorator
    utils.exists(t_in)

    # NBT file manipulation
    nbt = nbtlib.load(t_in)

    nbt_colors = nbt['data']['colors']

    # Draw the map to an image
    with Drawing() as draw:
        # Loop through the maps color values and draw them to the image
        for i, color_id in enumerate(nbt_colors):
            r, g, b, a =  get_color(color_id)
            color_str = f'#{r:02x}{g:02x}{b:02x}'

            # Set the color values
            draw.alpha = a
            draw.fill_color = Color(color_str)

            # Calculate x and y coordinates
            x = i %  DEFAULT_WIDTH
            y = i // DEFAULT_HEIGHT

            # Draw the maps point
            print(f'x: {x}, y: {y} = r: {r}, g: {g} b: {b} a: {a}')
            draw.point(x, y)

        print(f'Done now saving to {t_out}')
        # Save the image
        with Image(width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT) as img:
            draw(img)
            img.save(filename=t_out)
        pass

if __name__ == '__main__':
    pass
