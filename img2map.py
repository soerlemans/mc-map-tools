#!/usr/bin/python3


# Libraries:
import math
import shutil
import sys
import nbtlib

from math import sqrt
from typing import Tuple

from wand.drawing import Drawing
from wand.image import Image
from wand.color import Color

# Local modules:
import utils
from map_prop import *


# Functions:
def split_img(t_img: Image) -> list:
    '''Split one image into multiple.'''
    if t_img.width <= DEFAULT_WIDTH and t_img.height <= DEFAULT_HEIGHT:
        print('Image does not need to be split')
        return [(0, 0, t_img)]

    ratio_width = math.ceil(t_img.width / DEFAULT_WIDTH)
    ratio_height = math.ceil(t_img.height / DEFAULT_HEIGHT)
    print(f'Splitting into {ratio_width * ratio_height} images')

    imgs = []
    for x in range(ratio_width):
        for y in range(ratio_height):
            x_start = ratio_width * x
            y_start = ratio_height * y
            img = t_img.clone(left=x_start, top=y_start,
                              width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
            print(f'Img starts at: x: {x_start} y: {y_start}')
            imgs.append(tuple(x_start, y_start, img))
    pass

def closest_color(t_color: Tuple[int, int, int], t_color_options: list) -> list:
    '''Find the color that looks most like another color from a list.'''
    pr, pg, pb = t_color

    color_diffs = []
    for i, value in enumerate(t_color_options):
        cr, cg, cb, _ = value

        color_diff = sqrt((pr - cr)**2 + (pg - cg)**2 + (pb - cg)**2)
        color_diffs.append((color_diff, i))

    return min(color_diffs)

def img2map(t_in: str, t_out: str = 'custom_map.dat', t_map: str = 'map.dat'):
    '''Create a map nbt file out of an image.
    This requires a map file for copying purposes.'''
    # TODO: make exists a decorator
    utils.exists(t_in)

    # Check if our template map exists
    utils.exists(t_map)

    # Copy the default map file
    # shutil.copyfile(t_map, t_out)

    # NBT file manipulation
    # nbt = nbtlib.load(t_out)
    nbt = map_defaults()
    nbt.filename = t_out

    nbt_colors = []
    colors = get_colors()

    with Image(filename=t_in) as img:
        # Images are in a list they can be iterated through and mapped
        # To different, nbt files
        imgs = split_img(img)

        width = img.width
        height = img.height

        blob = img.make_blob(format='RGB')
        print('blob:', len(blob))

        for i in range(0, len(blob), 3):
            pr = blob[i]
            pg = blob[i + 1]
            pb = blob[i + 2]

            closest = closest_color((pr, pg, pb), colors)
            # print('closest: ', closest)

            # Use from unsiged to get the full 0 - 255 range
            byte = nbtlib.Byte.from_unsigned(closest[1])
            nbt_colors.append(byte)

            print(f'i: {i} byte: {byte}')

    # Split this into a seperate function
    # Set some of the map properties
    nbt['data']['locked'] = nbtlib.Byte(1)
    nbt['data']['xCenter'] = nbtlib.Int(0)
    nbt['data']['zCenter'] = nbtlib.Int(0)

    # Copy the color array to its proper location
    nbt['data']['colors'] = nbtlib.ByteArray(nbt_colors)

    print(f'Done now saving to {t_out}')
    nbt.save()
    pass

