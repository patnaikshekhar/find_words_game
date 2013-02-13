#!/usr/bin/env python

import pygame
from pygame.locals import *
from common import *


def main():
    """
        This is the main function which handles the flow of the game
    """

    global FPSCLOCK, DISPLAYSURF

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Find Words!!")
    FPSCLOCK = pygame.time.Clock()

    while True:
        DISPLAYSURF.fill(BGCOLOR)

        for event in pygame.event.get():
            # If the event is quit (close window) then close the game
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                break

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    return None


if __name__ == '__main__':
    pygame.init()
    main()
