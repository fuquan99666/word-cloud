# this file try to detect if the new word collides with the boundary and other words(placed)
from style import get_font

# now we should think about the direction of the word

def collide(x, y, font, word,placed_words, canvas_width, canvas_height,dir,padding=2):
    # now we just loop to check
    # first check if the word is within the canvas boundary
    # font is not the precise size of the word,we should get the precise size 

    from PIL import ImageDraw, ImageFont

    # bbox = draw.textbbox((0,0), word,font=font)
    bbox = font.getbbox(word)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    if dir in [90,-90]:
        w, h = h, w  # swap width and height for vertical text

    # use precise bounding box to check boundary collision
    if x - padding < 0 or y - padding < 0:
        return True
    if x + w + padding > canvas_width or y + h + padding > canvas_height:
        return True
    
    
    # then check if it collides with other placed words
    for px, py, pfont_size,pword,pdir in placed_words:
        try:
            pfont = get_font("/Library/Fonts/Arial Unicode.ttf", pfont_size)
        except:
            pfont = ImageFont.load_default()
        
        pbbox = pfont.getbbox(pword)
        pw = pbbox[2] - pbbox[0]
        ph = pbbox[3] - pbbox[1]

        if pdir in [90,-90]:
            pw, ph = ph, pw  # swap width and height for vertical text

        # check if the bounding boxes overlap
        if x >= px + pw + padding or x + w + padding <= px:
            continue
        if y >= py + ph + padding or y + h + padding <= py:
            continue
        # otherwise, they overlap
        return True

    return False