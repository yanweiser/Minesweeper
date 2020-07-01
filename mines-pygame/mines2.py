from sqare import Square
from game import Game
from highscore import Highscore
import pygame
import numpy as np
import random as rd
import time
from _thread import *
import os.path
import os

SCREENSIZE = 905
if os.path.exists("highscore.txt"):
    HS = "highscore.txt"
elif os.path.exists("mines-pygame/highscore.txt"):
    HS = "mines-pygame/highscore.txt"
else:
    f = open("highscore.txt", "w+")
    f.write("0,0,0")
    f.close
    HS = "highscore.txt"
hs = Highscore()
file = hs.readdata(HS)
hs.form(file)
print(hs.hs)
#hs.hs[1] = 40
#file = hs.writedata(HS)
#hs.writeHS(file)


pygame.init()
pygame.font.init()
win = pygame.display.set_mode((SCREENSIZE+400,SCREENSIZE))

test = Game(0,0,60,200)
back = Square(1000,100,(100,100,100),test)
fin = Square(1000,350, (100,100,100),test)
score = Square(1000,600,(150,80,80),test)




def end(x, game, win):
    if x:
        win.fill((255,255,255))
        s = "Gewonnen!! :)"
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render(s, 1, (255,69,0))

        for i in range(0,game.GAMESIZE):
            for j in range(0,game.GAMESIZE):
                if game.bombs[i][j]:
                    c = 200
                    iter = 0
                    if game.GAMESIZE == 9:
                        while iter<6:
                            it = iter*11
                            game.sqrs[i][j].col = (c-it*2,c+it,c-it*2)
                            iter +=1
                            drawPart(win,game,game.sqrs[i][j])
                    else:
                        game.sqrs[i][j].col = (100,255,100)
        drawWin(win,game)

    elif not x:
        win.fill((255,255,255))
        s = "Verloren :("
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render(s, 1, (255,69,0))

        for i in range(0,game.GAMESIZE):
            for j in range(0,game.GAMESIZE):
                if game.bombs[i][j]:
                    c = 200
                    iter = 0
                    if game.GAMESIZE == 9:
                        while iter<6:
                            it = iter*11
                            game.sqrs[i][j].col = (c+it,c-it*2,c-it*2)
                            iter +=1
                            drawPart(win,game,game.sqrs[i][j])
                    else:
                        game.sqrs[i][j].col = (255,100,100)
        drawWin(win,game)
       




def drawWin(win,game):
    print("full draw")
    win.fill((20,20,20))
    fin.draw(win,game)
    back.draw(win,game)
    score.draw(win,game)
    for i in range(0,game.GAMESIZE):
        for sqr in game.sqrs[i]:
            sqr.draw(win,game)
    pygame.display.update()

def drawPart(win, game, sqr):
    print("partial draw")
    score.draw(win, game)
    sqr.draw(win,game)
    pygame.display.update([pygame.Rect(sqr.x,sqr.y,sqr.size,sqr.size),pygame.Rect(score.x,score.y,score.size,score.size)])

def ctc(game):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                del game
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return


