#!/usr/bin/env bash


# Arguments
in_file="${1}"
out_file="${2}"

# TODO: Fix the hardcoded sizes
# Dont allow just any size
size="${3:-128}"

# TODO: Maps can be zoomed out and resized
convert "$in_file" -resize "${size}x${size}^" "$out_file"
convert "$out_file" -gravity center -crop 128x128+0+0 +repage "$out_file"
