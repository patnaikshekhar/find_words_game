#!/usr/bin/env python

import random
import sys
import pygame
import gametimer
from pygame.locals import *
from common import *

# Setting up constants

BOARDWIDTH = 8
BOARDHEIGHT = 6
TILESIZE = 80
GAPBETWEENTILES = 10

XMARGIN = 100
YMARGIN = 62

TILEFONTCOLOR = BLACK
TILECOLOR = YELLOW
TILEHIGHLIGHTCOLOR = DARKTURQUOISE
TILESELECTEDCOLOR = DARKORANGE

TILETOPLEFTFONTSIZE = 10
TILEBOTTOMRIGHTFONTSIZE = 10
TILECENTERFONTSIZE = 32
TILEEDGEOFFSET = 12
TILEHIGHLIGHTSIZE = 4
TILEHIGHLIGHOFFSET = 3

LETTER_SCORES = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4,
                    'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1,
                    'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1,
                    's': 1, 't': 1, 'u': 4, 'v': 4, 'w': 4, 'x': 8,
                    'y': 4, 'z': 10}


TRIPPLE_LETTER_TILE = 'TL'
DOUBLE_LETTER_TILE = 'DL'
TRIPPLE_WORD_TILE = 'TW'
DOUBLE_WORD_TILE = 'DW'
TEN_TIMES_TILE = 'TT'

DOUBLE_LETTER_CHANCE = 8
TRIPPLE_LETTER_CHANCE = 10
DOUBLE_WORD_CHANCE = 20
TRIPPLE_WORD_CHANCE = 40
TEN_TIMES_CHANCE = 100

DOUBLE_LETTER_IMAGE = pygame.image.load("images/Mauve.png")
TRIPPLE_LETTER_IMAGE = pygame.image.load("images/Pink.png")
DOUBLE_WORD_IMAGE = pygame.image.load("images/Green.png")
TRIPPLE_WORD_IMAGE = pygame.image.load("images/DeepPink.png")
TEN_TIMES_IMAGE = pygame.image.load("images/Blue.png")
TILE_IMAGE = pygame.image.load("images/Yellow.png")
TILE_SELECTED_IMAGE = pygame.image.load("images/Orange.png")

DOUBLE_LETTER_COLOR = OLIVEDRAB
TRIPPLE_LETTER_COLOR = VIOLETRED
DOUBLE_WORD_COLOR = CHARTREUSE
TRIPPLE_WORD_COLOR = MAROON
TEN_TIMES_COLOR = CORNFLOWERBLUE

WORD_IN_PROGRESS_FONT_SIZE = 30
WORD_IN_PROGRESS_FONT_COLOR = DODGERBLUE
WORD_IN_PROGRESS_FONT_CENTERX = XMARGIN + (TILESIZE + GAPBETWEENTILES) \
    * (BOARDWIDTH / 2)
WORD_IN_PROGRESS_FONT_CENTERY = YMARGIN / 2

TOP_LEFT_AND_RIGHT_TEXT_ADJUST = 5

TIME_LEFT_FONT_SIZE = 25
TIME_LEFT_FONT_COLOR = BLACK
TIME_LEFT_FONT_LEFT = XMARGIN
TIME_LEFT_FONT_TOP = YMARGIN / 2 - TOP_LEFT_AND_RIGHT_TEXT_ADJUST

SCORE_FONT_SIZE = 25
SCORE_FONT_COLOR = BLACK
SCORE_FONT_RIGHT = XMARGIN + (TILESIZE + GAPBETWEENTILES) * BOARDWIDTH \
    - GAPBETWEENTILES
SCORE_FONT_BOTTOM = YMARGIN - TOP_LEFT_AND_RIGHT_TEXT_ADJUST

WORDS_MADE_FONT_SIZE = 20
WORDS_MADE_FONT_LEFT = (2 * XMARGIN) + (TILESIZE + GAPBETWEENTILES) \
    * BOARDWIDTH - GAPBETWEENTILES
WORDS_MADE_FONT_TOP = YMARGIN

