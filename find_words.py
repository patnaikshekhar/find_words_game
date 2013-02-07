import random
import sys
import pygame
from pygame.locals import *

# Setting up constants

FPS = 30
WINDOWWIDTH = 1200
WINDOWHEIGHT = 600
BOARDWIDTH = 8
BOARDHEIGHT = 6
TILESIZE = 80
GAPBETWEENTILES = 10

XMARGIN = 100
YMARGIN = 62

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

BGCOLOR = WHITE
TILEFONTCOLOR = BLACK
TILECOLOR = YELLOW
TILEHIGHLIGHTCOLOR = DARKTURQUOISE
TILESELECTEDCOLOR = DARKORANGE

TILETOPLEFTFONTSIZE = 10
TILEBOTTOMRIGHTFONTSIZE = 10
TILECENTERFONTSIZE = 32
TILEEDGEOFFSET = 3
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

DOUBLE_LETTER_COLOR = OLIVEDRAB
TRIPPLE_LETTER_COLOR = VIOLETRED
DOUBLE_WORD_COLOR = CHARTREUSE
TRIPPLE_WORD_COLOR = MAROON
TEN_TIMES_COLOR = CORNFLOWERBLUE

WORD_IN_PROGRESS_FONT_SIZE = 25
WORD_IN_PROGRESS_FONT_COLOR = DODGERBLUE
WORD_IN_PROGRESS_FONT_CENTERX = XMARGIN + (TILESIZE + GAPBETWEENTILES) \
    * (BOARDWIDTH / 2)
WORD_IN_PROGRESS_FONT_CENTERY = YMARGIN / 2

STARTING_SCORE_GOAL = 1000


def main():
    """
        This is the main function which handles the flow of the game
    """

    global FPSCLOCK, DISPLAYSURF
    all_words = loadDictionary()
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0
    mousey = 0
    pygame.display.set_caption("Find Words!!")

    # Mainboard variable storing the whole board data
    mainBoard = getRandomizedBoard()
    selectedLetters = []
    words_created = []
    highlightedBox = None
    score = 0
    scoreGoal = STARTING_SCORE_GOAL

    # Main game loop
    while True:
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, selectedLetters, highlightedBox, score, scoreGoal)

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
                    print score
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


def drawBoard(board, selectedLetters, highlightedBox, score, scoreGoal):
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
            elif special == DOUBLE_LETTER_TILE:
                drawColor = DOUBLE_LETTER_COLOR
            elif special == TRIPPLE_LETTER_TILE:
                drawColor = TRIPPLE_LETTER_COLOR
            elif special == DOUBLE_WORD_TILE:
                drawColor = DOUBLE_WORD_COLOR
            elif special == TRIPPLE_WORD_TILE:
                drawColor = TRIPPLE_WORD_COLOR
            elif special == TEN_TIMES_TILE:
                drawColor = TEN_TIMES_COLOR
            else:
                drawColor = TILECOLOR

            drawTile(left, top, drawColor, letter, special, str(score))

            # Draw word on top
            word = ""
            for letterPosition in selectedLetters:
                word += board[letterPosition[1]][letterPosition[0]][0]

            if word != "":
                drawText(word, WORD_IN_PROGRESS_FONT_SIZE,
                    WORD_IN_PROGRESS_FONT_COLOR, BGCOLOR,
                    center=(WORD_IN_PROGRESS_FONT_CENTERX,
                    WORD_IN_PROGRESS_FONT_CENTERY))


def drawTile(left, top, color, letter, upperleft, lowerright):
    """
        This function draws a tile on the display surface
    """

    # Draw tile background
    pygame.draw.rect(DISPLAYSURF, color, (left, top, TILESIZE, TILESIZE))

    # Draw a letter on tile
    drawText(letter, TILECENTERFONTSIZE, TILEFONTCOLOR, color, topLeft=None,
        center=(left + TILESIZE / 2, top + TILESIZE / 2), bottomRight=None)

    # Draw a Special info on tile
    if upperleft != "":
        drawText(upperleft, TILETOPLEFTFONTSIZE, TILEFONTCOLOR, color,
            topLeft=(left + TILEEDGEOFFSET, top + TILEEDGEOFFSET), center=None,
            bottomRight=None)

    # Draw a letter score on tile
    if lowerright != "":
        drawText(lowerright, TILEBOTTOMRIGHTFONTSIZE, TILEFONTCOLOR, color,
            topLeft=None, center=None, bottomRight=(
            left + TILESIZE - TILEEDGEOFFSET, top + TILESIZE - TILEEDGEOFFSET))


def drawText(text, size, color, bgcolor, topLeft=None, center=None,
    bottomRight=None):
    """
        This function draws text at a certain location
    """
    fontObj = pygame.font.Font('freesansbold.ttf', size)
    textSurfaceObj = fontObj.render(text, True, color, bgcolor)
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

    if word not in words_created:
        if word in all_words:
            words_created.append(word)

            # Calculate final word score
            if doubleWordCount > 0:
                score = score * (2 * doubleWordCount)

            if trippleWordCount > 0:
                score = score * (3 * trippleWordCount)

            if tenTimesWordCount > 0:
                score = score * (10 * tenTimesWordCount)

            return score

    return 0


def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
