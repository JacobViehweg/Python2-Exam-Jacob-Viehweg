# Chess game :
# Make a working game of chess that runs in the terminal
# The game supports two players
# The game needs to be able to detect weather or not the king is threatened or if theres a checkmate or stalemate

import colorama
import math
import copy

colorama.init()

pieceDict = {} # Dictionary containing pieces

pieceDict[0] = '' # When a spot is empty
pieceDict[1] = 'Pawn'
pieceDict[2] = 'Tower'
pieceDict[3] = 'Horse'
pieceDict[4] = 'Bishop'
pieceDict[5] = 'Queen'
pieceDict[6] = 'King'

boardColor = {}
boardColor[True] = colorama.Back.WHITE
boardColor[False] = colorama.Back.BLACK

pieceColor = {}
pieceColor[0] = ''
pieceColor[1] = colorama.Fore.WHITE + colorama.Back.LIGHTBLACK_EX
pieceColor[2] = colorama.Fore.BLACK + colorama.Back.LIGHTBLACK_EX

board = [ [],[],[],[],[],[],[],[] ] # 2-dimensional array with 8 rows

turnState = 1 # Determines whos turn it is | 1 = white turn, 2 = black turn

def resetBoard():
    return [
    [(2, 1), (3, 1), (4, 1), (6, 1), (5, 1), (4, 1), (3, 1), (2, 1)],
    [(1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
    [(1, 2), (1, 2), (1, 2), (1, 2), (1, 2), (1, 2), (1, 2), (1, 2)],
    [(2, 2), (3, 2), (4, 2), (6, 2), (5, 2), (4, 2), (3, 2), (2, 2)] ]

# Prints out the board. Uses several for i loops
def printBoard():
    global board
    global boardColor
    global pieceColor
    global pieceDict

    printBoard = '\t   a\t   b\t   c\t   d\t   e\t   f\t   g\t   h\t\n\t'
    rowNumber = 1

    spotColor = True
    for row in board:
        
        # Render the top row
        for element in row:
            toAdd = boardColor[spotColor] + '\t' + colorama.Style.RESET_ALL
            printBoard += toAdd
            spotColor = not spotColor
        printBoard += '\n'

        printBoard += '      ' + str(rowNumber) + '\t'

        # Render the middle row
        for element in row:
            toAdd = boardColor[spotColor] + ' '
            toAdd += pieceColor[element[1]] + pieceDict[element[0]] # Retrieve data from the dictionaries
            toAdd += boardColor[spotColor] + '\t' + colorama.Style.RESET_ALL
            printBoard += toAdd
            spotColor = not spotColor
        printBoard += str(rowNumber) + '\n\t'
        rowNumber +=1

        # Render the bottom row
        for element in row:
            toAdd = boardColor[spotColor] + '\t' + colorama.Style.RESET_ALL
            printBoard += toAdd
            spotColor = not spotColor
        printBoard += '\n\t'
        
        spotColor = not spotColor

    printBoard += '   a\t   b\t   c\t   d\t   e\t   f\t   g\t   h\t\n\t'
    print(printBoard)

# This method will loop endlessly until it finds a viable spot to select, recursive
def findInput(whichTurn):
    global pieceColor
    a = input("Select a piece ").lower()

    letter = -1
    number = -1
    if a.find('a') != -1: letter = 0
    if a.find('b') != -1: letter = 1
    if a.find('c') != -1: letter = 2
    if a.find('d') != -1: letter = 3
    if a.find('e') != -1: letter = 4
    if a.find('f') != -1: letter = 5
    if a.find('g') != -1: letter = 6
    if a.find('h') != -1: letter = 7
    if a.find('1') != -1: number = 0
    if a.find('2') != -1: number = 1
    if a.find('3') != -1: number = 2
    if a.find('4') != -1: number = 3
    if a.find('5') != -1: number = 4
    if a.find('6') != -1: number = 5
    if a.find('7') != -1: number = 6
    if a.find('8') != -1: number = 7
    tileData = getTileData(board, (letter,number))

    if letter != -1 and number != -1 and len(a) == 2 and tileData[1] == whichTurn:

        locationInput = ()
        locationInput = findInputDestination(whichTurn, (letter, number))

        if locationInput != (-2,-2):
            return ((letter, number),locationInput)

        return findInput(whichTurn)
    elif a == "exit":
        exit()
    elif(tileData[1] != whichTurn):
        if (whichTurn == 1):
            print("Please select a " + pieceColor[1] + "White" + colorama.Style.RESET_ALL + " piece")
        if (whichTurn == 2):
            print("Please select a " + pieceColor[2] + "Black" + colorama.Style.RESET_ALL + " piece")
        return findInput(whichTurn)
    else:
        print("Invalid input, please only input 2 characters")
        return findInput(whichTurn)

# This method searchs specifically for spots to move to, recursive
def findInputDestination(whichTurn, b):
    a = input("Select a location ").lower()

    letter = -1
    number = -1
    if a.find('a') != -1: letter = 0
    if a.find('b') != -1: letter = 1
    if a.find('c') != -1: letter = 2
    if a.find('d') != -1: letter = 3
    if a.find('e') != -1: letter = 4
    if a.find('f') != -1: letter = 5
    if a.find('g') != -1: letter = 6
    if a.find('h') != -1: letter = 7
    if a.find('1') != -1: number = 0
    if a.find('2') != -1: number = 1
    if a.find('3') != -1: number = 2
    if a.find('4') != -1: number = 3
    if a.find('5') != -1: number = 4
    if a.find('6') != -1: number = 5
    if a.find('7') != -1: number = 6
    if a.find('8') != -1: number = 7
    
    if letter != -1 and number != -1 and len(a) == 2 and attemptMove(b, (letter, number)) == True:
        if checkMoveChess(b, (letter, number)):
            print("Cannot move while " + pieceColor[whichTurn] + "king" + colorama.Style.RESET_ALL + " is being threatened")
            return findInputDestination(whichTurn, b)
        return (letter, number)  
    elif a == "exit":
        exit()  
    elif attemptMove(b, (letter, number)) == False and a != 'back':
        print("Illegal move")
        return findInputDestination(whichTurn, b)
    else:
        if a == 'back':
            return (-2, -2)
        print("Invalid input, please only input 2 characters")
        return findInputDestination(whichTurn, b)

def getTileData(board, a):
    if a[0]<0 or a[0]>7 or a[1]<0 or a[1]>7:
        return (-1, -1)
    try:
        return board[a[1]][a[0]]
    except(IndexError):
        return (-1, -1)

#Check if its possible to move a piece from point a to point b
def attemptMove(a, b):
    global board

    side = getTileData(board, a)[1] #Find out which color the piece is

    if (getTileData(board, a)[0] == 1):
        #Pawn logic
        #If pawn is at its starting location
        if (side == 1 and a[1] == 1 and b[1] == 3 and a[0] == b[0] and getTileData(board, b)[1] != side):
            return True
        if (side == 2 and a[1] == 6 and b[1] == 4 and a[0] == b[0] and getTileData(board, b)[1] != side):
            return True
        #Normal movement
        if (side == 1 and b[1] == a[1]+1 and a[0] == b[0] and getTileData(board, b)[1] == 0):
            return True
        if (side == 2 and b[1] == a[1]-1 and a[0] == b[0] and getTileData(board, b)[1] == 0):
            return True
        #Move diagonal only if an enemy piece is present
        if (side == 1 and (b[0] == a[0]+1 or b[0] == a[0]-1) and b[1] == a[1]+1 and getTileData(board, b)[1] == 2):
            return True
        if (side == 2 and (b[0] == a[0]+1 or b[0] == a[0]-1) and b[1] == a[1]-1 and getTileData(board, b)[1] == 1):
            return True
    elif (getTileData(board, a)[0] == 2):
        #Tower logic
        #Vertical
        if (a[0] == b[0] and a[1] != b[1] and getTileData(board, b)[1] != side):
            for d in range(1, 9):
                if (a[1]+d == b[1]):
                    return True
                elif (a[1]-d == b[1]):
                    return True
                if (a[1] > b[1] and getTileData(board, (a[0], a[1]-d))[1] != 0):
                    return False
                elif (a[1] < b[1] and getTileData(board, (a[0], a[1]+d))[1] != 0):
                    return False
        #Horizontal
        if (a[1] == b[1] and a[0] != b[0] and getTileData(board, b)[1] != side):
            for d in range(1, 9):
                if (a[0]+d == b[0]):
                    return True
                elif (a[0]-d == b[0]):
                    return True
                if (a[0] > b[0] and getTileData(board, (a[0]-d, a[1]))[1] != 0):
                    return False
                elif (a[0] < b[0] and getTileData(board, (a[0]+d, a[1]))[1] != 0):
                    return False
        return False
    elif (getTileData(board, a)[0] == 3):
        #Horse logic
        if (getTileData(board, b)[1] != side):
            if ((a[0]+2 == b[0] and a[1]+1 == b[1]) or (a[0]+1 == b[0] and a[1]+2 == b[1]) or
                (a[0]-2 == b[0] and a[1]-1 == b[1]) or (a[0]-1 == b[0] and a[1]-2 == b[1]) or
                (a[0]+2 == b[0] and a[1]-1 == b[1]) or (a[0]+1 == b[0] and a[1]-2 == b[1]) or
                (a[0]-2 == b[0] and a[1]+1 == b[1]) or (a[0]-1 == b[0] and a[1]+2 == b[1]) ):
                return True
        return False
    elif (getTileData(board, a)[0] == 4):
        #Bishop logic
        #Find the difference between point a and b
        xdif = b[0]-a[0]
        ydif = b[1]-a[1]
        xincrement = math.copysign(1, xdif)
        yincrement = math.copysign(1, ydif)

        if (abs(xdif) == abs(ydif) and getTileData(board, b)[1] != side):
            for d in range(1, 9):
                if (a[0]+round(xincrement*d) == b[0] and a[1]+round(yincrement*d) == b[1]):
                    return True
                if getTileData(board, ( a[0]+round(d*xincrement), a[1]+round(d*yincrement) )  )[1] != 0:
                    return False
            return False
    elif (getTileData(board, a)[0] == 5):
        #Queen logic
        #Find the difference between point a and b
        xdif = b[0]-a[0]
        ydif = b[1]-a[1]
        xincrement = math.copysign(1, xdif)
        yincrement = math.copysign(1, ydif)

        if (abs(xdif) == abs(ydif) and getTileData(board, b)[1] != side):
            for d in range(1, 9):
                if (a[0]+round(xincrement*d) == b[0] and a[1]+round(yincrement*d) == b[1]):
                    return True
                if getTileData(board, ( a[0]+round(d*xincrement), a[1]+round(d*yincrement) )  )[1] != 0:
                    return False
        #Vertical
        if (a[0] == b[0] and a[1] != b[1] and getTileData(board, b)[1] != side):
            for d in range(1, 9):
                if (a[1]+d == b[1]):
                    return True
                elif (a[1]-d == b[1]):
                    return True
                if (a[1] > b[1] and getTileData(board, (a[0], a[1]-d))[1] != 0):
                    return False
                elif (a[1] < b[1] and getTileData(board, (a[0], a[1]+d))[1] != 0):
                    return False
        #Horizontal
        if (a[1] == b[1] and a[0] != b[0] and getTileData(board, b)[1] != side):
            for d in range(1, 9):
                if (a[0]+d == b[0]):
                    return True
                elif (a[0]-d == b[0]):
                    return True
                if (a[0] > b[0] and getTileData(board, (a[0]-d, a[1]))[1] != 0):
                    return False
                elif (a[0] < b[0] and getTileData(board, (a[0]+d, a[1]))[1] != 0):
                    return False
        return False
    else:
        #King logic
        #Find the difference between point a and b
        xdif = b[0]-a[0]
        ydif = b[1]-a[1]
        xincrement = math.copysign(1, xdif)
        yincrement = math.copysign(1, ydif)
        d = 1

        if (abs(xdif) == abs(ydif) and getTileData(board, b)[1] != side):
            if (a[0]+round(xincrement*d) == b[0] and a[1]+round(yincrement*d) == b[1]):
                return True
            if getTileData(board, ( a[0]+round(d*xincrement), a[1]+round(d*yincrement) )  )[1] != 0:
                return False
        #Vertical
        if (a[0] == b[0] and a[1] != b[1] and getTileData(board, b)[1] != side):
            if (a[1]+d == b[1]):
                return True
            elif (a[1]-d == b[1]):
                return True
            if (a[1] > b[1] and getTileData(board, (a[0], a[1]-d))[1] != 0):
                return False
            elif (a[1] < b[1] and getTileData(board, (a[0], a[1]+d))[1] != 0):
                return False
        #Horizontal
        if (a[1] == b[1] and a[0] != b[0] and getTileData(board, b)[1] != side):
            if (a[0]+d == b[0]):
                return True
            elif (a[0]-d == b[0]):
                return True
            if (a[0] > b[0] and getTileData(board, (a[0]-d, a[1]))[1] != 0):
                return False
            elif (a[0] < b[0] and getTileData(board, (a[0]+d, a[1]))[1] != 0):
                return False
        return False
    
    return False

#Checks if a player has entered a checkmate
def checkCheckmate(turn):
    global board
    a = 0

    for row in board:
        b = 0
        for element in row:
            if element[0]>0 and element[1] == turn:
                if checkEveryMove((b, a), turn, board) == False:
                    return False
            b+=1
        a+=1
    return True

#Tries to move a piece in every way possible and checks if the players king is still threatened
def checkEveryMove(a, turn, board):
    turnSwap = 0
    if turn == 1:
        turnSwap = 2
    if turn == 2:
        turnSwap = 1

    if getTileData(board, a)[0] == 1:
        #pawn
        if turn == 1:
            if a[1] == 1 and getTileData(board, (a[0], 3) )[1] == 0 and getTileData(board, (a[0], 2) )[1] == 0:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0], a[1]+2) )) == False:
                    return False
            if getTileData(board, (a[0], a[1]+1) )[1] == 0:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0], a[1]+1))) == False:
                    return False
            if getTileData(board, (a[0]+1, a[1]+1) )[1] == 2:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]+1, a[1]+1))) == False:
                    return False
            if getTileData(board, (a[0]-1, a[1]+1) )[1] == 2:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]-1, a[1]+1))) == False:
                    return False
        if turn == 2:
            if a[1] == 6 and getTileData(board, (a[0], 4) )[1] == 0 and getTileData(board, (a[0], 5) )[1] == 0:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0], a[1]-2) )) == False:
                    return False
            if getTileData(board, (a[0], a[1]-1) )[1] == 0:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0], a[1]-1))) == False:
                    return False
            if getTileData(board, (a[0]+1, a[1]-1) )[1] == 1:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]+1, a[1]-1))) == False:
                    return False
            if getTileData(board, (a[0]-1, a[1]-1) )[1] == 1:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]-1, a[1]-1))) == False:
                    return False
    elif getTileData(board, a)[0] == 2:
        #Tower
        for x in range(1, 10):
            if getTileData(board, (a[0]+x, a[1]))[1] == -1 or getTileData(board, (a[0]+x, a[1]))[1] == turn:
                break
            if getTileData(board, (a[0]+x, a[1]))[1] == 0 or getTileData(board, (a[0]+x, a[1]))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]+x, a[1]) )) == False:
                    return False
        for x in range(1, 10):
            if getTileData(board, (a[0]-x, a[1]))[1] == -1 or getTileData(board, (a[0]-x, a[1]))[1] == turn:
                break
            if getTileData(board, (a[0]-x, a[1]))[1] == 0 or getTileData(board, (a[0]-x, a[1]))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]-x, a[1]) )) == False:
                    return False
        for x in range(1, 10):
            if getTileData(board, (a[0], a[1]+x))[1] == -1 or getTileData(board, (a[0], a[1]+x))[1] == turn:
                break
            if getTileData(board, (a[0], a[1]+x))[1] == 0 or getTileData(board, (a[0], a[1]+x))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0], a[1]+x) )) == False:
                    return False
        for x in range(1, 10):
            if getTileData(board, (a[0], a[1]-x))[1] == -1 or getTileData(board, (a[0], a[1]-x))[1] == turn:
                break
            if getTileData(board, (a[0], a[1]-x))[1] == 0 or getTileData(board, (a[0], a[1]-x))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0], a[1]-x) )) == False:
                    return False
    elif getTileData(board, a)[0] == 3:
        #Horse
        if getTileData(board, (a[0]+2, a[1]+1))[1] == 0 or getTileData(board, (a[0]+2, a[1]+1))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0]+2, a[1]+1))) == False:
                return False
        if getTileData(board, (a[0]+2, a[1]-1))[1] == 0 or getTileData(board, (a[0]+2, a[1]-1))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0]+2, a[1]-1))) == False:
                return False
        if getTileData(board, (a[0]-2, a[1]+1))[1] == 0 or getTileData(board, (a[0]-2, a[1]+1))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0]-2, a[1]+1))) == False:
                return False
        if getTileData(board, (a[0]-2, a[1]-1))[1] == 0 or getTileData(board, (a[0]-2, a[1]-1))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0]-2, a[1]-1))) == False:
                return False
        if getTileData(board, (a[0]+1, a[1]+2))[1] == 0 or getTileData(board, (a[0]+1, a[1]+2))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0]+1, a[1]+2))) == False:
                return False
        if getTileData(board, (a[0]-1, a[1]+2))[1] == 0 or getTileData(board, (a[0]-1, a[1]+2))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0]-1, a[1]+2))) == False:
                return False
        if getTileData(board, (a[0]+1, a[1]-2))[1] == 0 or getTileData(board, (a[0]+1, a[1]-2))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0]+1, a[1]-2))) == False:
                return False
        if getTileData(board, (a[0]-1, a[1]-2))[1] == 0 or getTileData(board, (a[0]-1, a[1]-2))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0]-1, a[1]-2))) == False:
                return False
    elif getTileData(board, a)[0] == 4:
        #Bishop
        for x in range(1, 10):
            if getTileData(board, (a[0]+x, a[1]+x))[1] == -1 or getTileData(board, (a[0]+x, a[1]+x))[1] == turn:
                break
            if getTileData(board, (a[0]+x, a[1]+x))[1] == 0 or getTileData(board, (a[0]+x, a[1]+x))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]+x, a[1]+x) )) == False:
                    return False
        for x in range(1, 10):
            if getTileData(board, (a[0]-x, a[1]+x))[1] == -1 or getTileData(board, (a[0]-x, a[1]+x))[1] == turn:
                break
            if getTileData(board, (a[0]-x, a[1]+x))[1] == 0 or getTileData(board, (a[0]-x, a[1]+x))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]-x, a[1]+x) )) == False:
                    return False
        for x in range(1, 10):
            if getTileData(board, (a[0]+x, a[1]-x))[1] == -1 or getTileData(board, (a[0]+x, a[1]-x))[1] == turn:
                break
            if getTileData(board, (a[0]+x, a[1]-x))[1] == 0 or getTileData(board, (a[0]+x, a[1]-x))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]+x, a[1]-x) )) == False:
                    return False
        for x in range(1, 10):
            if getTileData(board, (a[0]-x, a[1]-x))[1] == -1 or getTileData(board, (a[0]-x, a[1]-x))[1] == turn:
                break
            if getTileData(board, (a[0]-x, a[1]-x))[1] == 0 or getTileData(board, (a[0]-x, a[1]-x))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]-x, a[1]-x) )) == False:
                    return False
    elif getTileData(board, a)[0] == 5:
        #Queen
        for x in range(1, 10):
            if getTileData(board, (a[0]+x, a[1]))[1] == -1 or getTileData(board, (a[0]+x, a[1]))[1] == turn:
                break
            if getTileData(board, (a[0]+x, a[1]))[1] == 0 or getTileData(board, (a[0]+x, a[1]))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]+x, a[1]) )) == False:
                    return False
        for x in range(1, 10):
            if getTileData(board, (a[0]-x, a[1]))[1] == -1 or getTileData(board, (a[0]-x, a[1]))[1] == turn:
                break
            if getTileData(board, (a[0]-x, a[1]))[1] == 0 or getTileData(board, (a[0]-x, a[1]))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]-x, a[1]) )) == False:
                    return False
        for x in range(1, 10):
            if getTileData(board, (a[0], a[1]+x))[1] == -1 or getTileData(board, (a[0], a[1]+x))[1] == turn:
                break
            if getTileData(board, (a[0], a[1]+x))[1] == 0 or getTileData(board, (a[0], a[1]+x))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0], a[1]+x) )) == False:
                    return False
        for x in range(1, 10):
            if getTileData(board, (a[0], a[1]-x))[1] == -1 or getTileData(board, (a[0], a[1]-x))[1] == turn:
                break
            if getTileData(board, (a[0], a[1]-x))[1] == 0 or getTileData(board, (a[0], a[1]-x))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0], a[1]-x) )) == False:
                    return False
        for x in range(1, 10):
            if getTileData(board, (a[0]+x, a[1]+x))[1] == -1 or getTileData(board, (a[0]+x, a[1]+x))[1] == turn:
                break
            if getTileData(board, (a[0]+x, a[1]+x))[1] == 0 or getTileData(board, (a[0]+x, a[1]+x))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]+x, a[1]+x) )) == False:
                    return False
        for x in range(1, 10):
            if getTileData(board, (a[0]-x, a[1]+x))[1] == -1 or getTileData(board, (a[0]-x, a[1]+x))[1] == turn:
                break
            if getTileData(board, (a[0]-x, a[1]+x))[1] == 0 or getTileData(board, (a[0]-x, a[1]+x))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]-x, a[1]+x) )) == False:
                    return False
        for x in range(1, 10):
            if getTileData(board, (a[0]+x, a[1]-x))[1] == -1 or getTileData(board, (a[0]+x, a[1]-x))[1] == turn:
                break
            if getTileData(board, (a[0]+x, a[1]-x))[1] == 0 or getTileData(board, (a[0]+x, a[1]-x))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]+x, a[1]-x) )) == False:
                    return False
        for x in range(1, 10):
            if getTileData(board, (a[0]-x, a[1]-x))[1] == -1 or getTileData(board, (a[0]-x, a[1]-x))[1] == turn:
                break
            if getTileData(board, (a[0]-x, a[1]-x))[1] == 0 or getTileData(board, (a[0]-x, a[1]-x))[1] == turnSwap:
                if checkChess(turnSwap, createBoardCopy(board, a, (a[0]-x, a[1]-x) )) == False:
                    return False
    else:
        x = 1
        if getTileData(board, (a[0]+x, a[1]))[1] == 0 or getTileData(board, (a[0]+x, a[1]))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0]+x, a[1]) )) == False:
                return False
        if getTileData(board, (a[0]-x, a[1]))[1] == 0 or getTileData(board, (a[0]-x, a[1]))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0]-x, a[1]) )) == False:
                return False
        if getTileData(board, (a[0], a[1]+x))[1] == 0 or getTileData(board, (a[0], a[1]+x))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0], a[1]+x) )) == False:
                return False
        if getTileData(board, (a[0], a[1]-x))[1] == 0 or getTileData(board, (a[0], a[1]-x))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0], a[1]-x) )) == False:
                return False
        if getTileData(board, (a[0]+x, a[1]+x))[1] == 0 or getTileData(board, (a[0]+x, a[1]+x))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0]+x, a[1]+x) )) == False:
                return False
        if getTileData(board, (a[0]-x, a[1]+x))[1] == 0 or getTileData(board, (a[0]-x, a[1]+x))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0]-x, a[1]+x) )) == False:
                return False
        if getTileData(board, (a[0]+x, a[1]-x))[1] == 0 or getTileData(board, (a[0]+x, a[1]-x))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0]+x, a[1]-x) )) == False:
                return False
        if getTileData(board, (a[0]-x, a[1]-x))[1] == 0 or getTileData(board, (a[0]-x, a[1]-x))[1] == turnSwap:
            if checkChess(turnSwap, createBoardCopy(board, a, (a[0]-x, a[1]-x) )) == False:
                return False
    return True

