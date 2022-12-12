#!/usr/bin/python3
'''
Contains information and data about minecraft map properties.
'''


from typing import Tuple

from nbtlib import *


# Globals:
# Default map width and height
DEFAULT_WIDTH = 128
DEFAULT_HEIGHT = 128

# Dictionary of all possible base color values that can be used in a map
BASE_COLORS = {
    'NONE' : (0, 0, 0, 0),
    'GRASS' : (127, 178, 56, 255),
    'SAND' : (247, 233, 163, 255),
    'WOOL' : (199, 199, 199, 255),
    'FIRE' : (255, 0, 0, 255),
    'ICE' : (160, 160, 255, 255),
    'METAL' : (167, 167, 167, 255),
    'PLANT' : (0, 124, 0, 255),
    'SNOW' : (255, 255, 255, 255),
    'CLAY' : (164, 168, 184, 255),
    'DIRT' : (151, 109, 77, 255),
    'STONE' : (112, 112, 112, 255),
    'WATER' : (64, 64, 255, 255),
    'WOOD' : (143, 119, 72, 255),
    'QUARTZ' : (255, 252, 245, 255),
    'COLOR_ORANGE' : (216, 127, 51, 255),
    'COLOR_MAGENTA' : (178, 76, 216, 255),
    'COLOR_LIGHT_BLUE' : (102, 153, 216, 255),
    'COLOR_YELLOW' : (229, 229, 51, 255),
    'COLOR_LIGHT_GREEN' : (127, 204, 25, 255),
    'COLOR_PINK' : (242, 127, 165, 255),
    'COLOR_GRAY' : (76, 76, 76, 255),
    'COLOR_LIGHT_GRAY' : (153, 153, 153, 255),
    'COLOR_CYAN' : (76, 127, 153, 255),
    'COLOR_PURPLE' : (127, 63, 178, 255),
    'COLOR_BLUE' : (51, 76, 178, 255),
    'COLOR_BROWN' : (102, 76, 51, 255),
    'COLOR_GREEN' : (102, 127, 51, 255),
    'COLOR_RED' : (153, 51, 51, 255),
    'COLOR_BLACK' : (25, 25, 25, 255),
    'GOLD' : (250, 238, 77, 255),
    'DIAMOND' : (92, 219, 213, 255),
    'LAPIS' : (74, 128, 255, 255),
    'EMERALD' : (0, 217, 58, 255),
    'PODZOL' : (129, 86, 49, 255),
    'NETHER' : (112, 2, 0, 255),
    'TERRACOTTA_WHITE' : (209, 177, 161, 255),
    'TERRACOTTA_ORANGE' : (159, 82, 36, 255),
    'TERRACOTTA_MAGENTA' : (149, 87, 108, 255),
    'TERRACOTTA_LIGHT_BLUE' : (112, 108, 138, 255),
    'TERRACOTTA_YELLOW' : (186, 133, 36, 255),
    'TERRACOTTA_LIGHT_GREEN' : (103, 117, 53, 255),
    'TERRACOTTA_PINK' : (160, 77, 78, 255),
    'TERRACOTTA_GRAY' : (57, 41, 35, 255),
    'TERRACOTTA_LIGHT_GRAY' : (135, 107, 98, 255),
    'TERRACOTTA_CYAN' : (87, 92, 92, 255),
    'TERRACOTTA_PURPLE' : (122, 73, 88, 255),
    'TERRACOTTA_BLUE' : (76, 62, 92, 255),
    'TERRACOTTA_BROWN' : (76, 50, 35, 255),
    'TERRACOTTA_GREEN' : (76, 82, 42, 255),
    'TERRACOTTA_RED' : (142, 60, 46, 255),
    'TERRACOTTA_BLACK' : (37, 22, 16, 255),
    'CRIMSON_NYLIUM' : (189, 48, 49, 255),
    'CRIMSON_STEM' : (148, 63, 97, 255),
    'CRIMSON_HYPHAE' : (92, 25, 29, 255),
    'WARPED_NYLIUM' : (22, 126, 134, 255),
    'WARPED_STEM' : (58, 142, 140, 255),
    'WARPED_HYPHAE' : (86, 44, 62, 255),
    'WARPED_WART_BLOCK' : (20, 180, 133, 255),
    'DEEPSLATE' : (100, 100, 100, 255),
    'RAW_IRON' : (216, 175, 147, 255),
    'GLOW_LICHEN' : (127, 167, 150, 255),
}

# Functions:
def calculate_shade_color(t_base_id, t_modifier) -> Tuple[int, int, int, int]:
    '''Calculates the proper color on basis of the modifier, for a base color ID.'''
    colors = get_base_color(t_base_id)
    func = lambda t_x: t_x * t_modifier // 255

    return tuple(map(func, colors))

def get_base_color(t_id) -> Tuple[int, int, int, int]:
    return list(BASE_COLORS.values())[t_id]

def get_color(t_id) -> Tuple[int, int, int, int]:
    '''Converts a given ID to its proper ID with shade.'''
    base_id, offset = divmod(t_id, 4)

    modifier = 1
    if offset == 0:
        modifier = 180
    elif offset == 1:
        modifier = 220
    elif offset == 2:
        modifier = 1
    elif offset == 3:
        modifier = 135
    else:
        print('Somehow we got an incorrect offset for a color!')
        exit(5)

    colors = calculate_shade_color(base_id, modifier)

    return colors

def get_colors() -> list:
    '''Return all colors with shades in a list.'''
    colors_len = len(BASE_COLORS) * 4
    colors = []

    for i in range(colors_len):
        base_id, offset = divmod(i, 4)
        color = get_color(i)

        r, g, b, a = color
        print(f'Getting shade color -> base_id: {base_id} offset: {offset} r: {r} g: {g} b: {b} a: {a}')

        colors.append(color)

    print('Returning colors')
    return colors

def map_defaults() -> File:
    '''Creates a map with the most sensible default settings.'''
    nbt_map = nbt.File(gzipped=True, byteorder='little', filename='')
    nbt_map['data'] = Compound()

    # Set Minecraft data version to latest version as of 12/12/2022
    #nbt_map['DataVersion'] = Int(3218) # 1.19.3

    # My server uses 1.19.2
    nbt_map['DataVersion'] = Int(3120) # 1.19.2

    # Set data section:
    # Create a reference to the data dict
    data = nbt_map['data']

    data['scale'] = Byte(0) # Set nbt_map scale to 1:1
    data['dimension'] = Byte(1) # Set dimension to overworld

    # Tracking settings:
    data['trackingPosition'] = Byte(0) # Do not show the player location arrow
    data['unlimitedTracking'] = Byte(0) # Do not show tracking position from unlimited distance

    # Lock the nbt_map so it wont change
    data['locked'] = Byte(1)

    # Set X and Z centers
    data['xCenter'] = Int(0)
    data['yCenter'] = Int(0)

    # Banners:
    data['banners'] = List([]) # Set no banners

    # Frames:
    data['frames'] = List([]) # Set no frames

    # Colors:
    data['colors'] = ByteArray([Byte(0)])

    return nbt_map
