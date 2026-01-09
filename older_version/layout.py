# in this file we try to layout the words on the canvas
from spiral import ArchimedeanSpiral
from collision import collide
from style import get_font,size_to_color,Orientation
import random,math
from PIL import Image, ImageDraw, ImageFont


# i think we can use a hierarchical bounding box to detect collision more efficiently
# from n*n to nlogn
# maybe even we can use a quadtree structure to do that
# now we just use simple method to loop detect collision
# to do later


spiral = ArchimedeanSpiral(step=0.2,a=0.5)


def layout(canvas, layout_words, font_sizes,padding=2,min_size=20,max_size=85):
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

        dir = random.choice(Orientation)
        
        while not placed: 
            x,y = spiral.next_point()
            # adjust position randomly a bit until it fits the constraints
            x_offset = random.randint(-5,5)
            y_offset = random.randint(-5,5)
            x_pos = w + x + x_offset
            y_pos = h + y + y_offset
            # check if the word fits in the canvas
            if collide(x_pos, y_pos, font, word,placed_words, width, height,dir,padding=padding):
                continue # try next point in spiral
            else:
                # place the word
                layout_words[word] = (int(x_pos),int(y_pos), font_size)
                placed_words.append((x_pos, y_pos, font_size,word,dir))
                placed = True
                # draw the word on the canvas
                print(f"Placing word '{word}' at ({int(x_pos)}, {int(y_pos)}) with font size {font_size}")
                color = size_to_color(font_size, min_size, max_size)

                # draw.text((int(x_pos), int(y_pos)), word, fill=color, font=font, angle=dir)
                # first create a temporary image to draw the rotated text
                bbox = font.getbbox(word)
                text_width = bbox[2] - bbox[0]
                print(f"{bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}")
                text_height = bbox[3] - bbox[1]
                # r = int(math.sqrt(text_width**2 + text_height**2))
                # temp_image = Image.new('RGBA', (r, r), (255, 255, 255, 0))
                # temp_draw = ImageDraw.Draw(temp_image)  
                # temp_draw.text((0, 0), word, font=font, fill=color)
                # rotated_image = temp_image.rotate(dir, expand=1)
                # if dir == 90:
                #     move = r - text_width
                # else:
                #     move = 0
                # canvas.paste(rotated_image, (int(x_pos), int(y_pos)-move), rotated_image)
                temp_image = Image.new('RGBA', (text_width, text_height), (255, 255, 255, 0))
                temp_draw = ImageDraw.Draw(temp_image)
                
                # 在 (0, 0) 绘制文字，注意要抵消 bbox 的起始偏移 (-bbox[0], -bbox[1])
                # 这样文字会紧贴图片的左上角，避免留白
                temp_draw.text((-bbox[0], -bbox[1]), word, font=font, fill=color)
                
                # 旋转图片，expand=1 会自动调整图片大小以适应旋转后的内容
                rotated_image = temp_image.rotate(dir, expand=1)
                
                # 直接粘贴到 (x_pos, y_pos)，不需要额外的 move 计算
                # 因为 rotated_image 现在就是紧凑的文字包围盒
                canvas.paste(rotated_image, (int(x_pos), int(y_pos)), rotated_image)
    return layout_words




