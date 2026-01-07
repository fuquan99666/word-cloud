# python main.py or python main.py --file input.txt
from .layout1 import layout_words
from .input1 import get_user_input,find,remove ,compute_counts,compute_weights
from PIL import Image,ImageDraw,ImageFont
from .style1 import select_font_sizes,select_angle,get_font,size_to_color,select_mask

WIDTH =  1600
HEIGHT = 1600
# FONT = "/System/Library/Fonts/Arial Unicode.ttf"
# FONT = "/System/Library/Fonts/Supplemental/Impact.ttf"
FONT = "Fonts/Impact.ttf"
FONT1 = "Fonts/Arial Unicode.ttf"

import argparse

def generate_word_cloud_from_text(input_text, mask_path=None, line_mode=False, zn_mode=False,max_num=800):
    processed_input = find(input_text,line_mode)

    to_remove = ['the', 'is', 'and', 'a', 'an', 'in', 'on', 'at', 'of', 'for', 'to', 'with']
    filtered_words = remove(processed_input, to_remove)
    counts, total = compute_counts(filtered_words,max_num)

    # use multi-factor weights
    weights = compute_weights(counts,total)

    mask = select_mask(mask_path,weights)
    # weights = {word: count / total for word,count in counts.items()}

    words = []
    font_sizes = select_font_sizes(weights, min_size=20, max_size=85)
    for word, weight in weights.items():
        size = font_sizes[word]
        rotate = select_angle(-60,60,5)
        words.append({"text": word, "size": size, "rotate": rotate})
    if zn_mode:
        Font = FONT1
    else:
        Font = FONT
    result = layout_words(words, Font, size=(WIDTH, HEIGHT),mask=mask)

    # paint the result in the canvas
    canvas = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    for w in result:
        text = w["text"]
        x = w["x"]
        y = w["y"]
        size = w["size"]
        rotate = w["rotate"]
        color = size_to_color(size,20,85)

        font = get_font(Font, size)

        # Create temporary transparent image
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        temp = Image.new("RGBA", (text_width,text_height), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp)

        temp_draw.text((-bbox[0],-bbox[1]), text, font=font, fill=color)

        if rotate != 0:
            temp = temp.rotate(rotate, expand=True,resample=Image.BICUBIC)

        canvas.paste(temp, (x, y), temp)
    return canvas

def main():
    parser = argparse.ArgumentParser(description='Process some input.')
    parser.add_argument('--file', type=str, help='Input file path')
    parser.add_argument('--mask', type=str,default=None, help='Mask image file path')
    parser.add_argument('--line',action='store_true',help='Whether to treat each line as a separate word')
    parser.add_argument('--max_num',type=int,default=800,help='Maximum number of words to include in the word cloud')
    arg = parser.parse_args()

    input= get_user_input(arg)

    processed_input = find(input,arg.line)

    to_remove = ['the', 'is', 'and', 'a', 'an', 'in', 'on', 'at', 'of', 'for', 'to', 'with']
    filtered_words = remove(processed_input, to_remove)
    counts, total = compute_counts(filtered_words,arg.max_num)

    # use multi-factor weights
    weights = compute_weights(counts,total)

    mask = select_mask(arg.mask,weights)
    # weights = {word: count / total for word,count in counts.items()}

    words = []
    font_sizes = select_font_sizes(weights, min_size=20, max_size=85)
    for word, weight in weights.items():
        size = font_sizes[word]
        rotate = select_angle(-60,60,5)
        words.append({"text": word, "size": size, "rotate": rotate})
    
    result = layout_words(words, FONT, size=(WIDTH, HEIGHT),mask=mask)

    # paint the result in the canvas
    canvas = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    for w in result:
        text = w["text"]
        x = w["x"]
        y = w["y"]
        size = w["size"]
        rotate = w["rotate"]
        color = size_to_color(size,20,85)

        font = get_font(FONT, size)

        # Create temporary transparent image
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        temp = Image.new("RGBA", (text_width,text_height), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp)

        temp_draw.text((-bbox[0],-bbox[1]), text, font=font, fill=color)

        if rotate != 0:
            temp = temp.rotate(rotate, expand=True,resample=Image.BICUBIC)

        canvas.paste(temp, (x, y), temp)
    canvas.show()
    # if mask:
    #     canvas.save(f"output_{mask}")
    # else:
    #     canvas.save("output.png")
    # canvas.save("temp_output.png")

if __name__ == "__main__":
    main()