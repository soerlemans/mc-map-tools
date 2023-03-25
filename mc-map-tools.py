#!/usr/bin/env python3


import sys

import img2map
import map2img


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
        print('Pass atleast three arguments.')
        print_help()
        exit(1)

    operation = sys.argv[1]
    in_file = sys.argv[2]
    out_file = sys.argv[3] if argc >= 4 else None
    file_idx = int(sys.argv[4]) if argc >= 5 else 0

    func = None
    if operation == 'img':
        func = img2map.img2map
    elif operation == 'map':
        func = map2img.map2img
    else:
        print('Invalid operation!')
        print_help()
        exit(2)

    # Determine if we should use the default argument
    # None evaluates to False
    if out_file:
        func(in_file, out_file, t_start = file_idx)
    else:
        func(in_file)

    pass
