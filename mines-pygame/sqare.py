import numpy as np
import random as rd
import pygame

class Square:
    def __init__(self,x,y,color,game):
        self.size = game.SQRSIZE
        self.x = x
        self.y = y
        self.col = color
        self.text = ""
        self.tagged = False

    def getX(self,game):
        for i in range(0,game.GAMESIZE):
            for j in range(0,game.GAMESIZE):
                if game.sqrs[i][j] == self:
                    return i

    def getY(self,game):
        for i in range(0,game.GAMESIZE):
            for j in range(0,game.GAMESIZE):
                if game.sqrs[i][j] == self:
                    return j


    def draw(self, win, game):
        pygame.draw.rect(win, self.col, (self.x, self.y, self.size, self.size))
        font = pygame.font.SysFont("comicsans", game.TEXTSIZE)
        text = font.render(self.text, 1, (0,0,0))
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
        x = self.getX(game)
        y = self.getY(game)
        if game.bombs[x][y]:
            return -1
        game.field[x][y] = 1
        nu = game.adj(True, x, y)
        if nu:
            self.text = str(nu)
        else:
            game.propagate(y,x)
        self.col = (100,100,255)
        if game.won():
            return 1
        return 0



    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.size and self.y <= y1 <= self.y + self.size:
            return True
        else:
            return False