#Colors for Pygame
AQUA      = (  0, 255, 255)
BLACK     = (  0,   0,   0)
BLUE      = (  0,   0, 255)
FUCHSIA   = (255,   0, 255)
GRAY      = (128, 128, 128)
GREEN     = (  0, 128,   0)
LIME      = (  0, 255,   0)
MAROON    = (128,   0,   0)
NAVYBLUE  = (  0,   0, 128)
OLIVE     = (128, 128,   0)
PURPLE    = (128,   0, 128)
RED       = (255,   0,   0)
SILVER    = (192, 192, 192)
TEAL      = (  0, 128, 128)
WHITE     = (255, 255, 255)
YELLOW    = (255, 255,   0)

# Game Constants
FPS = 60

# Window Constants
WINDOWWIDTH = 1280  # original = 1280
WINDOWHEIGHT = 720  # original = 720
COLORKEY = (150,125,255)

# PLAYER CONSTANTS
BIRDSIZE = int((35.0/720.0)*WINDOWHEIGHT)
FLAPHEIGHT = (60.0/720.0)*WINDOWHEIGHT
FALLSPEED = (0.14/720.0)*WINDOWHEIGHT

# GAME CONSTANTS
PIPEOPENING = FLAPHEIGHT*2
PIPEWIDTH = int((75.0/1280.0)*WINDOWWIDTH)
PIPESPEED = (2.0/1280.0)*WINDOWWIDTH