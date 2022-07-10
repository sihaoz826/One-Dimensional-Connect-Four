#################################################
# hw7: One-Dimensional Connect Four
# name: Sihao Zhou
# andrew id: sihaoz
#
# collaborator(s) names and andrew ids: William Tang (wyt)
# and Nirmay Bhanderi (nbhander)
# 
#################################################

import cs112_n21_week3_linter
from cmu_112_graphics import *
import random, string, math, time

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# main app
#################################################

'''
helper functions 
'''

# return the center and radius of a piece at the given index
def getPieceCenterAndRadius(app, pieceIndex):
    cx = app.width/app.total*0.5 + app.width/app.total*pieceIndex
    cy = app.height/2
    r = app.width/app.total*0.5*0.8
    return (cx, cy, r)

# gives the distance between two points
def distance(x0, y0, x1, y1):
    return (abs(x1-x0)**2 + abs(y1-y0)**2)**0.5

# return the index of the piece given mousepressed x and y
def getPieceIndex(app, x, y):
    for i in range(len(app.board)):
        (cx, cy, r) = getPieceCenterAndRadius(app, i)
        if distance(cx, cy, x, y) <= r:
            return i
        else:
            pass
    return None

# initialize the board
def initializeBoard(app):
    board = [] * app.total
    p1 = app.currentPlayer
    p2 = abs(1 - app.currentPlayer)
    for i in range(app.total):
        if i % 2 == 0:
            board.append(p1)
        else:
            if p1 == 1:
                board.append(0)
            else:
                board.append(1)
    return board


# reset the three elements is the game is over
def checkForWin(app):
    for i in range(len(app.board) - 3):
        if (app.board[i] == app.board[i+1] == app.board[i+2] == app.board[i+3]):
            app.gameOver = True
            app.message = 'Game Over!!!'
            app.winningRunStartIndex = i
            app.showBox = False
        else:
            pass

# move the current selection to the left or right
def moveSelection(app, moveToLeftEnd):
    board = app.board
    index = app.selectionCenterIndex
    first = board[:index-1]
    middle = board[index-1: index+2]
    last = board[index+2:]
    if moveToLeftEnd == True:
        app.board = middle + first + last
    else:
        app.board = first + last + middle

# replace the color of the dot for keypressed = c
def replace(app):
    index = app.selectionCenterIndex
    if index >= 1 and index <= app.total - 1:
        app.board[index-1: index+2] = [app.currentPlayer] * 3
    else:
        pass
    checkForWin(app)

'''
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
'''


# we do not reset the number of dots
def appStarted(app):
    app.total = 10
    resetApp(app)

# we reset all the other features
def resetApp(app):
    app.currentPlayer = random.randint(0, 1)
    app.board = initializeBoard(app)
    app.gameOver = False
    app.message = 'Select your 3-piece block'
    app.winningRunStartIndex = -1
    app.selectionCenterIndex = None
    app.selection = None
    app.selected = False
    app.showBox = False
    app.boxColor = 'orange'

'''
mouse and key aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
'''

def mousePressed(app, event):
    # always check if the game is over or not
    checkForWin(app)

    # the first click
    if app.selected ==  False:
        app.selectionCenterIndex = getPieceIndex(app, event.x, event.y)
        # instance where we click outside the dots
        if app.selectionCenterIndex == None:
            app.message = 'Select your 3-piece block'
            app.selected = False
            app.showBox = False
        # instance where we click inside the dots
        else:
            app.showBox = True
            app.selection = [app.selectionCenterIndex-1,
                            app.selectionCenterIndex,
                            app.selectionCenterIndex+1]
            # click the second or second to last dot
            if (app.selection[0] == 0 or app.selection[2] == (app.total-1)):
                app.message = 'End cannot be in block'
                app.selected = False
                app.boxColor = 'pink'
            # click the first or last dots
            elif (app.selection[0] < 0 or app.selection[2] > (app.total-1)):
                app.message = 'Cannot move illegal selection' 
                app.selected = False
                app.boxColor = ''
            # three dots are all the same color
            elif (app.selection[0] == app.selection[1] == app.selection[2]):
                app.message = 'Block must contain current player'
                app.selected = False
                app.boxColor = 'orange'
            # the right click 
            else:
                app.message = 'Select end to move block to'
                app.selected = True
                app.boxColor = 'orange'
    # the second click
    else:
        # the index of the end that we are moving to 
        endSelection = getPieceIndex(app, event.x, event.y)
        # making player redo it if the end click is not at one of the ends
        if not (endSelection == 0 or endSelection == app.total - 1):
            app.selected = True
        else:
            app.selected = False
        # move to the left end
        if endSelection == 0:
            moveSelection(app, True)
            app.showBox = False
            app.selected = False
            app.currentPlayer = abs(1 - app.currentPlayer)
        # move to the right end
        elif endSelection == app.total - 1:
            moveSelection(app, False)
            app.showBox = False
            app.selected = False
            app.currentPlayer = abs(1 - app.currentPlayer)
        else:
            pass

