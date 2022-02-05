"""Generates a CSS radial gradient that fits the input image.

E.g.:
python3 gradient.py drain_bg_2.jpg
"""

import math
import sys

from PIL import Image, ImageColor

_NUM_BANDS = 32
_BAND_SWEEP_SIZE = 40
_BAND_SWEEP_STEP = 5
_SHRINK_AMOUNT = 0.75

def pixel_add(a, b):
  assert len(a) == len(b)
  return tuple([x+y for x,y in zip(a,b)])

def pixel_scalar_div(a, b):
  return tuple([x / b for x in a])

def pixel_to_hex_color(p):
  assert len(p) == 3
  return "#" + "".join([hex(int(x))[2:].zfill(2) for x in p])

gradient = []

with Image.open(sys.argv[1]) as img:
  for band in range(_NUM_BANDS):
    pixel_sum = (0,0,0)
    num_pixels = 0
    for angle_deg in range(0, 360, 1):
      for band_sweep in range(0, _BAND_SWEEP_SIZE, _BAND_SWEEP_STEP):
        # Distance from image edge.
        band_size = max(img.width, img.height) / 2.0 / _NUM_BANDS
        band_start = (band) * band_size
        band_end = (band + 1) * band_size

        band_sweep_amount = band_sweep / _BAND_SWEEP_SIZE

        band_pos = band_start * (1.0 - band_sweep_amount) + band_end * band_sweep_amount

        band_pos *= _SHRINK_AMOUNT

        angle_rad = math.radians(angle_deg)
        x = math.cos(angle_rad) * band_pos + img.width / 2.0
        y = math.sin(angle_rad) * band_pos + img.height / 2.0

        if x < 0 or x >= img.width or y < 0 or y >= img.height:
          continue
        pixel = img.getpixel((x, y))

        pixel_sum = pixel_add(pixel, pixel_sum)
        num_pixels += 1
    
    mean = pixel_scalar_div(pixel_sum, num_pixels)

    gradient.append(mean)

#gradient = list(reversed(gradient))
print("radial-gradient(circle, " + ", ".join([pixel_to_hex_color(g) for g in gradient]) + ")")

