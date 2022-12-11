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


# Functions:
def closest_color(t_color, t_color_options):
    '''Find the color that looks most like another color from a list.'''
    color_diffs = []
    pr, pg, pb = t_color

    for i, value in enumerate(t_color_options):
        cr, cg, cb, _ = value

        color_diff = abs(pr - cr) + abs(pg - cg) + abs(pb - cg)
        color_diffs.append((color_diff, i))

    return min(color_diffs)

def img2map(t_in, t_out='custom_map.nbt', t_map='map.dat'):
    '''Create a map nbt file out of an image.
    This requires a map file for copying purposes.'''
    # TODO: make exists a decorator
    utils.exists(t_in)

    # NBT file manipulation
    nbt = nbtlib.load(t_map)

    nbt_colors_size = DEFAULT_WIDTH * DEFAULT_HEIGHT
    nbt_colors = []
    colors = get_colors()

    print('nbt colors:', nbt['data'])

    with Image(filename=t_in) as img:
        blob = img.make_blob(format='RGB')
        for i in range(0, len(blob), 3):
            pr = blob[i]
            pg = blob[i + 1]
            pb = blob[i + 2]

            closest = closest_color((pr, pg, pb), colors)
            # print('closest: ', closest)

            if i < nbt_colors_size:
                nbt_colors.append(nbtlib.Byte(closest[1]) - 30)
            else:
                break

    # print("nbt: ", nbt_colors)
    nbt['data']['colors'] = nbtlib.ByteArray(nbt_colors)

    # nbt.save()
    pass

