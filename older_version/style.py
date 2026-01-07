# in this file we select styles like font size, color based on the weights
# and all the things related to style of the image

from PIL import ImageFilter, Image, ImageDraw, ImageFont



def select_font_sizes(weights, min_size=10, max_size=100):
    # select font sizes based on weights
    font_sizes = {}
    min_weight = min(weights.values())
    max_weight = max(weights.values())
    for word, weight in weights.items():
        normalized_size = (weight - min_weight) / (max_weight - min_weight) + 0.000001

        # use exponential sacling to make size differences more sinificant
        exponent = 0.1
        scaled = normalized_size ** exponent
        font_size = min_size + (max_size - min_size) * scaled
        font_sizes[word] = int(font_size)
    return font_sizes

# to do , we do this after we complete the other parts 
def extract_boundary(image, threshold=100):
    # extract the boundary of the image
    # 转换为灰度
    gray = image.convert('L')
    
    # 使用查找边缘滤波器
    edges = gray.filter(ImageFilter.FIND_EDGES)
    
    # 增强边缘对比度
    # 边缘处理为白色，背景为黑色
    edges = edges.point(lambda x: 255 if x > threshold else 0)
    return edges

# we can use fixed canvas or let user upload their own canvas
# this canvas is meant to be the boundary of the word cloud
# not the background image

# abiviously, the size of the canvas should think about the size of the word font
# and we should adjust that , but we can do that later
def create_canvas(width=800, height=600, color=(255, 255, 255),file_path=None,threshold=100):
    from PIL import Image

    # if user don't provide a canvas, we create a block canvas
    if file_path is None:
        canvas = Image.new('RGB', (width, height), color)
    else:
        # the question is how to extract the boundary from the image
        canvas = Image.open(file_path)
        canvas = extract_boundary(canvas,threshold=threshold)
        canvas = canvas.resize((width, height))
    return canvas



# use a font cache to speed up font loading
font_cache = {}

def get_font(font_name, font_size):
    if font_name not in font_cache:
        font_cache[font_name] = {}
    
    if font_size in font_cache[font_name]:
        return font_cache[font_name][font_size]
    else:
        # create a new cache entry
        try:
            font = ImageFont.truetype(font_name, font_size)
        except:
            font = ImageFont.load_default()
        font_cache[font_name][font_size] = font
        return font
    


# create color select 

def size_to_color1(size, min_size, max_size):
    t = (size - min_size) / (max_size - min_size)
    r = int(80 + 150 * t)
    g = int(50 + 150 * (1 - t))
    b = int(150 + 105 * (1 - t))
    return (r, g, b)

import colorsys
def size_to_color(size, min_size, max_size):
    t = (size - min_size) / (max_size - min_size)
    
    # 色相从蓝 → 红（更醒目）
    hue = (1 - t) * 0.9   # 0.6=蓝, 0=红
    sat = 0.75
    val = 0.9

    r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
    return (int(r*255), int(g*255), int(b*255))

def lerp(a, b, t):
    return a + (b - a) * t

def size_to_color2(size, min_size, max_size):
    t = (size - min_size) / (max_size - min_size)

    cold = (70, 120, 200)   # 蓝
    warm = (220, 90, 60)    # 红橙

    r = int(lerp(cold[0], warm[0], t))
    g = int(lerp(cold[1], warm[1], t))
    b = int(lerp(cold[2], warm[2], t))

    return (r, g, b)



# create angle select
Orientation = [0,0,-90,90]

