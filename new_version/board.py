# in this file , we create a board class to hold the sprites

class Board:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.rows = [0] * height
    # we can add a fixed boundary image to make the image sensible, such as a circle, a man, etc.
    def add_boundary(self,boundary_sprite):
        for i, row in enumerate(boundary_sprite):
            if i < self.height:
                # print(row)
                self.rows[i] |= row # 直接填充白色边界，使得word无法放置
    def can_place(self,sprite,x,y,padding=2):
        # to avoid the word is so close to the other words 
        # we can add a padding here
        n = sprite[1]
        for i, row in enumerate(sprite[0]):
            # here we think the x,y is the top-left corner of the sprite
            yy = y + i
            padded_row = row
            for i in range(padding):
                padded_row |= (row << i)
                padded_row |= (row >> i)
            if yy < 0 or yy >= self.height:
                # print(f'height out of bound: {yy}')
                return False
            # print(f'{self.width}, {x}, {n}')
            if n + x > self.width or x < 0:
                # print(f'width out of bound: {yy}')
                return False
            # shifted = row << (self.width - x - n)
            shifted = padded_row << (self.width - x - n)
            # if self.rows[yy] & shifted != 0:
            #     # print(f'collision at row {yy}')
            #     return False
            for dy in range(-padding, padding + 1):
                check_y = yy + dy
                if 0 <= check_y < self.height:
                    if self.rows[check_y] & shifted != 0:
                        return False # 碰到任何邻近像素，即判定为无法放置
        return True
    
    def place(self,sprite,x,y):
        n = sprite[1]
        if self.can_place(sprite,x,y): 
            for i, row in enumerate(sprite[0]):
                yy = y + i
                shifted = row << (self.width - x - n)
                self.rows[yy] |= shifted
    def print_board(self):
        for row in self.rows:
            line = ''
            for i in range(self.width):
                if row & (1 << (self.width - 1 - i)):
                    line += '#'
                else:
                    line += '.'
            print(line)
    
        