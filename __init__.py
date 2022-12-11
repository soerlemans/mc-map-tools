#!/usr/bin/python3


import sys

from img2map import *
from map2img import *


def print_help():
    print('''Usage:
    ./__init__.py <operation> <in> <out>
    <operation> = img(2map) | map(2img)
    <in> = Input file
    <out> = Output file

    If <out> gets ommited defaults to either''')
    pass

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 3:
        print('Not enough arguments!')
        print('Pass atleast three arguments.')
        print_help()
        exit(1)

    operation = sys.argv[1]
    in_file = sys.argv[2]
    out_file = sys.argv[3] if argc >= 4 else None

    func = None
    if operation == 'img':
        func = img2map
    elif operation == 'map':
        func = map2img
    else:
        print('Invalid operation!')
        print_help()
        exit(2)

    # Check to see if we need to use default arg or not
    if out_file:
        func(in_file, out_file)
    else:
        func(in_file)

    pass
