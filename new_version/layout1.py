# layout.py
from new_version.raster import rasterize_text
from new_version.sprite import raster_to_sprite
from new_version.board import Board
from new_version.placer import place_sprite
from PIL import Image
import numpy as np
from new_version.style1 import convert_transparent_to_mask


def layout_words(words, font_path, size=(800, 800),mask=None):
    board = Board(*size)
    if mask:
        mask_img = convert_transparent_to_mask(mask, "temp_mask.png")
        mask_img = mask_img.resize(size, Image.BICUBIC)
        mask_data = np.array(mask_img)
        threshold = 250
        binary_mask = (mask_data > threshold).astype(int)
        mask_sprite = raster_to_sprite(binary_mask)
        if mask_sprite:
            board.add_boundary(mask_sprite[0])
    cx, cy = size[0] // 2, size[1] // 2

    results = []

    # words = sorted(words, key=lambda w: w["size"], reverse=True)

    for w in words:
        mask = rasterize_text(
            w["text"],
            font_path,
            w["size"],
            rotate=w["rotate"],
        )
        sprite = raster_to_sprite(mask)
        if not sprite:
            continue

        pos = place_sprite(board, sprite,w['text'], cx, cy)
        if pos:
            results.append({
                "text": w["text"],
                "x": pos[0],
                "y": pos[1],
                "size": w["size"],
                "rotate": w["rotate"],
            })
    # board.print_board()

    return results
