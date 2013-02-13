#!/usr/bin/env python

import pygame
from pygame.locals import *
from common import *


PRESS_ANY_KEY_TEXT = 'Press any key to return to the menu..'
PRESS_ANY_KEY_TEXT_FONT = DEFAULT_FONT
PRESS_ANY_KEY_TEXT_FONT_SIZE = 15
PRESS_ANY_KEY_TEXT_FONT_COLOR = RED4
PRESS_ANY_KEY_TEXT_PADDING = 20

SCORE_TEXT = 'Your score is '
SCORE_TEXT_FONT = DEFAULT_FONT
SCORE_TEXT_FONT_SIZE = 30
SCORE_TEXT_FONT_COLOR = RED4


def main(score):
    """
        This is the main function which handles the flow of the game
    """

    global FPSCLOCK, DISPLAYSURF

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Game Over')
    FPSCLOCK = pygame.time.Clock()

    gameOverImage = pygame.image.load('images/WordSprintGameOver.png')
    imageRect = gameOverImage.get_rect()
    imageRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 3)
    scoreTextCenter = (WINDOWWIDTH / 2, WINDOWHEIGHT * 2 / 3)
    anyKeyTextCenter = (WINDOWWIDTH / 2,
        (WINDOWHEIGHT * 2) / 3 + PRESS_ANY_KEY_TEXT_PADDING +
            PRESS_ANY_KEY_TEXT_FONT_SIZE)

    while True:
        DISPLAYSURF.fill(BGCOLOR)

        DISPLAYSURF.blit(gameOverImage, imageRect)

        drawTextOnSurface(DISPLAYSURF, SCORE_TEXT_FONT,
        SCORE_TEXT + str(score), SCORE_TEXT_FONT_SIZE,
        SCORE_TEXT_FONT_COLOR, BGCOLOR,
        center=scoreTextCenter)

        drawTextOnSurface(DISPLAYSURF, PRESS_ANY_KEY_TEXT_FONT,
        PRESS_ANY_KEY_TEXT, PRESS_ANY_KEY_TEXT_FONT_SIZE,
        PRESS_ANY_KEY_TEXT_FONT_COLOR, BGCOLOR,
        center=anyKeyTextCenter)

        for event in pygame.event.get():
            # If the event is quit (close window) then close the game
            if event.type == QUIT:
                terminate()

            # If any key is pressed then exit
            if event.type == KEYUP:
                return None
            if event.type == MOUSEBUTTONUP:
                return None

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    main(1000)
    terminate()
