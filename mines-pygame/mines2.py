from sqare import Square
from game import Game
import pygame
import numpy as np
from _thread import *
import os


SCREENSIZE = 905

pygame.init()
pygame.font.init()
win = pygame.display.set_mode((SCREENSIZE+400,SCREENSIZE))
test = Game(0,0,60,200)
back = Square(1000,100,0,0,(100,100,100),test)
fin = Square(1000,350, 0,0,(100,100,100),test)
score = Square(1000,600,0,0,(150,80,80),test)
ext = Square(1255,0,0,0,(100,100,100),Game(0,0,20,50))
ext.text = "exit"


def end(x, game, win):
    if x:
        win.fill((255,255,255))
        for i in range(0,game.GAMESIZE):
            for j in range(0,game.GAMESIZE):
                if game.bombs[i][j]:
                    game.sqrs[i][j].color = (100,255,100)
                    drawPart(win, game, game.sqrs[i][j])


    elif not x:
        win.fill((255,255,255))
        for i in range(0,game.GAMESIZE):
            for j in range(0,game.GAMESIZE):
                if game.bombs[i][j]:
                    game.sqrs[i][j].color = (255,100,100)
                    drawPart(win, game, game.sqrs[i][j])
       

def drawWin(win,game):
    win.fill((20,20,20))
    fin.draw(win,game)
    back.draw(win,game)
    score.draw(win,game)
    ext.draw(win,game)
    for i in range(0,game.GAMESIZE):
        for sqr in game.sqrs[i]:
            sqr.draw(win,game)
    pygame.display.update()

    
def drawPart(win, game, sqr):
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
    sq = None
    back.text = "Back"
    fin.text = "Finish"
    score.text = "! " + str(game.BOMBCOUNT-game.tagged)
    # print("game start")
    while run:
        #print("in mainloop")
        clock.tick(60)
        if no:
            drawWin(win,game)
            no = False
        if change:
            if sq.text != "" or (sq.text == "" and not game.field[sq.col][sq.row]):
                drawPart(win,game,sq)
            elif sq.text == "":
                drawWin(win,game)
            change = False
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                but = event.button
                if but == 1 and ext.click(pos):
                    run = False
                    pygame.quit()
                    exit()
                if but == 1 and back.click(pos):
                    run = False
                    return
                if but == 1 and fin.click(pos):
                    game.finish()
                    drawWin(win,game)
                    id = start_new_thread(end,(True,game,win))
                    try:
                        id.exit()
                    except:
                        
                        pass
                    ctc(game)
                    run = False
                    return
                for i in range(GAMESIZE):
                    for sqr in game.sqrs[i]:
                        pos = pygame.mouse.get_pos()
                        if first:
                            if sqr.click(pos) and but == 1:
                                print("first run --> generate")
                                game.generate(sqr)
                                first = False
                                no = True
                        else:
                            x = sqr.col
                            y = sqr.row
                            if sqr.click(pos) and but == 1 and not game.field[x][y] and not sqr.tagged:
                                ret = sqr.set(game)
                                change = True
                                sq = sqr
                                if ret == 1: # win
                                    drawPart(win,game,sqr)
                                    run = False
                                    id = start_new_thread(end,(True, game,win))
                                    try:
                                        id.exit()
                                    except:
                                        pass
                                    ctc(game)
                                    return
                                elif ret == -1: # lost
                                    id = start_new_thread(end,(False, game,win))
                                    ctc(game)
                                    try:
                                        id.exit()
                                    except:
                                        pass
                                    run = False
                                    return
                            elif sqr.click(pos) and but == 3 and game.field[x][y] == 0:
                                sqr.tag(game)
                                change = True
                                score.text = "! " + str(game.BOMBCOUNT-game.tagged)
                                sq = sqr




def start():
    SQRSIZE = 200
    clock = pygame.time.Clock()
    ex = Square(1255,0,0,0,(100,100,100),Game(0,0,20,50))
    ex.text = 'exit'
    ez = Square(350,100,0,0, (0,180,0),test)
    ez.text = "Einfach"
    med = Square(350,350,0,0, (255,127,80),test)
    med.text = "Medium"
    hard = Square(350,600,0,0, (180,0,0),test)
    hard.text = "Schwer"
    win.fill((255,255,255))
    pygame.display.update()
    while True:
        clock.tick(60)	
        ez.draw(win,test)
        med.draw(win,test)
        hard.draw(win,test)
        ex.draw(win,test)
        pos = pygame.mouse.get_pos()
        if ez.click(pos):
            ez.color = (0,100,0)
            med.color = (255,127,80)
            hard.color = (180,0,0)
        elif med.click(pos):
            ez.color = (0,180,0)
            med.color = (180,80,50)
            hard.color = (180,0,0)
        elif hard.click(pos):
            ez.color = (0,180,0)
            med.color = (255,127,80)
            hard.color = (100,0,0)
        else:
            ez.color = (0,180,0)
            med.color = (255,127,80)
            hard.color = (180,0,0)

        pygame.display.update([pygame.Rect(100,0,500,900),pygame.Rect(1255,0,50,50)])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if ez.click(pos):
                    main(GAMESIZE = 9,BOMBCOUNT = 20,TEXTSIZE = 60,SQRSIZE = 95)
                    win.fill((255,255,255))
                    pygame.display.update()
                elif med.click(pos):
                    main(GAMESIZE = 18,BOMBCOUNT = 80,TEXTSIZE = 45,SQRSIZE = 45)
                    win.fill((255,255,255))
                    pygame.display.update()
                elif hard.click(pos):
                    main(GAMESIZE = 36,BOMBCOUNT = 320,TEXTSIZE = 25,SQRSIZE = 20)
                    win.fill((255,255,255))
                    pygame.display.update()
                elif ex.click(pos):
                    pygame.quit()
                    exit()
        
start()