def createBoardCopy(board, a, b):
    #print(a + b)
    if b[0]>7 or b[1]>7 or b[0]<0 or b[1]<0:
        return board
    boardCopy = copy.deepcopy(board)
    boardCopy[b[1]][b[0]] = boardCopy[a[1]][a[0]]
    boardCopy[a[1]][a[0]] = (0, 0)
    return boardCopy

#Checks if the move leaves your king open
def checkMoveChess(a, b):
    global turnState
    global board
    turnSwap = 0
    if turnState == 1:
        turnSwap = 2
    if turnState == 2:
        turnSwap = 1
    boardCopy = copy.deepcopy(board)
    boardCopy[b[1]][b[0]] = boardCopy[a[1]][a[0]]
    boardCopy[a[1]][a[0]] = (0, 0)
    return checkChess(turnSwap, boardCopy)

#Checks if either players king is threatened
def checkChess(turn, board):
    #used to contruct the turple that we will give to checkPiecePath
    a = 0 

    for row in board:
        b = 0
        for element in row:
            if element[0]>0 and element[1] == turn:
                if checkPiecePath( (b, a), turn, board):
                    return True
            b+=1
        a+=1
    return False

#Checks if a piece is threatening the opposing king
def checkPiecePath(a, turnState, board):

    otherKing = () 
    #Saves a turple in a variable so we know what to look for
    if turnState == 1:
        otherKing = (6,2)
    if turnState == 2:
        otherKing = (6,1)

    if getTileData(board, a)[0] != 0:
        if getTileData(board, a)[0] == 1:
            #check if a pawn is threatening the king
            if turnState == 1:
                #white side
                if (getTileData(board, (a[0]+1, a[1]+1)) == otherKing or getTileData(board, (a[0]-1, a[1]+1)) == otherKing):
                    return True
                return False
            if turnState == 2:
                #black side
                if (getTileData(board, (a[0]+1, a[1]-1)) == otherKing or getTileData(board, (a[0]-1, a[1]-1)) == otherKing):
                    return True
                return False
        elif getTileData(board, a)[0] == 2:
            #check if a tower is threatening the king
            for x in range(1, 10):
                if (getTileData(board, (a[0]+x ,a[1])) == otherKing):
                    return True
                if (getTileData(board, (a[0]+x ,a[1]))[1] != 0 or getTileData(board, (a[0]+x ,a[1])) == (-1, -1)):
                    break
            for x in range(1, 10):
                if (getTileData(board, (a[0]-x ,a[1])) == otherKing):
                    return True
                if (getTileData(board, (a[0]-x ,a[1]))[1] != 0 or getTileData(board, (a[0]-x ,a[1])) == (-1, -1)):
                    break
            for x in range(1, 10):
                if (getTileData(board, (a[0] ,a[1]+x)) == otherKing):
                    return True
                if (getTileData(board, (a[0] ,a[1]+x))[1] != 0 or getTileData(board, (a[0] ,a[1]+x)) == (-1, -1)):
                    break
            for x in range(1, 10):
                if (getTileData(board, (a[0] ,a[1]-x)) == otherKing):
                    return True
                if (getTileData(board, (a[0] ,a[1]-x))[1] != 0 or getTileData(board, (a[0] ,a[1]-x)) == (-1, -1)):
                    break
            return False
        elif getTileData(board, a)[0] == 3:
            #check if a horse is threatening the king
            if (getTileData(board, ( a[0]+2, a[1]+1)) == otherKing or getTileData(board, ( a[0]+2, a[1]-1)) == otherKing
                or getTileData(board, ( a[0]-2, a[1]+1)) == otherKing or getTileData(board, ( a[0]-2, a[1]-1)) == otherKing
                or getTileData(board, ( a[0]+1, a[1]+2)) == otherKing or getTileData(board, ( a[0]+1, a[1]-2)) == otherKing
                or getTileData(board, ( a[0]-1, a[1]+2)) == otherKing or getTileData(board, ( a[0]-1, a[1]-2)) == otherKing):
                return True
            return False
        elif getTileData(board, a)[0] == 4:
            #check if a bishop is threatening the king
            for x in range(1, 10):
                if (getTileData(board, ( a[0]+x, a[1]+x)) == otherKing):
                    return True
                if (getTileData(board, (a[0]+x ,a[1]+x))[1] != 0 or getTileData(board, (a[0]+x ,a[1]+x)) == (-1, -1)):
                    break
            for x in range(1, 10):
                if (getTileData(board, ( a[0]-x, a[1]+x)) == otherKing):
                    return True
                if (getTileData(board, (a[0]-x ,a[1]+x))[1] != 0 or getTileData(board, (a[0]-x ,a[1]+x)) == (-1, -1)):
                    break
            for x in range(1, 10):
                if (getTileData(board, ( a[0]+x, a[1]-x)) == otherKing):
                    return True
                if (getTileData(board, (a[0]+x ,a[1]-x))[1] != 0 or getTileData(board, (a[0]+x ,a[1]-x)) == (-1, -1)):
                    break
            for x in range(1, 10):
                if (getTileData(board, ( a[0]-x, a[1]-x)) == otherKing):
                    return True
                if (getTileData(board, (a[0]-x ,a[1]-x))[1] != 0 or getTileData(board, (a[0]-x ,a[1]-x)) == (-1, -1)):
                    break
            return False
        elif getTileData(board, a)[0] == 5:
            #Check if the queen is threatening the king
            for x in range(1, 10):
                if (getTileData(board, (a[0]+x ,a[1])) == otherKing):
                    return True
                if (getTileData(board, (a[0]+x ,a[1]))[1] != 0 or getTileData(board, (a[0]+x ,a[1])) == (-1, -1)):
                    break
            for x in range(1, 10):
                if (getTileData(board, (a[0]-x ,a[1])) == otherKing):
                    return True
                if (getTileData(board, (a[0]-x ,a[1]))[1] != 0 or getTileData(board, (a[0]-x ,a[1])) == (-1, -1)):
                    break
            for x in range(1, 10):
                if (getTileData(board, (a[0] ,a[1]+x)) == otherKing):
                    return True
                if (getTileData(board, (a[0] ,a[1]+x))[1] != 0 or getTileData(board, (a[0] ,a[1]+x)) == (-1, -1)):
                    break
            for x in range(1, 10):
                if (getTileData(board, (a[0] ,a[1]-x)) == otherKing):
                    return True
                if (getTileData(board, (a[0] ,a[1]-x))[1] != 0 or getTileData(board, (a[0] ,a[1]-x)) == (-1, -1)):
                    break
            for x in range(1, 10):
                if (getTileData(board, ( a[0]+x, a[1]+x)) == otherKing):
                    return True
                if (getTileData(board, (a[0]+x ,a[1]+x))[1] != 0 or getTileData(board, (a[0]+x ,a[1]+x)) == (-1, -1)):
                    break
            for x in range(1, 10):
                if (getTileData(board, ( a[0]-x, a[1]+x)) == otherKing):
                    return True
                if (getTileData(board, (a[0]-x ,a[1]+x))[1] != 0 or getTileData(board, (a[0]-x ,a[1]+x)) == (-1, -1)):
                    break
            for x in range(1, 10):
                if (getTileData(board, ( a[0]+x, a[1]-x)) == otherKing):
                    return True
                if (getTileData(board, (a[0]+x ,a[1]-x))[1] != 0 or getTileData(board, (a[0]+x ,a[1]-x)) == (-1, -1)):
                    break
            for x in range(1, 10):
                if (getTileData(board, ( a[0]-x, a[1]-x)) == otherKing):
                    return True
                if (getTileData(board, (a[0]-x ,a[1]-x))[1] != 0 or getTileData(board, (a[0]-x ,a[1]-x)) == (-1, -1)):
                    break
            return False
        else:
            #Check if the king is threatening the other king
            if (getTileData(board, ( a[0]+1, a[1])) == otherKing or getTileData(board, ( a[0]+1, a[1]+1)) == otherKing
             or getTileData(board, ( a[0], a[1]+1)) == otherKing or getTileData(board, ( a[0]-1, a[1]+1)) == otherKing
             or getTileData(board, ( a[0]-1, a[1])) == otherKing or getTileData(board, ( a[0]-1, a[1]-1)) == otherKing
             or getTileData(board, ( a[0], a[1]-1)) == otherKing or getTileData(board, ( a[0]+1, a[1]-1)) == otherKing):
                return True
            return False
    return False

