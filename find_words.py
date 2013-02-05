import random, sys, pygame
from pygame.locals import *

# Setting up constants

FPS = 30
WINDOWWIDTH = 1200
WINDOWHEIGHT = 600
BOARDWIDTH = 8
BOARDHEIGHT = 6
TILESIZE = 80
GAPBETWEENTILES = 10

XMARGIN = 150
YMARGIN = 50

WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)
BLACK = (0, 0, 0)

BGCOLOR = WHITE
TILEFONTCOLOR = BLACK
TILECOLOR = YELLOW
FONTSIZE = 32
"""
    This is the main function which handles the flow of the game
"""
def main():
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
    score = 0

    DISPLAYSURF.fill(BGCOLOR)

    # Main game loop
    while True:
        mouseClicked = False

        drawBoard(mainBoard, selectedLetters)

        for event in pygame.event.get():
            # If the event is quit (close window) then close the game
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


"""
    This function generates a random board with letters
"""
def getRandomizedBoard():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    board = []
    for row in range(BOARDHEIGHT):
        new_row = []
        for column in range(BOARDWIDTH):
            new_row.append(random.choice(letters))
        board.append(new_row)
    return board


"""
    This function loads the dictionary of words into a list
"""
def loadDictionary():
    all_words = []
    f = open('words.txt')
    for line in f:
        all_words.append(line)
    return all_words


"""
    This function returns the top left corner of the board
"""
def topLeftCoordsOfBox(boxX, boxY):
    left = XMARGIN + ((TILESIZE + GAPBETWEENTILES) * boxX)
    top = YMARGIN + ((TILESIZE + GAPBETWEENTILES) * boxY)
    return (left, top)


"""
    This function draws the board on the display surface
"""
def drawBoard(board, selectedLetters):

    for row in range(BOARDHEIGHT):
        for column in range(BOARDWIDTH):
            left, top = topLeftCoordsOfBox(column, row)

            drawTile(left, top, TILECOLOR, board[row][column], "", "")

def drawTile(left, top, color, letter, upperleft, lowerright):

    # Draw tile background
    pygame.draw.rect(DISPLAYSURF, color, (left, top, TILESIZE, TILESIZE))

    # Draw letter on tile
    fontObj = pygame.font.Font('freesansbold.ttf', FONTSIZE)
    textSurfaceObj = fontObj.render(letter, True, TILEFONTCOLOR, color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (left + TILESIZE / 2, top + TILESIZE / 2)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

if __name__ == '__main__':
    main()
