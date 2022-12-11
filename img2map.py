#!/usr/bin/python3


# Libraries:
import math
import shutil
import sys
import nbtlib

from typing import Tuple

from wand.drawing import Drawing
from wand.image import Image
from wand.color import Color

# Local modules:
import utils
from map_prop import *


# Functions:
def split_img(t_img: Image) -> list:
    if t_img.width <= DEFAULT_WIDTH and t_img.height <= DEFAULT_HEIGHT:
        print('Image does not need to be split')
        return [t_img]

    ratio_width = math.ceil(t_img.width / DEFAULT_WIDTH)
    ratio_height = math.ceil(t_img.height / DEFAULT_height)
    print(f'Splitting into {ratio_width * ratio_height} images')

    ret = []
    for x in range(ratio_width):
        for y in range(ratio_height):
            x_start = ratio_width * x
            y_start = ratio_height * y
            img = t_img.clone(left=x_start, top=y_start,
                              width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)
            print(f'Copying quadrants: x: {x_start} y: {y_start}')
            ret.append(img)
    pass

def closest_color(t_color: Tuple[int, int, int], t_color_options: list) -> list:
    '''Find the color that looks most like another color from a list.'''
    color_diffs = []
    pr, pg, pb = t_color

    for i, value in enumerate(t_color_options):
        cr, cg, cb, _ = value

        color_diff = abs(pr - cr) + abs(pg - cg) + abs(pb - cg)
        color_diffs.append((color_diff, i))

    return min(color_diffs)

def img2map(t_in: str, t_out: str = 'custom_map.dat'):
    '''Create a map nbt file out of an image.
    This requires a map file for copying purposes.'''
    # TODO: make exists a decorator
    utils.exists(t_in)

    # Check if our template map exists
    src_map = 'map.dat'
    utils.exists(src_map)

    # Copy the default map file
    shutil.copyfile(src_map, t_out)

    # NBT file manipulation
    nbt = nbtlib.load(t_out)

    nbt_colors = []
    colors = get_colors()

    # print('nbt colors:', nbt['data'])

    with Image(filename=t_in) as img:
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

    # Copy the color array to its proper location
    nbt['data']['colors'] = nbtlib.ByteArray(nbt_colors)

    print(f'Done now saving to {t_out}')
    nbt.save()
    pass