def main(GAMESIZE,BOMBCOUNT,TEXTSIZE,SQRSIZE):
    game = Game(GAMESIZE,BOMBCOUNT,TEXTSIZE,SQRSIZE)
    clock = pygame.time.Clock()
    run = True
    win.fill((20,20,20))
    first = True
    change = False
    update = (0,0)
    no = True
    sq = Square(0,0,(0,0,0),game)
    back.text = "Back"
    fin.text = "Finish"
    while run:
        clock.tick(60)
        score.text = "! " + str(game.BOMBCOUNT-game.tagged) 
        if no:
            drawWin(win,game)
            no = False
        if change:
            if sq.text != "" or (sq.text == "" and not game.field[sq.getX(game)][sq.getY(game)]):
                drawPart(win,game,sq)
            elif sq.text == "":
                drawWin(win,game)
        change = False
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                del game
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                but = event.button
                if but == 1 and back.click(pos):
                    run = False
                    del game
                    return
                if but == 1 and fin.click(pos):
                    game.finish()
                    drawWin(win,game)
                    id = start_new_thread(end,(True,game,win))
                    if game.GAMESIZE == 9:
                        ctc(game)
                    try:
                        id.exit()
                    except:
                        print("thread already finished")
                    pygame.time.delay(3000)
                    run = False
                    del game
                    return
                for i in range(0,game.GAMESIZE):
                    for sqr in game.sqrs[i]:
                        pos = pygame.mouse.get_pos()
                        if first:
                            if sqr.click(pos) and but == 1:
                                game.generate(sqr)
                                first = False
                                no = True
                        else:
                            x = sqr.getX(game)
                            y = sqr.getY(game)
                            if sqr.click(pos) and but == 1 and not game.field[x][y] and not sqr.tagged:
                                ret = sqr.set(game)
                                change = True
                                sq = sqr
                                if ret == 1:
                                    drawPart(win,game,sqr)
                                    run = False
                                    id = start_new_thread(end,(True, game,win))
                                    if game.GAMESIZE == 9:
                                        ctc(game)
                                    try:
                                        id.exit()
                                    except:
                                        print("thread already finished")
                                    run = False
                                    pygame.time.delay(3000)
                                    if GAMESIZE == 9:
                                        hs.hs[0] = 100
                                    elif GAMESIZE == 18:
                                        hs.hs[1] = 100
                                    else:
                                        hs.hs[2] = 100
                                    file = hs.writedata(HS)
                                    hs.writeHS(file)
                                    del game
                                    return
                                elif ret == -1:

                                    id = start_new_thread(end,(False, game,win))
                                    if game.GAMESIZE == 9:
                                        ctc(game)
                                    try:
                                        id.exit()
                                    except:
                                        print("thread already finished")
                                    run = False
                                    pygame.time.delay(3000)
                                    del game
                                    return
                            elif sqr.click(pos) and but == 3 and game.field[x][y] == 0:
                                sqr.tag(game)
                                change = True
                                sq = sqr

def setup():
    font1 = pygame.font.SysFont("comicsans", 70)
    font2 = pygame.font.SysFont("comicsans", 55)
    text1 = font1.render("highscores", 1, (0,0,0))
    text2 = font2.render(str(hs.hs[0]), 1, (0,0,0))
    text3 = font2.render(str(hs.hs[1]), 1, (0,0,0))
    text4 = font2.render(str(hs.hs[2]), 1, (0,0,0))
    win.fill((255,255,255))
    win.blit(text1, (700,50))
    win.blit(text2, (780, 200 - text2.get_height()/2))
    win.blit(text3, (780, 450 - text3.get_height()/2))
    win.blit(text4, (780, 700 - text4.get_height()/2))


def start():
    SQRSIZE = 200
    clock = pygame.time.Clock()
    ez = Square(350,100, (0,180,0),test)
    ez.text = "Einfach"
    med = Square(350,350, (255,127,80),test)
    med.text = "Medium"
    hard = Square(350,600, (180,0,0),test)
    hard.text = "Schwer"
    setup()
    pygame.display.update()
    while True:
        clock.tick(60)	
        win.fill((255,255,255))
        ez.draw(win,test)
        med.draw(win,test)
        hard.draw(win,test)
        pos = pygame.mouse.get_pos()

        if ez.click(pos):
            ez.col = (0,100,0)
            med.col = (255,127,80)
            hard.col = (180,0,0)
        elif med.click(pos):
            ez.col = (0,180,0)
            med.col = (180,80,50)
            hard.col = (180,0,0)
        elif hard.click(pos):
            ez.col = (0,180,0)
            med.col = (255,127,80)
            hard.col = (100,0,0)
        else:
            ez.col = (0,180,0)
            med.col = (255,127,80)
            hard.col = (180,0,0)

        pygame.display.update(pygame.Rect(100,0,500,900))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if ez.click(pos):
                    main(GAMESIZE = 9,BOMBCOUNT = 20,TEXTSIZE = 60,SQRSIZE = 95)
                    setup()
                    pygame.display.update()
                elif med.click(pos):
                    main(GAMESIZE = 18,BOMBCOUNT = 80,TEXTSIZE = 60,SQRSIZE = 45)
                    setup()
                    pygame.display.update()
                elif hard.click(pos):
                    main(GAMESIZE = 36,BOMBCOUNT = 320,TEXTSIZE = 30,SQRSIZE = 20)
                    setup()
                    pygame.display.update()
              
start()