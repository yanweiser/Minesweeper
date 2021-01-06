import os.path
import os
import numpy as np

class Highscore:
    def __init__(self):
        self.hs = []
        if os.path.exists('highscore.txt'):
            self.file = 'highscore.txt'
        elif os.path.exists('mines-pygame/highscore.txt'):
            self.file = 'mines-pygame/highscore.txt'
        else:
            file = open('highscore.txt','w+')
            file.write('0,0,0')
            file.close()
            self.file = 'highscore.txt'

    def form(self, file):
        file = open(self.file, 'r')
        dl = file.read()
        x = []
        args = dl.split(",")
        for a in args:
            a = int(a.strip())
            x.append(a)
        self.hs = x
        file.close()

    def writeHS(self):
        file = open(self.file, 'w')
        file.write(self.makeStr())
        file.close()

    def makeStr(self):
        s = ""
        for h in self.hs:
            s = s + str(h) + ","
        return s[:-1]
