#!/usr/bin/env python

import pygame
from common import *
import splash_screen
import game_board
import game_over

SINGLE_PLAYER_FIRST_GOAL = 200


def startGame(gameType):
    """
        This function starts the actual game
    """

    if gameType == GAME_TYPE_SINGLE_PLAYER:
        goal = SINGLE_PLAYER_FIRST_GOAL
    else:
        goal = None

    # Loop once for multiplayer and until the goal is not
    # Reached for single player
    while True:
            score = game_board.main(gameType, goal)

            if gameType == GAME_TYPE_SINGLE_PLAYER:
                if score < goal:
                    return score
                else:
                    goal = int(goal * 1.2)
            else:
                return score


def main():

    pygame.init()
    splash_screen.main()

    while True:

        # Menu code will go here
        # gameType = menu.main()
        gameType = GAME_TYPE_SINGLE_PLAYER

        if gameType == GAME_TYPE_SINGLE_PLAYER or \
        gameType == GAME_TYPE_MULTI_PLAYER:
            score = startGame(gameType)
            game_over.main(score)
        elif gameType == GAME_TYPE_INSTRUCTIONS:
            # The code to show instructions will go here
            # instructions.main()
            pass
        else:
            terminate()


if __name__ == '__main__':
    main()
