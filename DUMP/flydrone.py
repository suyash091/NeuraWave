import pygame
from pygame import *
from random import *
import random
import time
import os
import sys
from pygame.locals import *


black = (0,0,0)
white =(255,255,255)

pygame.init()

surfaceWidth = 800
surfaceHeight = 500
imageHeight = 43
imageWidth = 100


surface = pygame.display.set_mode((surfaceWidth,surfaceHeight))
pygame.display.set_caption('helecopter')
clock = pygame.time.Clock()
img = pygame.image.load('helicopter.png')

def makeTextObjs(text , font):
    textSurface = font.render(text, True , white )
    return textSurface , textSurface.get_rect()


def blocks (x_block , y_block , block_width , block_height , gap):
    pygame.draw.rect(surface , white ,[x_block,y_block,block_width,block_height])
    pygame.draw.rect(surface , white ,[x_block,y_block+block_height+gap,block_width,surfaceHeight])


#define replay or
def replay_or_quit():
     for event in pygame.event.get([pygame.KEYDOWN , pygame.KEYUP , pygame.QUIT]):
         if event.type == pygame.QUIT:
             pygame.quit()
             quit()

         elif event.type == pygame.KEYDOWN:
             continue

         return event.key
     return None


def gameOver():
    msgSurface('Loser!')

def msgSurface(text):
    smallText = pygame.font.Font('freesansbold.ttf',20)
    largeText = pygame.font.Font('freesansbold.ttf',150)

    titleTextSurf , titleTextRect = makeTextObjs(text, largeText)
    titleTextRect.center = surfaceWidth / 2 , surfaceHeight / 2
    surface.blit(titleTextSurf , titleTextRect)

    typTextSurf , typTextRect = makeTextObjs('Press any key to continue', smallText)
    typTextRect.center = surfaceWidth / 2 , ((surfaceHeight / 2) + 100)
    surface.blit(typTextSurf , typTextRect)

    pygame.display.update()

    time.sleep(1)

    while replay_or_quit() == None:
        clock.tick()

    main()

def Command_drone(text):
    smallText = pygame.font.Font('freesansbold.ttf',20)
    largeText = pygame.font.Font('freesansbold.ttf',60)

    titleTextSurf , titleTextRect = makeTextObjs(text, largeText)
    titleTextRect.center = surfaceWidth / 2 , surfaceHeight*0.20 / 2
    surface.blit(titleTextSurf , titleTextRect)
    pygame.display.update()
    time.sleep(0.1)

#put image to the console

def helicopter (x,y,image):
    surface.blit(img , (x,y))

flag_message = False

def main():
    x = 260
    y = 500
    y_move = 0
    x_block = surfaceWidth
    y_block = 0
    block_width =0
    block_height = randint(0, (surfaceHeight/2))
    gap = imageHeight * 3
    block_move = 3
    global flag_message

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    #actually it means UP
                    y_move = -50

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    #actually it means UP
                    y_move = 25
        if y<280:
            Command_drone("Drone Command: Up")

        y+=y_move
        print(y)
        if y>300:
            y=300
        elif y<0:
            y=0


        surface.fill(black)
        helicopter(x,y,img)
        blocks(x_block , y_block , block_width ,block_height , gap)
        x_block -= block_move

        pygame.display.update()
        clock.tick(100)

main()
pygame.quit()
quit()