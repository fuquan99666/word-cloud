# placer.py
from spiral1 import ArchimedeanSpiral


def place_sprite(board, sprite,word ,cx, cy, max_steps=6500):
    spiral = ArchimedeanSpiral(step=1)

    for _ in range(max_steps):
        dx, dy = next(spiral)
        x = int(cx + dx)
        y = int(cy + dy)

        if x < 0 or y < 0:
            continue
        if x + sprite[1] >= board.width:
            continue
        if y + sprite[2] >= board.height:
            continue

        if board.can_place(sprite, x, y):
            board.place(sprite, x, y)
            return x, y
    print(f'Failed to place word: {word}')

    return None
