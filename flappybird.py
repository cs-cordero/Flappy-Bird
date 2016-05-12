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
from math import ceil
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

def scaletowidth(scalar):  return (scalar/1280.0)*WINDOWWIDTH
def scaletoheight(scalar): return (scalar/720.0)*WINDOWHEIGHT

def loadBackgroundSprites():
  if artTime == 0: bg_img = pygame.image.load(os.path.join('images','background_light.png')).convert()
  else: bg_img = pygame.image.load(os.path.join('images','background_dark.png')).convert()
  bg_img = pygame.transform.scale(bg_img,(int(WINDOWHEIGHT*1.1*(float(bg_img.get_size()[0])/float(bg_img.get_size()[1]))),WINDOWHEIGHT))

  ground_img = pygame.image.load(os.path.join('images','background_ground.png')).convert()
  ground_img = pygame.transform.scale(ground_img,(int(ceil(bg_img.get_size()[0]/PIPESPEED)*PIPESPEED),int(scaletoheight(128.0))))

  title_img = pygame.image.load(os.path.join('images','titlescreen.png')).convert()
  title_img = pygame.transform.scale(title_img,(int(scaletowidth(222.5)), int(scaletoheight(75.0))))
  title_img.set_colorkey(COLORKEY)

  scorebox_img = pygame.image.load(os.path.join('images','game_scorebox.png')).convert()
  scorebox_img = pygame.transform.scale(scorebox_img,(int(scaletowidth(250.0)), int(scaletoheight(100.0))))
  scorebox_img.set_colorkey(COLORKEY)

  new_img = pygame.image.load(os.path.join('images','game_new.png')).convert()
  new_img = pygame.transform.scale(new_img,(int(scaletowidth(42.0)), int(scaletoheight(16.0))))
  new_img.set_colorkey(COLORKEY)

  return bg_img, ground_img, title_img, scorebox_img, new_img

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

def displayText(text, posx, posy, size=int(scaletoheight(72.0)), font='Flappy-Bird', color=WHITE):
  fontObj = pygame.font.Font(os.path.join('..','fonts',font + '.TTF'), size)
  textSurfaceObj = fontObj.render(text, True, color)
  textRectObj = textSurfaceObj.get_rect()
  textRectObj.center = (posx, posy)
  return textSurfaceObj, textRectObj

def drawAssets(bg_gameZone, bg_titleScreen, bg_img, bg_grounds, bg_gamePipes, flappyBird, gamePoints, finalScore, suppressScore=False):
  canvas.fill(BLACK)
  canvas.blit(bg_img,bg_gameZone.topleft)
  if len(bg_gamePipes) > 0:
    for pipe in bg_gamePipes:
      canvas.blit(pipe.images[0],(pipe.opening.left, pipe.opening.bottom))
      canvas.blit(pipe.images[1],(pipe.opening.left, pipe.opening.top - WINDOWHEIGHT))
  for ground in bg_grounds: canvas.blit(ground.img,ground.rect.topleft)
  canvas.blit(bg_titleScreen.img,(bg_titleScreen.rect.topleft))
  
  scoreBoardWhite = displayText(str(gamePoints), bg_gameZone.centerx, scaletoheight(100.0), color=WHITE)
  scoreBoardBlack = displayText(str(gamePoints), bg_gameZone.centerx, scaletoheight(100.0), color=BLACK)
  scoreBoardBlack[1].right += scaletowidth(3)
  scoreBoardBlack[1].top += scaletoheight(3)
  if bg_titleScreen.rect.right < bg_gameZone.left and not suppressScore:
    canvas.blit(scoreBoardBlack[0], scoreBoardBlack[1])
    canvas.blit(scoreBoardWhite[0], scoreBoardWhite[1])
  
  canvas.blit(flappyBird.img,(flappyBird.posx,flappyBird.posy))
  canvas.blit(finalScore.img,finalScore.rect.topleft)

  pygame.draw.rect(canvas, BLACK, ((0,0),bg_gameZone.bottomleft))
  pygame.draw.rect(canvas, BLACK, (bg_gameZone.topright,(WINDOWWIDTH,WINDOWHEIGHT)))


