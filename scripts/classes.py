import pygame, random
import scripts.sounds as sounds
from scripts.constants import *

class bird(object):
  def __init__(self, bird_imgs, loop=True, frames=1, angle=0):
    # select and create bird image
    x = random.randint(0,2)
    self.image_list = []
    self.image_list.append(bird_imgs[0+(x*3)])
    self.image_list.append(bird_imgs[1+(x*3)])
    self.image_list.append(bird_imgs[2+(x*3)])

    # positional variables
    self.posx = 60.0
    self.posy = 60.0
    self.dy = 0.00

    # animation variables
    self.i = 0
    self.f = frames
    self.loop = loop
    self.frames = frames
    
    # angle variables
    self.angle = angle
    self.dt_angle = -0.1

  def next(self):
    if self.i >=(len(self.image_list)):
      if self.loop: self.i = 0
      else: pass
    self.fall()
    self.rotate()
    image = pygame.transform.rotate(self.image_list[self.i],self.angle)
    if self.loop:
      self.f -= 1
      if self.f == 0:
        self.i += 1
        self.f = self.frames
    return image
  
  def rotate(self,flap=False):
    if flap == False and self.loop == True:
      self.angle += self.dt_angle
      self.dt_angle -= 0.05
      if self.angle <= -80: self.angle = -80
    elif flap == True:
      self.angle = 45;
      self.dt_angle = -0.1
      self.loop = True

  def fall(self,flap=False):
    if flap == False:
      self.posy += self.dy
      self.dy += FALLSPEED
      if (self.posy + BIRDSIZE) >= WINDOWHEIGHT:
        if self.loop == True:
          sounds.channel2.play(sounds.sound_hit)
          sounds.channel2.queue(sounds.sound_die)
        self.posy = (WINDOWHEIGHT - BIRDSIZE)
        self.loop = False
    elif flap == True:
      self.posy -= FLAPHEIGHT
      self.dy = 0.00
      self.loop = True
      sounds.channel1.play(sounds.sound_wingflap)
      if self.posy <= 0: self.posy = 0