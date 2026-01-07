# in this file we select styles like font size, color based on the weights
# and all the things related to style of the image

from PIL import ImageFilter, Image, ImageDraw, ImageFont

def convert_transparent_to_mask(image_path, output_path):
    # 1. 打开原始图片 (确保它是 RGBA 模式)
    original = Image.open(image_path).convert("RGBA")

    # 2. 创建一个纯白色的背景图，大小和原图一样
    # (255, 255, 255, 255) 代表纯白色且完全不透明
    new_background = Image.new("RGBA", original.size, (255, 255, 255, 255))

    # 3. 将原图叠加到白底上 (alpha_composite 会正确处理透明度)
    # 现在透明部分变成了白色，黑色部分依然是黑色
    combined = Image.alpha_composite(new_background, original)

    # 4. 转换为最终的灰度遮罩图 (L 模式)
    # 结果：黑色(0) 是苹果形状，白色(255) 是背景
    final_mask = combined.convert("L")

    # 5. 保存结果 (可选，方便查看)也可以直接返回对象在代码里用
    # final_mask.save(output_path)
    # final_mask.show() # 如果想直接看看结果，取消注释这一行
    return final_mask

def select_font_sizes1(weights, min_size=10, max_size=100):
    # select font sizes based on weights
    font_sizes = {}
    min_weight = min(weights.values())
    max_weight = max(weights.values())
    for word, weight in weights.items():
        normalized_size = (weight - min_weight) / (max_weight - min_weight) + 0.000001

        # use exponential sacling to make size differences more sinificant
        exponent = 0.7
        scaled = normalized_size ** exponent
        font_size = min_size + (max_size - min_size) * scaled
        font_sizes[word] = int(font_size)
    return font_sizes

