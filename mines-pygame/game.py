import numpy as np
import random as rd
from sqare import Square

class Game:
    def __init__(self,GAMESIZE,BOMBCOUNT,TEXTSIZE,SQRSIZE):
        self.field = np.zeros((GAMESIZE,GAMESIZE), dtype='int8')
        self.bombs = np.zeros((GAMESIZE,GAMESIZE), dtype='int8')
        self.adjBombs = np.zeros((GAMESIZE,GAMESIZE), dtype='int8')
        self.GAMESIZE = GAMESIZE
        self.BOMBCOUNT = BOMBCOUNT
        self.TEXTSIZE = TEXTSIZE
        self.SQRSIZE = SQRSIZE
        self.tagged = 0
        self.sqrs = []
        n = 1
        if GAMESIZE == 9:
            n = 100
        elif GAMESIZE == 18:
            n = 50
        elif GAMESIZE == 36:
            n = 25
        for i in range(0,GAMESIZE):
            self.sqrs.append([])
        for i in range(0,(n*GAMESIZE) - (n-1),n):
            for j in range(0,(n*GAMESIZE) - (n-1),n):
                self.sqrs[i//n].append(Square(i+5,j+5,i//n,j//n,(200,200,200),self))

    def finish(self):
        if not self.bombs.sum():
            self.generate(self.sqrs[0][0])
        for i in range(0,self.GAMESIZE):
            for j in range(0, self.GAMESIZE):
                if self.field[i][j] == 0 and self.bombs[i][j] == 0:
                    self.sqrs[i][j].set(self)

    def adj(self,bomb,x,y):
        ret = 0
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i in range(0,self.GAMESIZE) and j in range(0,self.GAMESIZE):
                    if bomb:
                        ret += self.bombs[i][j]
                    else:
                        ret += self.field[i][j]
        return ret

    def propagate(self,x,y):
        #print(f"propagate called on ({x},{y})")
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if (i,j) == (x,y) or i not in range(0,self.GAMESIZE) or j not in range(0,self.GAMESIZE):
                    continue
                if not self.field[i][j] and not self.bombs[i][j]:
                    self.sqrs[i][j].set(self)
                    if not self.adjBombs[i][j]:
                        #print(f"further propagating to ({i},{j})")
                        self.propagate(i,j)
        return
    
    
    def near(self,t2):
        return [(t2[0],t2[1]),(t2[0],t2[1]+1),(t2[0],t2[1]-1),(t2[0]+1,t2[1]),(t2[0]-1,t2[1]),(t2[0]+1,t2[1]+1),(t2[0]+1,t2[1]-1),(t2[0]-1,t2[1]+1),(t2[0]-1,t2[1]-1)]

    def generate(self,sqr):
        x = sqr.col
        y = sqr.row
        f_near = set(self.near((x,y)))
        while self.bombs.sum() < self.BOMBCOUNT:
            r = rd.randint(0,(self.GAMESIZE*self.GAMESIZE) - 1 )
            e = r//self.GAMESIZE
            r = r%self.GAMESIZE
            if self.bombs[e][r] or (e,r) in f_near or (self.adj(True,e,r) > 3):
                continue
            self.bombs[e][r] = 1
                
        for i in range(0,self.GAMESIZE):
            for j in range(0,self.GAMESIZE):
                self.adjBombs[i][j] = self.adj(True,i,j)

        self.sqrs[x][y].set(self)

    def won(self):
        return  self.field.sum() + self.bombs.sum() == self.GAMESIZE**2
