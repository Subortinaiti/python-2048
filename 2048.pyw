import pygame as pg
import random
import math
import os
pg.init()

tilesize = 100
bordersize = 10
boardsize = (4,4)
starting_cells = 2 
clockspeed = 100

colors = [
    (255, 255, 240),  # White
    (255, 255, 230),  # Very Light Yellow
    (255, 255, 204),  # Light Yellow
    (255, 255, 179),  # Light Yellow
    (255, 255, 153),  # Light Yellow
    (255, 229, 102),  # Dark Yellow
    (255, 204, 51),   # Dark Yellow
    (255, 179, 25),   # Light Orange
    (255, 153, 12),   # Orange
    (230, 115, 0),    # Light Red
    (153, 0, 51)      # Dark Purple
]

background_clr = (200,200,200)

displaysize = (bordersize+boardsize[0]*(tilesize+bordersize),
               bordersize+boardsize[1]*(tilesize+bordersize))

display = pg.display.set_mode(displaysize)
pg.display.set_caption("2048")
clock = pg.time.Clock()

class board_class:
    def __init__(self,size):
        self.w,self.h = size
        self.tiles = [[None for i in range(self.w)] for i in range(self.h)]

        for i in range(starting_cells):
            self.generate_cell()



    def generate_cell(self):
        while True:
            row,col = random.randint(0,self.h-1),random.randint(0,self.w-1)
            if not self.tiles[row][col]:
                if random.random() >= 0.2:
                    value = 2
                else:
                    value = 4
                self.tiles[row][col] = tile_class(value)
                print("new cell generated at",row,col)
                return



    def draw_self(self):
        for row in range(self.h):
            for cell in range(self.w):
                if self.tiles[row][cell]:
                    self.tiles[row][cell].draw_self(cell,row)



    def move_down(self):
        global moved
        for i in range(boardsize[1]):
            for col in range(self.w):
                for row in range(self.h-1,-1,-1):
                    if row == self.h-1:
                        continue
                    curow = row+1
                    while True:
                        if curow == self.h:
                            break
                        if not self.tiles[row][col]:
                            break
                        if self.tiles[curow][col]:
                            break
                        
                       
                        self.tiles[curow][col] = self.tiles[curow-1][col]
                        self.tiles[curow-1][col] = None
                        curow += 1
                        moved = True

    def move_up(self):
        global moved
        for i in range(boardsize[1]):
            for col in range(self.w):
                for row in range(1, self.h):
                    if row == 0:
                        continue
                    curow = row - 1
                    while True:
                        if curow == -1:
                            break
                        if not self.tiles[row][col]:
                            break
                        if self.tiles[curow][col]:
                            break
                           
                        self.tiles[curow][col] = self.tiles[curow+1][col]
                        self.tiles[curow+1][col] = None
                        curow -= 1
                        moved = True

    def move_right(self):
        global moved
        for i in range(boardsize[1]):
            for row in range(self.h):
                for col in range(self.w - 1, -1, -1):
                    if col == self.w - 1:
                        continue
                    cucol = col + 1
                    while True:
                        if cucol == self.w:
                            break
                        if not self.tiles[row][col]:
                            break
                        if self.tiles[row][cucol]:
                            break
                            
                        self.tiles[row][cucol] = self.tiles[row][cucol - 1]
                        self.tiles[row][cucol - 1] = None
                        cucol += 1
                        moved = True

    def move_left(self):
        global moved
        for i in range(boardsize[1]):
            for row in range(self.h):
                for col in range(1, self.w):
                    if col == 0:
                        continue
                    cucol = col - 1
                    while True:
                        if cucol == -1:
                            break
                        if not self.tiles[row][col]:
                            break
                        if self.tiles[row][cucol]:
                            break
                            
                        self.tiles[row][cucol] = self.tiles[row][cucol + 1]
                        self.tiles[row][cucol + 1] = None
                        cucol -= 1
                        moved = True



    def merge_down(self):
            for col in range(self.w):
                for row in range(self.h-1,-1,-1):
                    if not self.tiles[row][col]:
                        continue
                    selfvalue = self.tiles[row][col].value
                    if self.tiles[row-1][col] and selfvalue == self.tiles[row-1][col].value:
                        self.tiles[row-1][col] = None
                        self.tiles[row][col].increase_value()

    def merge_up(self):
        for col in range(self.w):
            for row in range(self.h):
                if not self.tiles[row][col]:
                    continue
                self_value = self.tiles[row][col].value
                if row < self.h - 1 and self.tiles[row + 1][col] and self_value == self.tiles[row + 1][col].value:
                    self.tiles[row + 1][col] = None
                    self.tiles[row][col].increase_value()

    def merge_left(self):
        for row in range(self.h):
            for col in range(self.w):
                if not self.tiles[row][col]:
                    continue
                self_value = self.tiles[row][col].value
                if col > 0 and self.tiles[row][col - 1] and self_value == self.tiles[row][col - 1].value:
                    self.tiles[row][col - 1] = None
                    self.tiles[row][col].increase_value()

    def merge_right(self):
        for row in range(self.h):
            for col in range(self.w - 1, -1, -1):
                if not self.tiles[row][col]:
                    continue
                self_value = self.tiles[row][col].value
                if col < self.w - 1 and self.tiles[row][col + 1] and self_value == self.tiles[row][col + 1].value:
                    self.tiles[row][col + 1] = None
                    self.tiles[row][col].increase_value()






