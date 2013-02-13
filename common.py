import sys
import pygame

GAME_TYPE_SINGLE_PLAYER = 1
GAME_TYPE_MULTI_PLAYER = 2
GAME_TYPE_INSTRUCTIONS = 3
GAME_TYPE_EXIT = 4

FPS = 30
WINDOWWIDTH = 1200
WINDOWHEIGHT = 600


WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)
BLACK = (0, 0, 0)
DARKTURQUOISE = (0, 206, 209)
DARKORANGE = (255, 127, 0)
OLIVEDRAB = (179, 238, 58)
CHARTREUSE = (69, 139, 0)
VIOLETRED = (205, 50, 120)
MAROON = (139, 28, 98)
CORNFLOWERBLUE = (100, 149, 237)
DODGERBLUE = (30, 144, 255)
CADETBLUE = (95, 158, 160)
DARKGREEN = (0, 100, 0)
STEELBLUE = (70, 130, 80)
LIGHTSKYBLUE = (135, 206, 250)
INDIANRED3 = (205, 85, 85)
RED4 = (139, 0, 0)

BGCOLOR = WHITE

DEFAULT_FONT = 'freesansbold.ttf'


def terminate():
    """
        This function terminates the application
    """
    pygame.quit()
    sys.exit()


def drawTextOnSurface(surface, font, text, size, color, bgcolor, topLeft=None,
        center=None, bottomRight=None):
    """
        This function draws text at a certain location
    """
    fontObj = pygame.font.Font(font, size)
    if bgcolor:
        textSurfaceObj = fontObj.render(text, True, color, bgcolor)
    else:
        textSurfaceObj = fontObj.render(text, True, color)

    textRectObj = textSurfaceObj.get_rect()

    if center:
        textRectObj.center = center
    elif topLeft:
        textRectObj.topleft = topLeft
    else:
        textRectObj.bottomright = bottomRight

    surface.blit(textSurfaceObj, textRectObj)