WORDS_MADE_LEVEL0_FONT_COLOR = LIGHTSKYBLUE
WORDS_MADE_LEVEL1_FONT_COLOR = INDIANRED3
WORDS_MADE_LEVEL2_FONT_COLOR = STEELBLUE
WORDS_MADE_LEVEL3_FONT_COLOR = CADETBLUE
WORDS_MADE_LEVEL4_FONT_COLOR = DARKGREEN
WORDS_MADE_LEVEL5_FONT_COLOR = RED4

WORDS_MADE_LEVEL1 = 50
WORDS_MADE_LEVEL2 = 80
WORDS_MADE_LEVEL3 = 100
WORDS_MADE_LEVEL4 = 150
WORDS_MADE_LEVEL5 = 200


def main(gameType, scoreGoal):
    """
        This is the main function which handles the flow of the game
    """

    global FPSCLOCK, DISPLAYSURF
    all_words = loadDictionary()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0
    mousey = 0
    pygame.display.set_caption("Find Words!!")

    # Mainboard variable storing the whole board data
    mainBoard = getRandomizedBoard()

    # Create a timer object and start the timer for the game
    timer = gametimer.Timer(0.5)
    timer.start()

    # Initialize variables
    selectedLetters = []
    words_created = {}
    highlightedBox = None
    score = 0

    # Main game loop
    while True:
        mouseClicked = False

        timeLeft = timer.getTimeLeft()

        if timeLeft is None:
            break
        elif score > scoreGoal:
            break

        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, selectedLetters, highlightedBox, score, scoreGoal,
            timeLeft, words_created)

        for event in pygame.event.get():
            # If the event is quit (close window) then close the game
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP:
                # If event is escape then remove selected letters
                if event.key == K_ESCAPE:
                    selectedLetters = []
                # If event is enter then check word
                elif event.key == K_RETURN:
                    new_score = checkWord(mainBoard, selectedLetters,
                        all_words, words_created)
                    score += new_score
                    selectedLetters = []

            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

            tileX, tileY = getTileAtPixel(mousex, mousey)

            if tileX is not None and tileY is not None:
                highlightedBox = (tileX, tileY)
                if mouseClicked:
                    if (tileX, tileY) not in selectedLetters:
                        selectedLetters += [(tileX, tileY)]
                    else:
                        selectedLetters.remove((tileX, tileY))
            else:
                highlightedBox = None

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    return score


def getRandomizedBoard():
    """
        This function generates a random board with letters. It
        also calculates the score for the letters and whether the
        letters have any special score associated with them
    """

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    board = []
    for row in range(BOARDHEIGHT):
        new_row = []
        for column in range(BOARDWIDTH):
            random_letter = random.choice(letters)

            if random_letter.lower() in LETTER_SCORES:
                score = LETTER_SCORES[random_letter.lower()]

            double_letter_random = random.randint(1, DOUBLE_LETTER_CHANCE)
            tripple_letter_random = random.randint(1, TRIPPLE_LETTER_CHANCE)
            double_word_random = random.randint(1, DOUBLE_WORD_CHANCE)
            tripple_word_random = random.randint(1, TRIPPLE_WORD_CHANCE)
            ten_times_random = random.randint(1, TEN_TIMES_CHANCE)

            if ten_times_random == 1:
                special = TEN_TIMES_TILE
            elif tripple_word_random == 1:
                special = TRIPPLE_WORD_TILE
            elif double_word_random == 1:
                special = DOUBLE_WORD_TILE
            elif tripple_letter_random == 1:
                special = TRIPPLE_LETTER_TILE
            elif double_letter_random == 1:
                special = DOUBLE_LETTER_TILE
            else:
                special = None

            new_row.append((random_letter, score, special))

        board.append(new_row)

    return board


def loadDictionary():
    """
        This function loads the dictionary of words into a list
    """
    all_words = []
    f = open('words.txt')
    for line in f:
        all_words.append(line.strip())
    return all_words


def topLeftCoordsOfBox(boxX, boxY):
    """
        This function returns the top left corner of the board
    """

    left = XMARGIN + ((TILESIZE + GAPBETWEENTILES) * boxX)
    top = YMARGIN + ((TILESIZE + GAPBETWEENTILES) * boxY)
    return (left, top)


