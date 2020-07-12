import sys
import pygame
from pygame.locals import *
from random import randint, choice
from time import sleep

pygame.init()
size = width, height = 800,500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("testing")
myfont = pygame.font.SysFont("monospace", 60)
WHITE = (118,238,198)

score = 0

symbols = ['x' , '-', '+']

def get_text(num):
    if num < 0:
        return '({})'.format(num)
    else:
        return '{}'.format(num)

def getexprtext():
    symbol = choice(symbols)
    number1 = randint(-7, 7)
    number2 = randint(-7, 7)
    n1text = get_text(number1)
    n2text = get_text(number2)
    return '{} {} {} = '.format(n1text, symbol, n2text)

while True:
    pygame.display.flip()
    for event in pygame.event.get():
        # I remove the timer just for my testing
        if event.type == pygame.QUIT: sys.exit()
        screen.fill(WHITE)
    screen.fill(WHITE)
    disclaimertext = myfont.render("Some disclaimer...", 1, (0,0,0))
    screen.blit(disclaimertext, (5, 480))

    #scoretext = myfont.render("Score {0}".format(score), 1, (0,0,0))
    expr = getexprtext()
    exprtext =  myfont.render(expr, 1, (0,0,0))
    screen.blit(exprtext, (200, 200))
    score += 1
    sleep(10)
