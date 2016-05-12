import pygame, random
import scripts.sounds as sounds
from scripts.constants import *
from flappybird import scaletoheight, scaletowidth, displayText
from math import ceil, floor

class bird(object):
  def __init__(self, bird_imgs, loop=True, frames=1, angle=0):
    # select and create bird image
    x = random.randint(0,2)
    self.image_list = []
    self.image_list.append(bird_imgs[0+(x*3)])
    self.image_list.append(bird_imgs[1+(x*3)])
    self.image_list.append(bird_imgs[2+(x*3)])
    self.img = self.image_list[0]

    # positional variables
    self.posx = (WINDOWWIDTH / 2) - (BIRDSIZE / 2)
    self.posy = 256.0
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
    
    # hover variables
    self.boundary_upper = self.posy + int(scaletoheight(5.0))
    self.boundary_lower = self.posy + int(scaletoheight(10.0))
    self.hover_dy = 1.0
    self.hover_dy2 = 0.05

  def hover(self):
    self.hover_dy = max(min(self.hover_dy + self.hover_dy2,1.5),-1.5)
    self.posy += self.hover_dy
    if self.posy < self.boundary_upper: self.hover_dy2 = abs(self.hover_dy2)
    elif self.posy > self.boundary_lower: self.hover_dy2 = abs(self.hover_dy2)*-1

  def next(self):
    if self.i >=(len(self.image_list)): self.i = 0
    self.fall()  # manipulate y position
    self.rotate()  # manipulate the rotation of the bird
    self.img = pygame.transform.rotate(self.image_list[self.i],self.angle)  # manipulate the rotation of the bird

    # loops the sprite list to animate the bird flapping wings
    if self.loop:
      self.f -= 1
      if self.f == 0:
        self.i += 1
        self.f = self.frames
  
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
  def __init__(self, pipeImgs, gameZone, groundClearance):
    self.status = "Incoming"
    self.opening = pygame.Rect((WINDOWWIDTH/2)+(gameZone[0]/2), random.randint(30, WINDOWHEIGHT-PIPEOPENING-int(60.0/WINDOWHEIGHT)-groundClearance),PIPEWIDTH, PIPEOPENING)
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


class gameGround(object):
  def __init__(self, groundImg, startingx):
    self.rect = pygame.Rect(startingx,WINDOWHEIGHT-groundImg.get_size()[1],groundImg.get_size()[0],groundImg.get_size()[1])
    self.img = groundImg

  def next(self, gameZone):
    self.rect.left -= PIPESPEED
    if self.rect.right <= gameZone.left: self.rect.left = gameZone.right - 2

class titleScreen(object):
  def __init__(self, titleImg, startingx):
    self.rect = pygame.Rect(WINDOWWIDTH/2 - titleImg.get_size()[0]/2,  int(scaletoheight(144.0)), titleImg.get_size()[0], titleImg.get_size()[1])
    self.img = titleImg

  def next(self, gameZone):
    if self.rect.right > gameZone.left: self.rect.left -= PIPESPEED*10

class finalScoreBox(object):
  def __init__(self, scoreboxImg, newScoreImg, gameZone):
    self.rect = scoreboxImg.get_rect()
    self.rect.bottomleft = gameZone.midright
    self.img = scoreboxImg
    self.newscoreimg = newScoreImg

  def update(self,gamePoints,highScore,newScore=False):
    gameScoreWhite = displayText(str(gamePoints), scaletowidth(75.0), scaletoheight(55.0), color=WHITE)
    gameScoreBlack = displayText(str(gamePoints), scaletowidth(75.0), scaletoheight(55.0), color=BLACK)
    gameScoreBlack[1].right += scaletowidth(3)
    gameScoreBlack[1].top += scaletoheight(3)
    self.img.blit(gameScoreBlack[0], gameScoreBlack[1])
    self.img.blit(gameScoreWhite[0], gameScoreWhite[1])

    highScoreWhite = displayText(str(highScore), scaletowidth(190.0), scaletoheight(55.0), color=WHITE)
    highScoreBlack = displayText(str(highScore), scaletowidth(190.0), scaletoheight(55.0), color=BLACK)
    highScoreBlack[1].right += scaletowidth(3)
    highScoreBlack[1].top += scaletoheight(3)
    self.img.blit(highScoreBlack[0], highScoreBlack[1])
    self.img.blit(highScoreWhite[0], highScoreWhite[1])

    if newScore: self.img.blit(self.newscoreimg, (scaletowidth(200),scaletoheight(10)))

  def next(self, gameZone):
    if self.rect.centerx > gameZone.centerx: self.rect.left -= PIPESPEED*10
    else: self.rect.centerx = gameZone.centerx