def drawBoard(board, selectedLetters, highlightedBox, totalScore, scoreGoal,
                timeLeft, words_created):
    """
        This function draws the board on the display surface
    """
    # Draw the tiles for the board
    for row in range(BOARDHEIGHT):
        for column in range(BOARDWIDTH):
            left, top = topLeftCoordsOfBox(column, row)

            # Hightlight box which the mouse is hovering on
            if highlightedBox:
                if (column, row) == highlightedBox:
                    highlightBox(column, row)

            letter = board[row][column][0]
            score = board[row][column][1]
            special = board[row][column][2]

            if (column, row) in selectedLetters:
                drawColor = TILESELECTEDCOLOR
                tileImage = TILE_SELECTED_IMAGE
            elif special == DOUBLE_LETTER_TILE:
                drawColor = DOUBLE_LETTER_COLOR
                tileImage = DOUBLE_LETTER_IMAGE
            elif special == TRIPPLE_LETTER_TILE:
                drawColor = TRIPPLE_LETTER_COLOR
                tileImage = TRIPPLE_LETTER_IMAGE
            elif special == DOUBLE_WORD_TILE:
                drawColor = DOUBLE_WORD_COLOR
                tileImage = DOUBLE_WORD_IMAGE
            elif special == TRIPPLE_WORD_TILE:
                drawColor = TRIPPLE_WORD_COLOR
                tileImage = TRIPPLE_WORD_IMAGE
            elif special == TEN_TIMES_TILE:
                drawColor = TEN_TIMES_COLOR
                tileImage = TEN_TIMES_IMAGE
            else:
                drawColor = TILECOLOR
                tileImage = TILE_IMAGE

            drawTile(left, top, drawColor, letter, special, str(score),
                tileImage)

    # Draw word on top
    word = ""
    for letterPosition in selectedLetters:
        word += board[letterPosition[1]][letterPosition[0]][0]

    if word != "":
        drawText(word, WORD_IN_PROGRESS_FONT_SIZE,
            WORD_IN_PROGRESS_FONT_COLOR, BGCOLOR,
            center=(WORD_IN_PROGRESS_FONT_CENTERX,
            WORD_IN_PROGRESS_FONT_CENTERY))

    # Draw timer on top left
    drawText(timeLeft, TIME_LEFT_FONT_SIZE,
            TIME_LEFT_FONT_COLOR, BGCOLOR,
            topLeft=(TIME_LEFT_FONT_LEFT,
            TIME_LEFT_FONT_TOP))

    # Draw totalScore on top right
    totalScoreString = str(totalScore)

    if scoreGoal:
        totalScoreString += " / " + str(scoreGoal)

    drawText(totalScoreString, SCORE_FONT_SIZE,
            SCORE_FONT_COLOR, BGCOLOR,
            bottomRight=(SCORE_FONT_RIGHT,
            SCORE_FONT_BOTTOM))

    # Draw the list of words already made on the right
    drawWordsCreated(words_created)


def drawTile(left, top, color, letter, upperleft, lowerright, tileImage):
    """
        This function draws a tile on the display surface
    """

    # Draw tile background
    #pygame.draw.rect(DISPLAYSURF, color, (left, top, TILESIZE, TILESIZE))
    DISPLAYSURF.blit(tileImage, (left, top))

    # Draw a letter on tile
    drawText(letter, TILECENTERFONTSIZE, TILEFONTCOLOR, None, topLeft=None,
        center=(left + TILESIZE / 2, top + TILESIZE / 2), bottomRight=None)

    # Draw a Special info on tile
    if upperleft != "":
        drawText(upperleft, TILETOPLEFTFONTSIZE, TILEFONTCOLOR, None,
            topLeft=(left + TILEEDGEOFFSET, top + TILEEDGEOFFSET), center=None,
            bottomRight=None)

    # Draw a letter score on tile
    if lowerright != "":
        drawText(lowerright, TILEBOTTOMRIGHTFONTSIZE, TILEFONTCOLOR, None,
            topLeft=None, center=None, bottomRight=(
            left + TILESIZE - TILEEDGEOFFSET, top + TILESIZE - TILEEDGEOFFSET))