def select_font_sizes(weights, min_size=10, max_size=100):
    font_sizes = {}

    min_weight = min(weights.values())
    max_weight = max(weights.values())

    if max_weight == min_weight:
        return {word: (min_size + max_size) // 2 for word in weights}

    for word, weight in weights.items():
        t = (weight - min_weight) / (max_weight - min_weight)

        # 非线性
        t = t ** 0.4

        # 量化为 6 个视觉层级
        levels = 6
        t = round(t * levels) / levels

        font_size = min_size + (max_size - min_size) * t
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


import colorsys
def size_to_color1(size, min_size, max_size):
    t = (size - min_size) / (max_size - min_size)
    
    # 色相从蓝 → 红（更醒目）
    hue = (1 - t) * 0.9   # 0.6=蓝, 0=红
    sat = 0.75
    val = 0.9

    r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
    return (int(r*255), int(g*255), int(b*255))

def lerp(a, b, t):
    return a + (b - a) * t

def size_to_color3(size, min_size, max_size):
    t = (size - min_size) / (max_size - min_size)

    cold = (70, 120, 200)   # 蓝
    warm = (220, 90, 60)    # 红橙

    r = int(lerp(cold[0], warm[0], t))
    g = int(lerp(cold[1], warm[1], t))
    b = int(lerp(cold[2], warm[2], t))

    return (r, g, b)

PALETTE = [
    # --- 第一梯队：核心重色（高饱和、低明度，用于大词，压住阵脚） ---
    (62, 68, 129),    # 浓郁靛蓝（对应 "WORD", "placed"）- 比之前更深、更纯
    (113, 114, 63),   # 深苔藓绿（对应 "algorithm", "area"）- 提高浓郁度
    (139, 68, 65),    # 铁锈红（对应 "collision", "implementation"）- 增加暖感

    (46, 52, 92),     # 夜靛蓝 / 深海军蓝（比靛蓝更冷，适合“SYSTEM / CORE”级词）
    (58, 82, 68),     # 深松针绿 / 冷森林绿（比苔藓绿更理性）


    # --- 第二梯队：明亮跳色（高亮度，用于中型词，产生视觉跳跃） ---
    (204, 168, 100),  # 琥珀金/深黄（对应 "retrieve", "box"）- 这种黄色非常提神
    (133, 135, 189),  # 丁香紫/亮蓝（对应 "sprite", "move"）- 增加色彩的多样性
    (185, 132, 146),  # 玫瑰灰/干粉（对应 "expensive", "detection"）

    # --- 第三梯队：清透过渡色（低饱和，用于小词，增加层次感） ---
    (177, 164, 214),  # 浅熏衣草紫
    (220, 210, 174),  # 羊皮纸色/米色
    (150, 180, 150),  # 浅草绿（原图中偶尔出现的清新色调）
]

PALETTE1 = [
    # --- 靛蓝系 ---
    (54, 60, 108),
    (62, 68, 120),
    (70, 76, 132),
    (58, 64, 115),

    # --- 橄榄绿系 ---
    (88, 112, 62),
    (96, 122, 63),
    (104, 130, 72),
    (92, 118, 68),

    # --- 砖红系 ---
    (124, 72, 68),
    (134, 76, 72),
    (142, 84, 78),
    (128, 80, 76),

    # --- 赭黄系 ---
    (112, 98, 62),
    (123, 106, 58),
    (132, 114, 68),
    (118, 104, 64),

    # --- 冷灰蓝系 ---
    (142, 148, 170),
    (150, 160, 180),
    (160, 168, 192),
    (148, 156, 175),
]


def size_to_color(size, min_size, max_size):
    t = (size - min_size) / (max_size - min_size)

    # if t > 0.7:
    #     pool = PALETTE[0:3]      # 深蓝系（大词）
    # elif t > 0.4:
    #     pool = PALETTE[3:7]      # 紫 / 红
    # else:
    #     pool = PALETTE[7:]       # 橄榄 / 米色（小词）

    return random.choice(PALETTE)

def size_to_color2(size, min_size, max_size):
    t = (size - min_size) / (max_size - min_size)
    t = max(0.0, min(1.0, t))

    # 基础色相（偏蓝灰，耐看）
    base_hue = 0.58   # 蓝灰
    hue_jitter = random.uniform(-0.03, 0.03)

    hue = base_hue + hue_jitter

    # 饱和度低一点，避免抢戏
    sat = 0.45

    # 亮度随 size 变化（这是重点）
    val = 0.5 + 0.35 * t   # 小词暗，大词亮

    r, g, b = colorsys.hsv_to_rgb(hue, sat, val)
    return (int(r*255), int(g*255), int(b*255))



# create angle select
def select_angle1(size, min_size, max_size):
    t = (size - min_size) / (max_size - min_size)
    angle = int(lerp(-30, 63, 1 - t))  # smaller size → larger angle
    return angle


import random
import math

def select_angle(min_angle,max_angle,n):
    # 分层设计
    levels = n
    angle_levels = []
    for i in range(levels):
        t = i / (levels - 1)
        angle = int(lerp(min_angle, max_angle, t))
        angle_levels.append(angle)
    angle = random.choice(angle_levels)
    return angle

topic_masks = {
    "love": "masks/heart.png",
    "nature": "masks/tree.png",
    "dog": "masks/dog.png",
    "dance": "masks/dancer.png",
    "beautiful": "masks/dancer.png",
    "china": "masks/china.png",
    "food": "masks/apple.png",
    "apple": "masks/apple.png",
    "circle": "masks/circle.png",
    "good": "masks/heart.png",
}

def select_mask(arg,weights):
    if arg.mask:
        return arg.mask
    else:
        # select the most weighted word as the topic word
        weights = list(weights.items())
        first_word = weights[0][0]
        # second_word = weights[1][0] if len(weights) > 1 else first_word
        # third_word = weights[2][0] if len(weights) > 2 else second_word
        print("First word:", first_word)
        if first_word in topic_masks:
            print("Selected mask for topic:", first_word)
            return topic_masks[first_word]
        else:
            return "masks/yh.jpg"
        