class tile_class:
    def __init__(self,value):
        self.value = value
        self.color = calculate_color(value) 
        self.text = self.calculate_text()

    def draw_self(self,x,y):
        xv,yv = shift_coords(x,y)
        pg.draw.rect(display,self.color,(xv,yv,tilesize,tilesize))
        
        text_rect = self.text.get_rect(center=(xv + tilesize / 2, yv + tilesize / 2))
        display.blit(self.text, text_rect)

    def calculate_text(self):
        # Calculate an appropriate font size to fit within the cell
        fontsize = 1
        font = pg.font.Font(None, fontsize)
        text = str(self.value)
        text_width, text_height = font.size(text)
        while text_width < tilesize and text_height < tilesize:
            fontsize += 1
            font = pg.font.Font(None, fontsize)
            text_width, text_height = font.size(text)
        # Use the last valid fontsize
        return font.render(text, True, (0, 0, 0))


    def increase_value(self):
        self.value *= 2
        self.color = calculate_color(self.value)
        self.text = self.calculate_text()        
        

    


def calculate_color(value):
    return colors[int(math.log(value,2)-1)]

def shift_coords(x,y):
    x2 = bordersize + x*(tilesize+bordersize)
    y2 = bordersize + y*(tilesize+bordersize)
    return x2,y2

def logic_calls():
    global dead
    if moved:
        full = True

        for col in range(board.w):
            if not full:
                break
            for row in range(board.h):
                if not board.tiles[row][col]:
                    full = False
                    break

        if not full:
            board.generate_cell()
        else:
            dead = 2

    
    #clock.tick(clockspeed)

def graphic_calls():
    display.fill(background_clr)
    board.draw_self()
    
    pg.display.flip()

def main():
    global board,dead,moved,cache
    board = board_class(boardsize)


    dead = 0
    while not dead:
        moved = False
        cache = list(board.tiles)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                dead = 1
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    dead = 1
                if not moved:
                    if event.key == pg.K_DOWN or event.key == pg.K_s:
                        board.move_down()
                        board.merge_down()
                        board.move_down()

                    if event.key == pg.K_UP or event.key == pg.K_w:
                        board.move_up()
                        board.merge_up()
                        board.move_up()


                    if event.key == pg.K_RIGHT or event.key == pg.K_d:
                        board.move_right()
                        board.merge_right()
                        board.move_right()


                    if event.key == pg.K_LEFT or event.key == pg.K_a:
                        board.move_left()
                        board.merge_left()
                        board.move_left()




        logic_calls()
        graphic_calls()

main()
pg.quit()
quit()
