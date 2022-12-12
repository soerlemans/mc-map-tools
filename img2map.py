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
    needed_splits = ratio_width * ratio_height
    print(f'Splitting into {needed_splits} images')

    imgs = []
    counter = 0
    for x in range(ratio_width):
        for y in range(ratio_height):
            counter += 1

            x_start = x * DEFAULT_WIDTH
            y_start = y * DEFAULT_HEIGHT

            print(f'{x_start} {DEFAULT_WIDTH} {y_start} {DEFAULT_HEIGHT} {y}')
            img = t_img[x_start:DEFAULT_WIDTH, y_start:DEFAULT_HEIGHT]

            print(f'Img ({counter}/{needed_splits}) starts at: x: {x_start} y: {y_start}')
            imgs.append((x_start, y_start, img))

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

def img2map(t_in: str, t_out: str = 'custom_map.dat', t_default_map: str = 'map.dat'):
    '''Create a map nbt file out of an image.
    This requires a map file for copying purposes.'''
    # TODO: make exists a decorator
    utils.exists(t_in)
    utils.exists(t_default_map)

    # TODO: Fix this this does not work yet
    # nbt = map_defaults()
    # nbt.filename = t_out

    full_img = Image(filename=t_in)

    nbt_colors = []
    colors = get_colors()

    # Images are in a list they can be iterated through and mapped
    # To different, nbt files
    splits = split_img(full_img)

    for img_idx, (x_start, y_start, img) in enumerate(splits):
        backup_out = f'{t_out.removesuffix(".dat")}_{str(img_idx)}.png'
        map_out = t_out if not img_idx else backup_out

        # Copy the default map file
        shutil.copyfile(t_default_map, map_out)

        # NBT file manipulation
        nbt = nbtlib.load(map_out)

        width = img.width
        height = img.height

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