def main():
  highScore = 0
  while True:
    TitleScreen = True
    GameOver = False
    ResetGame = False
    gamePoints = 0
    bg_img, ground_img, bg_title, scorebox_img, new_img = loadBackgroundSprites()
    bg_gameZone = Rect(((WINDOWWIDTH/2)-(bg_img.get_size()[0]/2)),0,bg_img.get_size()[0],WINDOWHEIGHT)
    bg_titleScreen = titleScreen(bg_title,bg_gameZone)
    flappyBird = bird(loadPlayerSprites(), frames=FPS/12)
    finalScore = finalScoreBox(scorebox_img, new_img, bg_gameZone)
    pipeImgs = loadPipeSprites()
    bg_gamePipes = []
    bg_grounds = []
    bg_grounds.append(gameGround(ground_img,bg_gameZone.left))
    bg_grounds.append(gameGround(ground_img,bg_gameZone.right))

    # Hover Title Screen
    while TitleScreen == True:
      drawAssets(bg_gameZone, bg_titleScreen, bg_img, bg_grounds, bg_gamePipes, flappyBird, gamePoints, finalScore)
      flappyBird.hover()
      for ground in bg_grounds: ground.next(bg_gameZone)
      for event in pygame.event.get():
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == K_SPACE):
          TitleScreen = False
          flappyBird.rotate(flap=True)
          flappyBird.fall(flap=True)
        if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and bool(event.mod & pygame.KMOD_ALT)) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
          pygame.quit()
          sys.exit()
      pygame.display.update()
      fps.tick(60)

    # Title Screen Wipe Animation
    sounds.channel3.play(sounds.sound_swoosh)
    while bg_titleScreen.rect.right > bg_gameZone.left:
      drawAssets(bg_gameZone, bg_titleScreen, bg_img, bg_grounds, bg_gamePipes, flappyBird, gamePoints, finalScore)
      bg_titleScreen.next(bg_gameZone)
      for ground in bg_grounds: ground.next(bg_gameZone)
      flappyBird.next()
      pygame.display.update()
      fps.tick(60)
    
    # Actual Game
    elapsed_time = 0
    while GameOver == False:
      drawAssets(bg_gameZone, bg_titleScreen, bg_img, bg_grounds, bg_gamePipes, flappyBird, gamePoints, finalScore)

      for event in pygame.event.get():
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == K_SPACE):
          flappyBird.rotate(flap=True)
          flappyBird.fall(flap=True)
        if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and bool(event.mod & pygame.KMOD_ALT)) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
          pygame.quit()
          sys.exit()
        
      flappyBird.next()
      for pipe in bg_gamePipes:
        pipe.next()
        checkDeath, gamePoints = pipe.checkCollision(flappyBird, gamePoints)
        if checkDeath == "Killed": GameOver = True
        if pipe.opening.right < (WINDOWWIDTH/2)-(bg_img.get_size()[0]/2):
          bg_gamePipes.remove(pipe)
      for ground in bg_grounds: ground.next(bg_gameZone)
      elapsed_time += fps.get_time()
      if elapsed_time > 2000:
        elapsed_time = 0
        bg_gamePipes.append(gamePipe(pipeImgs, bg_img.get_size(),ground_img.get_size()[1]))

      # check for bottom collision
      if (flappyBird.posy + BIRDSIZE) >= WINDOWHEIGHT - ground_img.get_size()[1]:
        if flappyBird.loop == True:
          sounds.channel2.play(sounds.sound_hit)
          sounds.channel2.queue(sounds.sound_die)
        flappyBird.posy = (WINDOWHEIGHT - BIRDSIZE - ground_img.get_size()[1])
        flappyBird.loop = False
        GameOver = True
      
      pygame.display.update()
      fps.tick(60)

    # Show High Score
    if gamePoints > highScore:
      highScore = max(highScore, gamePoints)
      finalScore.update(gamePoints, highScore, newScore=True)
    else: finalScore.update(gamePoints, highScore, newScore=False)
    sounds.channel3.play(sounds.sound_swoosh)
    while ResetGame == False:
      drawAssets(bg_gameZone, bg_titleScreen, bg_img, bg_grounds, bg_gamePipes, flappyBird, gamePoints, finalScore, suppressScore=True)
      finalScore.next(bg_gameZone)
      flappyBird.next()
      # check for bottom collision
      if (flappyBird.posy + BIRDSIZE) >= WINDOWHEIGHT - ground_img.get_size()[1]:
        if flappyBird.loop == True:
          sounds.channel2.play(sounds.sound_hit)
          sounds.channel2.queue(sounds.sound_die)
        flappyBird.posy = (WINDOWHEIGHT - BIRDSIZE - ground_img.get_size()[1])
        flappyBird.loop = False
        GameOver = True

      for event in pygame.event.get():
        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or (event.type == pygame.KEYDOWN and event.key == K_SPACE):
          if flappyBird.posy == (WINDOWHEIGHT - BIRDSIZE - ground_img.get_size()[1]):
            ResetGame = True
        if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and bool(event.mod & pygame.KMOD_ALT)) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
          pygame.quit()
          sys.exit()

      pygame.display.update()
      fps.tick(60)

if __name__ == '__main__':
  main()