import numpy as np
import random as rd
from sqare import Square

class Game:
    def __init__(self,GAMESIZE,BOMBCOUNT,TEXTSIZE,SQRSIZE):
        self.field = np.zeros((GAMESIZE,GAMESIZE), dtype=int)
        self.bombs = np.zeros((GAMESIZE,GAMESIZE), dtype=int)
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
                self.sqrs[i//n].append(Square(i+5,j+5,(200,200,200),self))

    def finish(self):
        for i in range(0,self.GAMESIZE):
            for j in range(0, self.GAMESIZE):
                if self.field[i][j] == 0 and self.bombs[i][j] == 0:
                    self.sqrs[i][j].set(self)

    def adj(self,ar,x,y):
        ret = 0
        for i in range(x-1,x+2):
            for j in range(y-1,y+2):
                if i in range(0,self.GAMESIZE) and j in range(0,self.GAMESIZE):
                    if ar:
                        ret += self.bombs[i][j]
                    else:
                        ret += self.field[i][j]
        return ret

    def propagate(self,x,y):
        for j in range(x-1,x+2):
            for i in range(y-1,y+2):
                if (i,j) == (x,y) or i not in range(0,self.GAMESIZE) or j not in range(0,self.GAMESIZE):
                    continue
                if not self.field[i][j] and not self.bombs[i][j]:
                    self.sqrs[i][j].set(self)
                    if not self.adj(True, i, j):
                        self.propagate(j,i)
        return

    def generate(self,sqr):
        x = sqr.getX(self)
        y = sqr.getY(self)
        while self.bombs.sum() < self.BOMBCOUNT:
            r = rd.randint(0,(self.GAMESIZE*self.GAMESIZE) - 1 )
            e = 0
            while r > self.GAMESIZE - 1:
                e+=1
                r-=self.GAMESIZE
            self.bombs[e][r] = 1
            if self.adj(True, x,y) or self.adj(True,e,r) > 3:
                self.bombs[e][r] = 0

        print(self.bombs)
        self.sqrs[x][y].set(self)
        self.propagate(y,x)


    def won(self):
        if self.field.sum() + self.bombs.sum() == self.GAMESIZE**2:
            return True
        else:
            return False