def keyPressed(app, event):
    # reset stuff
    if event.key == "r":
        resetApp(app)
    # replace all three colors in the selection
    elif event.key == "c":
        replace(app)
    # change player
    elif event.key == "p":
        app.currentPlayer = abs(1 - app.currentPlayer)
    # increase the number of dots
    elif (event.key == "Up" or event.key == "Right") and app.total <= 18:
        app.total += 2
        resetApp(app)
    # decrease the number of dots
    elif (event.key == "Down" or event.key == "Left") and app.total >= 8:
        app.total -= 2
        resetApp(app)
    else:
        pass


'''
draw stuff bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
'''

def redrawAll(app, canvas):
    drawTitle(app, canvas)
    drawInstructions(app, canvas)
    drawCurrentPlayerAndMessage(app, canvas)
    drawBox(app, canvas)
    drawBoard(app, canvas)
    drawRules(app, canvas)
    drawLine(app, canvas)

# draw a line if we reach game over
def drawLine(app, canvas):
    if app.gameOver == True:
        cx0, cy0, r0 = getPieceCenterAndRadius(app, app.winningRunStartIndex)
        cx1, cy1, r1 = getPieceCenterAndRadius(app, app.winningRunStartIndex+3)
        canvas.create_line(cx0, cy0, cx1, cy1, width = 5)
    else:
        pass

# draws the title
def drawTitle(app, canvas):
    canvas.create_text(app.width/2, app.height/36,
                        text = 'One-Dimentional Connect Four',
                        anchor = 'n',
                        font = "Helvetica 15 bold")

# draws the instructions
def drawInstructions(app, canvas):
    messages = ['See rules below.',
                'Click interior piece to select center of 3-piece block.',
                'Click end piece to move that block to that end.',
                'Change board size (and then restart) with arrow keys.',
                'For debugging, press c to set the color of selected block.',
                'For debugging, press p to change the current player.',
                'Press r to restart.',
               ]

    for line in range(len(messages)):
        canvas.create_text(app.width/2, 
                            app.height/24*2 + app.height/24*line, 
                            text=messages[line],
                            anchor = 'n',
                            font="Helvetica 10 bold")

# draws the rules
def drawRules(app, canvas):
    messages = [
  "The Rules of One-Dimensional Connect Four:",
  "Arrange N (10 by default) pieces in a row of alternating colors.",
  "Players take turns to move three pieces at a time, where:",
  "      The pieces must be in the interior (not on either end)",
  "      The pieces must be adjacent (next to each other).",
  "      At least one moved piece must be the player's color.",
  "The three pieces must be moved in the same order to either end of the row.",
  "The gap must be closed by sliding the remaining pieces together.",
  "The first player to get four (or more) adjacent pieces of their color wins!",
               ]

    for line in range(len(messages)):
        canvas.create_text(app.width/80, app.height*16/25 + app.height/25*line,
                            text = messages[line],
                            anchor = 'w',
                            font = "Helvetica 10 bold")

def drawCurrentPlayerAndMessage(app, canvas):
    # set up the color of the text according to who is playing 
    if app.currentPlayer == 0:
        txt = "green"
    else:
        txt = "blue"

    # first text
    canvas.create_text(app.width/3, app.height*10/25,
                        text = 'Current Player: ',
                        font = "Helvetica 12 bold",
                        fill = txt)

    # circle in the middle
    cx = app.width/2
    cy = app.height*24/60
    r = app.height/60
    drawPlayerPiece(app, canvas, app.currentPlayer, cx, cy, r)

    # message at the end that can change            
    canvas.create_text(app.width*15/20, app.height*10/25,
                        text = app.message,
                        font = "Helvetica 12 bold",
                        fill = txt)

# draw the box that signals where the selection is at
def drawBox(app, canvas):
    if app.showBox:
        cx0, cy0, r0 = getPieceCenterAndRadius(app, app.selectionCenterIndex-1)
        cx1, cy1, r1 = getPieceCenterAndRadius(app, app.selectionCenterIndex+1)
        canvas.create_rectangle(cx0 - r0*6/5, cy0 - r0*6/5, 
                                cx1 + r0*6/5, cy1 + r0*6/5,
                                fill = app.boxColor, outline = '')
    else:
        pass

# draw a single dot
def drawPlayerPiece(app, canvas, player, cx, cy, r):
    # set up the color of the circle 
    if player == 0:
        fi, out = 'light green', 'green'
    else:
        fi, out = 'light blue', 'blue'
    # draw it 
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                        fill = fi, outline = out, width = 5)

# draw all the dots combined
def drawBoard(app, canvas):
    for index in range(len(app.board)):
        (cx, cy, r) = getPieceCenterAndRadius(app, index)
        if app.board[index] == 1:
            drawPlayerPiece(app, canvas, 1, cx, cy, r)
        else:
            drawPlayerPiece(app, canvas, 0, cx, cy, r)

def main():
    cs112_n21_week3_linter.lint()
    runApp(width=650, height=550)

if __name__ == '__main__':
    main()