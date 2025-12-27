# this file try to detect if the new word collides with the boundary and other words(placed)
from utils.style import get_font


def collide(x, y, font, word,placed_words, canvas_width, canvas_height,padding=2):
    # now we just loop to check
    # first check if the word is within the canvas boundary
    # font is not the precise size of the word,we should get the precise size 
    from PIL import ImageFont, ImageDraw, Image
    temp_image = Image.new('RGB', (1, 1),'white')
    draw = ImageDraw.Draw(temp_image)

    
    bbox = draw.textbbox((0,0), word,font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    # use precise bounding box to check boundary collision
    if x - padding < 0 or y - padding < 0:
        return True
    if x + w + padding > canvas_width or y + h + padding > canvas_height:
        return True
    
    
    # then check if it collides with other placed words
    for px, py, pfont_size,pword in placed_words:
        try:
            pfont = get_font("/Library/Fonts/Arial Unicode.ttf", pfont_size)
        except:
            pfont = ImageFont.load_default()
        pbbox = draw.textbbox((px,py),pword,font=pfont)
        pw = pbbox[2] - pbbox[0]
        ph = pbbox[3] - pbbox[1]

        # check if the bounding boxes overlap
        if x >= px + pw + padding or x + w + padding <= px:
            continue
        if y >= py + ph + padding or y + h + padding <= py:
            continue
        # otherwise, they overlap
        return True

    return False