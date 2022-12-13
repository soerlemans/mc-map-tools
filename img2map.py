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
def print_view(t_x, t_y, t_w, t_h, t_corner='+'):
    '''Print the location of the map in a graph'''
    frame = t_corner + '-' * t_w + t_corner
    print(frame)
    for y in range(t_h):
        print('|', end='')
        for x in range(t_w):
            char = '#' if x == t_x and y == t_y else '.'
            print(char, end='')
        print('|')
    print(frame)
    pass

def round_up_img(t_img:Image) -> Image:
    width, height = t_img.size
    ratio_width
    pass

def split_img(t_img: Image) -> list:
    '''Split one image into multiple, so it fits into a map.'''
    if t_img.width <= DEFAULT_WIDTH and t_img.height <= DEFAULT_HEIGHT:
        print('Image does not need to be split')
        return [(0, 0, t_img)]

    ratio_width = math.ceil(t_img.width / DEFAULT_WIDTH)
    ratio_height = math.ceil(t_img.height / DEFAULT_HEIGHT)
    needed_splits = ratio_width * ratio_height
    print(f'Splitting into {needed_splits} images')

    imgs = []
    counter = 0
    for y_idx in range(ratio_height):
        for x_idx in range(ratio_width):
            counter += 1

            x = x_idx * DEFAULT_WIDTH
            y = y_idx * DEFAULT_HEIGHT

            img = t_img.clone()
            img.crop(x, y, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)

            print(f'x: {x_idx} y: {y_idx}')
            print_view(x_idx, y_idx, ratio_width, ratio_height)
            print(f'Splitting image ({counter}/{needed_splits})\n')
            imgs.append((x, y, img))

    return imgs

def closest_color(t_color: Tuple[int, int, int], t_color_options: list) -> list:
    '''Find the color that looks most like another color from a list.'''
    pr, pg, pb = t_color

    color_diffs = []
    for i, value in enumerate(t_color_options):
        cr, cg, cb, _ = value

        color_diff = sqrt((pr - cr)**2 + (pg - cg)**2 + (pb - cg)**2)
        color_diffs.append((color_diff, i))

    return min(color_diffs)

def img2map(t_in: str, t_out: str = 'custom_map.dat', t_default_map: str = 'map.dat', t_start = 0):
    '''Create a map nbt file out of an image.
    This requires a map file for copying purposes.'''
    # TODO: make exists a decorator
    utils.exists(t_in)
    utils.exists(t_default_map)

    # TODO: Fix this this does not work yet
    # nbt = map_defaults()
    # nbt.filename = t_out

    full_img = Image(filename=t_in, background='WHITE')

    colors = get_colors()

    # Images are in a list they can be iterated through and mapped
    # To different, nbt files
    splits = split_img(full_img)

    for img_idx, (x_start, y_start, img) in enumerate(splits):
        file_idx = img_idx + t_start
        backup_out = f'{t_out.removesuffix(".dat")}_{str(file_idx)}.dat'
        map_out = t_out if not file_idx else backup_out

        # Copy the default map file
        shutil.copyfile(t_default_map, map_out)

        # NBT file manipulation
        nbt = nbtlib.load(map_out)
        nbt_colors = []

        blob = img.make_blob(format='RGB')
        for blob_idx in range(0, len(blob), 3):
            pr = blob[blob_idx]
            pg = blob[blob_idx + 1]
            pb = blob[blob_idx + 2]

            closest = closest_color((pr, pg, pb), colors)
            # print('closest: ', closest)

            # Use from unsiged to get the full 0 - 255 range
            byte = nbtlib.Byte.from_unsigned(closest[1])
            nbt_colors.append(byte)

            # print(f'blob_idx: {blob_idx} byte: {byte}')

        # Split this into a seperate function
        # Copy the color array to its proper location
        nbt['data']['colors'] = nbtlib.ByteArray(nbt_colors)

        print(f'Done with image {img_idx + 1}/{len(splits)} saving to {map_out}')
        nbt.save()
    pass

