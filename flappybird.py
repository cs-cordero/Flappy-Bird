'''
===============================================================================
Creator: Christopher Sabater Cordero
Original: Nguyen Ha Dong
Date Started: 12/30/2015
File: Flappy Bird Clone
Notice: (c) Copyright 2015 by Christopher Sabater Cordero  All Rights Reserved.
===============================================================================
'''

import sys, os, random, pygame
from pygame.locals import *
from scripts.spritesheets import *
from scripts.constants import *
from scripts.classes import *
import scripts.sounds

pygame.init()
fps = pygame.time.Clock()

pygame.display.set_caption('Flappy Bird')
canvas = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
canvas.set_colorkey(COLORKEY)
artTime = random.randint(0,1)

def generateBackground():
  if artTime == 0: background_img = pygame.image.load(os.path.join('images','background_light.png')).convert()
  else: background_img = pygame.image.load(os.path.join('images','background_dark.png')).convert()
  background_size = background_img.get_size()
  background_img = pygame.transform.scale(background_img,(int(WINDOWHEIGHT*1.1*(float(background_size[0])/float(background_size[1]))),WINDOWHEIGHT))
  return background_img, background_img.get_size()

def loadPlayerSprites():
  rects = []
  for x in range(1,10): rects.append(pygame.Rect(17*(x-1),0,17,12))
  sheet = spritesheet(os.path.join('images','player_bird.png'))
  images = sheet.images_at(rects, COLORKEY)
  resized_images = []
  for image in images: resized_images.append(pygame.transform.scale(image,(BIRDSIZE*(image.get_size()[0]/image.get_size()[1]),BIRDSIZE)))
  return resized_images

def loadPipeSprites():
  rects = []
  for x in range(0,4): rects.append(pygame.Rect(26*x,0,26,160))
  sheet = spritesheet(os.path.join('images','game_pipes.png'))
  images = sheet.images_at(rects, COLORKEY)
  pipeImgs = []
  if artTime == 0:
    pipeImgs.append(pygame.transform.scale(images[2],(PIPEWIDTH,WINDOWHEIGHT)))
    pipeImgs.append(pygame.transform.scale(images[3],(PIPEWIDTH,WINDOWHEIGHT)))
  else:
    pipeImgs.append(pygame.transform.scale(images[0],(PIPEWIDTH,WINDOWHEIGHT)))
    pipeImgs.append(pygame.transform.scale(images[1],(PIPEWIDTH,WINDOWHEIGHT)))
  return pipeImgs

def GenerateText(text, posx, posy, size=72, font='Flappy-Bird', color=WHITE):
  fontObj = pygame.font.Font(os.path.join(os.path.dirname(__file__),'fonts',font + '.TTF'), size)
  textSurfaceObj = fontObj.render(text, True, color)
  textRectObj = textSurfaceObj.get_rect()
  textRectObj.center = (posx, posy)
  return textSurfaceObj, textRectObj

def drawAssets(background_img, background_size, pipes, pipeImgs, player, flappybird, points):
  gameZone = Rect(((WINDOWWIDTH/2)-(background_size[0]/2)),0,background_size[0],WINDOWHEIGHT)
  canvas.fill(BLACK)
  canvas.blit(background_img,gameZone.topleft)
  if len(pipes) > 0:
    for pipe in pipes:
      canvas.blit(pipeImgs[0],(pipe.opening.left, pipe.opening.bottom))
      canvas.blit(pipeImgs[1],(pipe.opening.left, pipe.opening.top - WINDOWHEIGHT))
  pygame.draw.rect(canvas, BLACK, ((0,0),gameZone.bottomleft))
  pygame.draw.rect(canvas, BLACK, (gameZone.topright,(WINDOWWIDTH,WINDOWHEIGHT)))
  scoreBoard = GenerateText(str(points), gameZone.centerx, ((100.0/720.0)*WINDOWHEIGHT))
  scoreBoardShadow = GenerateText(str(points), gameZone.centerx, ((100.0/720.0)*WINDOWHEIGHT), color=BLACK, size=96)
  scoreBoardShadow[1].center = scoreBoard[1].center
  canvas.blit(scoreBoardShadow[0], scoreBoardShadow[1])
  canvas.blit(scoreBoard[0], scoreBoard[1])
  canvas.blit(player,(flappybird.posx,flappybird.posy))

def main():
  while True:
    GameOver = False
    ResetGame = False
    elapsed_time = 0
    points = 0
    background_img, background_size = generateBackground()
    flappybird = bird(loadPlayerSprites(), frames=FPS/12)
    player = flappybird.image_list[0]
    pipeImgs = loadPipeSprites()
    pipes = []

    while ResetGame == False:
      drawAssets(background_img, background_size, pipes, pipeImgs, player, flappybird, points)

      for event in pygame.event.get():
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == K_SPACE):
          if GameOver == False:
            flappybird.rotate(flap=True)
            flappybird.fall(flap=True)
          elif GameOver == True and flappybird.posy == (WINDOWHEIGHT - BIRDSIZE):
            ResetGame = True
        if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and bool(event.mod & pygame.KMOD_ALT)) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
          pygame.quit()
          sys.exit()
        
      if GameOver == False:
        for pipe in pipes:
          pipe.next()
          checkDeath, points = pipe.checkCollision(flappybird, points)
          if checkDeath == "Killed": GameOver = True
          if pipe.opening.right < (WINDOWWIDTH/2)-(background_size[0]/2):
            pipes.remove(pipe)
        elapsed_time += fps.get_time()
        if elapsed_time > 2000:
          elapsed_time = 0
          pipes.append(gamePipe(pipeImgs, background_size))

      player = flappybird.next()
      # check for bottom collision
      if (flappybird.posy + BIRDSIZE) >= WINDOWHEIGHT:
        if flappybird.loop == True:
          sounds.channel2.play(sounds.sound_hit)
          sounds.channel2.queue(sounds.sound_die)
        flappybird.posy = (WINDOWHEIGHT - BIRDSIZE)
        flappybird.loop = False
        GameOver = True
      
      pygame.display.update()
      fps.tick(60)

if __name__ == '__main__':
  main()
