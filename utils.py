#!/usr/bin/python3


import os.path

from os import path


def exists(t_path: str) -> bool:
    if not path.exists(t_path):
        print(f'File "{t_path}" does not exist!')
        exit(3)

    if not path.isfile(t_path):
        print('Path "{t_path}" is not a file!')
        exit(4)
    pass
