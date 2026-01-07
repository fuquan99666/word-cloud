# in this file ,we convert text to pixels and handle rotate here

from PIL import Image, ImageDraw, ImageFont
from .style1 import get_font
import numpy as np
import math


def rasterize_text(text, font_path, font_size, rotate=0):
    font = get_font(font_path, font_size)
    
    bbox = font.getbbox(text)
    # print(bbox[0], bbox[1], bbox[2], bbox[3])
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    # print(bbox[0], bbox[1], bbox[2], bbox[3])
    # print("w,h:",w,h)
    img = Image.new('L', (w, h),0)
    draw = ImageDraw.Draw(img)
    # draw.text((w/2,h/2), text, fill=255, font=font,anchor='mm')

    draw.text((-bbox[0],-bbox[1]),text, fill=255, font=font)

    # draw.text((0,0), text, fill=255, font=font,anchor='lt')

    if rotate != 0:
        img = img.rotate(rotate, expand=1)
    arr = np.array(img)
    mask = arr > 0
    # for row in mask:
    #     print(row.astype(int))
    mask = mask.astype(int)

    # for row in mask:
    #     print("".join(map(str, row)))

    return mask