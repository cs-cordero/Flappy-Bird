import os, pygame, random

pygame.mixer.init()
sound_wingflap = pygame.mixer.Sound(os.path.join('..','audio','sfx_wing.ogg'))
sound_swoosh = pygame.mixer.Sound(os.path.join('..','audio','sfx_swooshing.ogg'))
sound_die = pygame.mixer.Sound(os.path.join('..','audio','sfx_die.ogg'))
sound_hit = pygame.mixer.Sound(os.path.join('..','audio','sfx_hit.ogg'))
sound_point = pygame.mixer.Sound(os.path.join('..','audio','sfx_point.ogg'))
channel1 = pygame.mixer.Channel(1)
channel2 = pygame.mixer.Channel(2)
channel3 = pygame.mixer.Channel(3)