# in this file we try to layout the words on the canvas
from src.spiral import ArchimedeanSpiral
from src.collision import collide
from utils.style import get_font
import random
from PIL import Image, ImageDraw, ImageFont


# i think we can use a hierarchical bounding box to detect collision more efficiently
# from n*n to nlogn
# maybe even we can use a quadtree structure to do that
# now we just use simple method to loop detect collision
# to do later


spiral = ArchimedeanSpiral(step=0.2,a=0.5)


def layout(canvas, layout_words, font_sizes,padding=2):
    # we can use sprial layout to place the words 
    # and we maybe also need to use random to adjust the position a bit
    placed_words = []
    width = canvas.width
    height = canvas.height
    w = width // 2
    h = height // 2
    spiral.reset() # init the spiral before use
    draw = ImageDraw.Draw(canvas)


    for word, font_size in font_sizes.items():
        # spiral.reset()
        placed = False
        try:
            font = get_font("/Library/Fonts/Arial Unicode.ttf", font_size)
        except Exception as e:
            print(f"Error loading font for word '{word}': {e}. Using default font.")
            font = ImageFont.load_default()
        
        while not placed: 
            x,y = spiral.next_point()
            # adjust position randomly a bit until it fits the constraints
            x_offset = random.randint(-5,5)
            y_offset = random.randint(-5,5)
            x_pos = w + x + x_offset
            y_pos = h + y + y_offset
            # check if the word fits in the canvas
            if collide(x_pos, y_pos, font, word,placed_words, width, height,padding=padding):
                continue # try next point in spiral
            else:
                # place the word
                layout_words[word] = (int(x_pos),int(y_pos), font_size)
                placed_words.append((x_pos, y_pos, font_size,word))
                placed = True
                # draw the word on the canvas
                print(f"Placing word '{word}' at ({int(x_pos)}, {int(y_pos)}) with font size {font_size}")
                draw.text((int(x_pos), int(y_pos)), word, fill=(0,0,0), font=font)
                
    return layout_words




