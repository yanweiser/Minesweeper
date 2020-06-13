import os.path
import os
import numpy as np

class Highscore:
    def __init__(self):
        self.hs = []

    def readdata(self, file):
        f = open(file, "r")
        return f

    def writedata(self, file):
        f = open(file,"w")
        return f

    def form(self, file):
        dl = file.read()
        x = []
        args = dl.split(",", 3)
        print(args)
        for a in args:
            print(a)
            a = a.replace(" ", "")
            a = a.replace("\n", "")
            a = a.replace(",", "")
            if a == "":
                continue
            a = int(a)
            x.append(a)
        while len(x) != 3:
            x.append(0)
        self.hs = x
        file.close()

    def writeHS(self, file):
        file.write(self.makeStr())
        file.close()

    def makeStr(self):
        s = ""
        for h in self.hs:
            print(s)
            s = s + str(h) + ","
        return s



