import numpy as np
import pygame

class Square:
    def __init__(self,x,y,col,row,color,game):
        self.size = game.SQRSIZE
        self.x = x
        self.y = y
        self.color = color
        self.text = ""
        self.tagged = False
        self.row = row
        self.col = col
        self.font = pygame.font.SysFont("comicsans", game.TEXTSIZE)
        

    def draw(self, win, game):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size)
        text = self.font.render(self.text, 1, (0,0,0))
        win.blit(text, (self.x + round(self.size/2) - round(text.get_width()/2), self.y + round(self.size/2) - round(text.get_height()/2)))


    def tag(self,game):
        if self.tagged:
            self.tagged = False
            self.text = ""
            game.tagged -= 1
        else:
            self.tagged = True
            self.text = "!"
            game.tagged += 1

                         
    def set(self,game):
        x = self.col
        y = self.row
        if game.bombs[x][y]:
            return -1
        game.field[x][y] = 1
        nu = game.adjBombs[x][y]
        if nu:
            self.text = str(nu)
        else:
            game.propagate(y,x)
        self.col = (100,100,255)
        if game.won():
            return 1
        return 0


    def click(self, pos):
        if self.x <= pos[0] <= self.x + self.size and self.y <= pos[1] <= self.y + self.size:
            return True
        else:
            return False
