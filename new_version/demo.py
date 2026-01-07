## for look
from new_version.raster import rasterize_text
from new_version.sprite import raster_to_sprite
from new_version.board import Board

word1 = 'fuck you :'
word2 = 'jello'

board = Board(128,200)


mask1 = rasterize_text(word1, "/Library/Fonts/Arial Unicode.ttf", 30, rotate=0)
mask2 = rasterize_text(word2, "/Library/Fonts/Arial Unicode.ttf", 30, rotate=0)

sprite1 = raster_to_sprite(mask1)
sprite2 = raster_to_sprite(mask2)

board.place(sprite1,0,0)
board.place(sprite2,0,100)

board.print_board()

# for row in rows :
#     print(row)



# from layout1 import layout_words
# from style1 import get_font

# FONT = "/Library/Fonts/Arial Unicode.ttf"
# WIDTH = 800
# HEIGHT = 800

# words = [
#     {"text": "Python", "size": 30, "rotate": 30},
#     {"text": "Bitmask", "size": 20, "rotate": 90},
#     {"text": "WordCloud", "size": 30, "rotate": 0},
#     {"text": "Spiral", "size": 30, "rotate": -45},
#     {"text": "Collision", "size": 15, "rotate": 0},
#     {"text": "Placement", "size": 25, "rotate": 15},
#     {"text": "Algorithm", "size": 20, "rotate": -30},
#     {"text": "Visualization", "size": 35, "rotate": 0},
#     {"text": "Graphics", "size": 20, "rotate": 60},
#     {"text": "Rendering", "size": 25, "rotate": -15},
#     {"text": "Text", "size": 15, "rotate": 0},
#     {"text": "Image is a so great thing!", "size": 15, "rotate": 88},
# ]


# result = layout_words(words, FONT,size=(WIDTH,HEIGHT))

# # paint the result in the canvas
# from PIL import Image,ImageDraw,ImageFont


# # 1️⃣ 创建最终画布
# image = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
# draw = ImageDraw.Draw(image)

# # 2️⃣ 逐个词渲染
# for w in result:
#     text = w["text"]
#     x = w["x"]
#     y = w["y"]
#     size = w["size"]
#     rotate = w["rotate"]
#     color = w.get("color", (0, 0, 0))

#     font = get_font(FONT, size)

#     # 2.1 创建临时透明图（和 raster 思路一致）
#     bbox = font.getbbox(text)
#     text_width = bbox[2] - bbox[0]
#     text_height = bbox[3] - bbox[1]
#     temp = Image.new("RGBA", (text_width,text_height), (0, 0, 0, 0))
#     temp_draw = ImageDraw.Draw(temp)

#     # 左上角画字（和 layout 中的 sprite 左上角一致）
#     temp_draw.text((-bbox[0],-bbox[1]), text, font=font, fill=color)

#     # 2.2 旋转（如果需要）
#     if rotate != 0:
#         temp = temp.rotate(rotate, expand=True)

#     # 2.3 粘贴到主画布
#     image.paste(temp, (x, y), temp)

# image.show()
