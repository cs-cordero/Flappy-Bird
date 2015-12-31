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

pygame.init()
fps = pygame.time.Clock()

pygame.display.set_caption('Flappy Bird')
canvas = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
canvas.set_colorkey(COLORKEY)

def generateBackground():
  if random.randint(0,1) == 0: background_img = pygame.image.load(os.path.join('images','background_light.png')).convert()
  else: background_img = pygame.image.load(os.path.join('images','background_dark.png')).convert()
  background_size = background_img.get_size()
  background_img = pygame.transform.scale(background_img,(int(WINDOWHEIGHT*1.1*(float(background_size[0])/float(background_size[1]))),WINDOWHEIGHT))
  return background_img, background_img.get_size()

def loadPlayerSprites():
  rects = []
  for x in range(1,9): rects.append(pygame.Rect(17*(x-1),0,17,12))
  sheet = spritesheet(os.path.join('images','player_bird.png'))
  images = sheet.images_at(rects, COLORKEY)
  resized_images = []
  for image in images: resized_images.append(pygame.transform.scale(image,(BIRDSIZE*(image.get_size()[0]/image.get_size()[1]),BIRDSIZE)))
  return resized_images

def main():
  background_img, background_size = generateBackground()
  bird_imgs = loadPlayerSprites()

  while True:
    canvas.fill(BLACK)
    canvas.blit(background_img,((WINDOWWIDTH/2)-(background_size[0]/2),0))
    canvas.blit(bird_imgs[0],(10,10))

    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
    pygame.display.update()
    fps.tick(60)


if __name__ == '__main__':
  main()