def mainLoop():
    global pieceColor
    global board
    global turnState

    #we check for a checkmate at the start of a turn
    if checkCheckmate(turnState):
        if turnState == 1:
            if checkChess(2, board) == False:
                print("\tStalemate")
            print("\t" + "Checkmate! " + pieceColor[2] + "black" + colorama.Style.RESET_ALL + " wins!")
            return
        if turnState == 2:
            if checkChess(1, board) == False:
                print("\tStalemate")
            print("\t" + "Checkmate! " + pieceColor[1] + "white" + colorama.Style.RESET_ALL + " wins!")
            return

    if turnState == 1:
        print("\t" + pieceColor[turnState] + "Whites" + colorama.Style.RESET_ALL + " turn")
    else:
        print("\t" + pieceColor[turnState] + "Blacks" + colorama.Style.RESET_ALL + " turn")

    selectInput = ((),())
    selectInput = findInput(turnState)

    foundPiece = board[selectInput[0][1]][selectInput[0][0]]

    board[selectInput[0][1]][selectInput[0][0]] = (0, 0)

    board[selectInput[1][1]][selectInput[1][0]] = foundPiece

    printBoard()

    if checkChess(turnState, board):
        print("\tchess")

    if turnState == 1:
        turnState = 2
    else:
        turnState = 1

    mainLoop()

# =============                          |=============|                          =============
# =======================================| MAIN EVENTS |=======================================
# =============                          |=============|                          =============

turnState = 1

board = resetBoard()
printBoard()

print("For input, please only type 2 characters eg: 1a, d5 etc.")
mainLoop()