def drawText(text, size, color, bgcolor, topLeft=None, center=None,
    bottomRight=None):
    """
        This function draws text at a certain location
    """
    fontObj = pygame.font.Font('freesansbold.ttf', size)
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

    DISPLAYSURF.blit(textSurfaceObj, textRectObj)


def getTileAtPixel(x, y):
    """
        This function figures out which box the mouse is currently on
    """
    for yCounter in range(BOARDHEIGHT):
        for xCounter in range(BOARDWIDTH):
            left, top = topLeftCoordsOfBox(xCounter, yCounter)
            rect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if rect.collidepoint(x, y):
                return xCounter, yCounter

    return (None, None)


def highlightBox(tileX, tileY):
    """
        This function highlights the box the mouse is hovering on
    """
    left, top = topLeftCoordsOfBox(tileX, tileY)
    pygame.draw.rect(DISPLAYSURF, TILEHIGHLIGHTCOLOR,
        (left - TILEHIGHLIGHOFFSET, top - TILEHIGHLIGHOFFSET,
            TILESIZE + (2 * TILEHIGHLIGHOFFSET) - 1,
            TILESIZE + (2 * TILEHIGHLIGHOFFSET) - 1),
            TILEHIGHLIGHTSIZE)


def checkWord(board, selectedLetters, all_words, words_created):
    """
        This function checks if the selected letters are a word
        and then calculates the score. It also adds to the words
        created
    """
    word = ""
    score = 0
    doubleWordCount = 0
    trippleWordCount = 0
    tenTimesWordCount = 0

    for letterPosition in selectedLetters:
        letter = board[letterPosition[1]][letterPosition[0]][0]
        letterScore = board[letterPosition[1]][letterPosition[0]][1]
        special = board[letterPosition[1]][letterPosition[0]][2]

        if special == DOUBLE_LETTER_TILE:
            letterScore = letterScore * 2
        elif special == TRIPPLE_LETTER_TILE:
            letterScore = letterScore * 3
        elif special == DOUBLE_WORD_TILE:
            doubleWordCount += 1
        elif special == TRIPPLE_WORD_TILE:
            trippleWordCount += 1
        elif special == TEN_TIMES_TILE:
            tenTimesWordCount += 1

        score += letterScore
        letter = letter.lower()
        word += letter

    # Calculate final word score
    if doubleWordCount > 0:
        score = score * (2 * doubleWordCount)

    if trippleWordCount > 0:
        score = score * (3 * trippleWordCount)

    if tenTimesWordCount > 0:
        score = score * (10 * tenTimesWordCount)

    if word not in words_created:
        if word in all_words:
            words_created[word] = score
            return score

    return 0


def terminate():
    pygame.quit()
    sys.exit()


def drawWordsCreated(words_created):
    """
        This function draws the list of words that the player
        has already created
    """

    adjustment = 0

    for word in words_created:
        score = words_created[word]
        word = word.upper()
        fontColor = getWordsCreatedFontColor(score)

        wordsCreatedText = word + " (" + str(score) + ")"

        drawText(wordsCreatedText, WORDS_MADE_FONT_SIZE,
                fontColor, BGCOLOR,
                topLeft=(WORDS_MADE_FONT_LEFT,
                WORDS_MADE_FONT_TOP + adjustment))
        adjustment += WORDS_MADE_FONT_SIZE


def getWordsCreatedFontColor(score):
    """
        This function returns the color of the font to be used for
        the word. Depending on the score
    """
    color = BLACK

    if score >= WORDS_MADE_LEVEL5:
        color = WORDS_MADE_LEVEL5_FONT_COLOR
    elif score >= WORDS_MADE_LEVEL4:
        color = WORDS_MADE_LEVEL4_FONT_COLOR
    elif score >= WORDS_MADE_LEVEL3:
        color = WORDS_MADE_LEVEL3_FONT_COLOR
    elif score >= WORDS_MADE_LEVEL2:
        color = WORDS_MADE_LEVEL2_FONT_COLOR
    elif score >= WORDS_MADE_LEVEL1:
        color = WORDS_MADE_LEVEL1_FONT_COLOR
    else:
        color = WORDS_MADE_LEVEL0_FONT_COLOR

    return color

if __name__ == '__main__':
    pygame.init()
    main()
