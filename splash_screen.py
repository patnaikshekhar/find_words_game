#!/usr/bin/env python

import pygame
from pygame.locals import *
from common import *


PRESS_ANY_KEY_TEXT = 'Press any key to continue..'
PRESS_ANY_KEY_TEXT_FONT = DEFAULT_FONT
PRESS_ANY_KEY_TEXT_FONT_SIZE = 15
PRESS_ANY_KEY_TEXT_FONT_COLOR = RED4


def main():
    """
        This is the main function which handles the flow of the game
    """

    global FPSCLOCK, DISPLAYSURF

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Find Words!!')
    FPSCLOCK = pygame.time.Clock()

    logoImage = pygame.image.load('images/WordSprintLogo.png')
    imageRect = logoImage.get_rect()
    imageRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 3)
    textCenter = (WINDOWWIDTH / 2, WINDOWHEIGHT * 2 / 3)
#    textLeft, textTop = imageRect.bottomLeft

    while True:
        DISPLAYSURF.fill(BGCOLOR)

        DISPLAYSURF.blit(logoImage, imageRect)

        drawTextOnSurface(DISPLAYSURF, PRESS_ANY_KEY_TEXT_FONT,
        PRESS_ANY_KEY_TEXT, PRESS_ANY_KEY_TEXT_FONT_SIZE,
        PRESS_ANY_KEY_TEXT_FONT_COLOR, BGCOLOR,
        center=textCenter)

        for event in pygame.event.get():
            # If the event is quit (close window) then close the game
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                return None
            if event.type == MOUSEBUTTONUP:
                return None

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    main()
    terminate()
