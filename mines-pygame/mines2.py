from sqare import Square
from game import Game
import pygame
import numpy as np
import random as rd
import time

SCREENSIZE = 905

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
                        while iter<5:
                            it = iter*10
                            game.sqrs[i][j].col = (c-it*2,c+it,c-it*2)
                            #time.sleep(0.001)
                            iter +=1
                            drawWin(win,game)
                    else:
                        game.sqrs[i][j].col = (100,255,100)

        drawWin(win,game)
        #win.blit(text, (450 - text.get_width()//2, 450))
        pygame.display.update()
        pygame.time.delay(3000)
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
                        while iter<5:
                            it = iter*10
                            game.sqrs[i][j].col = (c+it,c-it*2,c-it*2)
                            #time.sleep(0.001)
                            iter +=1
                            drawWin(win, game)
                    else:
                        game.sqrs[i][j].col = (255,100,100)
        

        drawWin(win,game)
        #win.blit(text, (450 - text.get_width()//2, 450))
        pygame.display.update()
        pygame.time.delay(3000)


def drawWin(win,game):
    win.fill((20,20,20))
    fin.draw(win,game)
    back.draw(win,game)
    score.draw(win,game)
    for i in range(0,game.GAMESIZE):
        for sqr in game.sqrs[i]:
            sqr.draw(win,game)
    pygame.display.update()


def main(GAMESIZE,BOMBCOUNT,TEXTSIZE,SQRSIZE):
    game = Game(GAMESIZE,BOMBCOUNT,TEXTSIZE,SQRSIZE)
    clock = pygame.time.Clock()
    run = True
    win.fill((20,20,20))
    print(game.field.sum())
    first = True
    change = True
    while run:
        clock.tick(40)
        back.text = "Back"
        fin.text = "Finish"
        score.text = "! " + str(game.BOMBCOUNT-game.tagged) 
        if change:
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
                    end(True,game,win)
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
                                change = True
                        else:
                            x = sqr.getX(game)
                            y = sqr.getY(game)
                            if sqr.click(pos) and but == 1 and not game.field[x][y] and not sqr.tagged:
                                ret = sqr.set(game)
                                change = True
                                if ret == 1:
                                    run = False
                                    end(True, game,win)
                                    del game
                                    return
                                elif ret == -1:
                                    end(False, game,win)
                                    run = False
                                    del game
                                    return
                            elif sqr.click(pos) and but == 3 and game.field[x][y] == 0:
                                sqr.tag(game)
                                change = True


def start():
    SQRSIZE = 200
    clock = pygame.time.Clock()
    ez = Square(350,100, (0,180,0),test)
    ez.text = "Einfach"
    med = Square(350,350, (255,127,80),test)
    med.text = "Medium"
    hard = Square(350,600, (180,0,0),test)
    hard.text = "Schwer"
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

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if ez.click(pos):
                    main(GAMESIZE = 9,BOMBCOUNT = 20,TEXTSIZE = 60,SQRSIZE = 95)
                elif med.click(pos):
                    main(GAMESIZE = 18,BOMBCOUNT = 80,TEXTSIZE = 60,SQRSIZE = 45)
                elif hard.click(pos):
                    main(GAMESIZE = 36,BOMBCOUNT = 320,TEXTSIZE = 30,SQRSIZE = 20)
              
start()