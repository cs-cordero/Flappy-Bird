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
    self.posx = (WINDOWWIDTH / 2) - (BIRDSIZE / 2)
    self.posy = 60.0
    self.dy = 0.00
    self.right = self.posx + BIRDSIZE
    self.center = self.posx + (BIRDSIZE/2)

    # animation variables
    self.i = 0
    self.f = frames
    self.loop = True
    self.frames = frames
    
    # angle variables
    self.angle = angle
    self.dt_angle = -0.1

  def next(self):
    if self.i >=(len(self.image_list)): self.i = 0
    self.fall()  # manipulate y position
    self.rotate()  # manipulate the rotation of the bird
    image = pygame.transform.rotate(self.image_list[self.i],self.angle)  # manipulate the rotation of the bird

    # loops the sprite list to animate the bird flapping wings
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
    elif flap == True:
      self.posy -= FLAPHEIGHT
      self.dy = 0.00
      self.loop = True
      sounds.channel1.play(sounds.sound_wingflap)
      if self.posy <= 0: self.posy = 0


class gamePipe(object):
  def __init__(self, pipeImgs, gameZone):
    self.status = "Incoming"
    self.opening = pygame.Rect((WINDOWWIDTH/2)+(gameZone[0]/2), random.randint(30, WINDOWHEIGHT-PIPEOPENING-60),PIPEWIDTH, PIPEOPENING)
    self.images = pipeImgs

  def next(self):
    self.opening.left -= PIPESPEED

  def checkCollision(self, player, points):
    # player is horizontally between the pipes
    if player.right > self.opening.left and player.right < self.opening.right:
      if self.status != "Killed" and (player.posy < self.opening.top or player.posy + BIRDSIZE > self.opening.bottom):
        self.status = "Killed"
        player.loop = False
        sounds.channel2.play(sounds.sound_hit)
        sounds.channel2.queue(sounds.sound_die)
      elif self.status == "Incoming" and player.center >= self.opening.centerx:
        self.status = "Passed"
        points += 1
        sounds.channel2.play(sounds.sound_point)
    return self.status, points