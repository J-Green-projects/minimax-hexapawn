import numpy as np
from random import randint

class piece():
    def __init__(self, col, row, team):
        self.col = col
        self.row = row
        self.team = team


class board():
    def __init__(self, rows=4, cols=4, pieces = []):
        self.rows = rows
        self.cols = cols
        self.pieces = pieces
        
    def populate(self):
        '''board -> None
        places pieces on every column at the first and last row of the board.'''
        self.pieces.clear() # full reset in case of any earlier calls
        for i in range(self.cols):
            self.pieces.append(piece(i, 0, "w")) # white starts at the top of the board
            self.pieces.append(piece(i, self.rows-1, "b")) # black starts at the bottom
    
    def isOccupied(self, col, row): 
        '''board, int, int -> bool, str/None
        returns whether or not a piece is at target location, and if so what team it belongs to.'''

        for i in range(len(self.pieces)): # locate each piece and match it with target col/row
            if self.pieces[i].col == col and self.pieces[i].row == row:
                return True, self.pieces[i].team

        return False, None # if no pieces in target square, it isn't occupied

    def getOccupant(self, col, row):
        '''board, int, int -> int
        Finds the index of the piece occupying the target row and column.
        Will return None if no piece exists, ensure that the piece exists by calling 
        board.isOccupied(col, row) first.'''
        for i in range(len(self.pieces)):
            if self.pieces[i].col == col and self.pieces[i].row == row:
                return i

    def legalMove(self, piece):
        '''board, piece -> list of lists of tuples
        Returns every legal move a piece could make. Moves are in the form of:
        [(starting col, starting row), (target col, target row)]'''
        moves = []
        if piece.team == "w":
            occupied, team = self.isOccupied(piece.col,piece.row+1)
            if occupied == False and piece.row < self.rows-1: # move forward if not blocked
                moves.append([(piece.col, piece.row), (piece.col, piece.row+1)])
            occupied, team = self.isOccupied(piece.col+1, piece.row+1)
            if occupied == True and piece.team != team: # take if occupied by opponent
                moves.append([(piece.col, piece.row), (piece.col+1, piece.row+1)])
            occupied, team = self.isOccupied(piece.col-1, piece.row+1)
            if occupied == True and piece.team != team: # take if occupied by opponent
                moves.append([(piece.col, piece.row), (piece.col-1, piece.row+1)])
        if piece.team == "b": # as "w", but going in the opposite direction
            occupied, team = self.isOccupied(piece.col,piece.row-1)
            if occupied == False and piece.row > 0:
                moves.append([(piece.col, piece.row), (piece.col, piece.row-1)])
            occupied, team = self.isOccupied(piece.col+1, piece.row-1)
            if occupied == True and piece.team != team:
                moves.append([(piece.col, piece.row), (piece.col+1, piece.row-1)])
            occupied, team = self.isOccupied(piece.col-1, piece.row-1)
            if occupied == True and piece.team != team:
                moves.append([(piece.col, piece.row), (piece.col-1, piece.row-1)])
        return moves

    def generateMoves(self, team):
        '''board, str -> list of lists of tuples
        returns a list of all valid moves in [(col, row) -> (col, row)] format'''
        teamMoves = []
        for i in range(len(self.pieces)):
            if self.pieces[i].team == team:
                moves = self.legalMove(self.pieces[i])
                teamMoves.extend(moves)

        return teamMoves

    def move(self, move):
        '''board, list of tuples -> None
        moves a piece based on an input move in [(col, row) -> (col, row)] format'''
        if move[0][0] != move[1][0]:
            targetPiece = self.getOccupant(move[1][0],move[1][1])
            self.pieces.remove(self.pieces[targetPiece])

        movingPiece = self.getOccupant(move[0][0],move[0][1])
        self.pieces[movingPiece].col, self.pieces[movingPiece].row = move[1][0], move[1][1]
             
    def getWinner(self, team):
        '''board, str -> bool
        if input team (str "w" or "b") has reached the other end of the board, they win.
        Note that running out of pieces/valid moves is handled elsewhere.'''
        if team == "w":
            for i in range(len(self.pieces)):
                if self.pieces[i].row == self.rows-1 and self.pieces[i].team == "w":
                    return True # pieces.row starts at 0, board.rows starts at 1
                elif len(self.generateMoves("b")) == 0: # if b can't move, w wins.
                    return True
        else:
            for i in range(len(self.pieces)):
                if self.pieces[i].row == 0 and self.pieces[i].team == "b":
                    return True
                elif len(self.generateMoves("w")) == 0: # if w can't move, b wins.
                    return True
        return False

    def boardStr(self):
        '''board -> str
        returns a boardState encoded in str format for comparisons with board states in graph nodes'''
        boardStr = ""
        for i in range(self.cols):
            for j in range(self.rows):
                occupant = self.isOccupied(i, j)
                if occupant[1] == None:
                    boardStr = boardStr + "_"
                else:
                    boardStr = boardStr + occupant[1] 

        return boardStr
                


class player():
    '''basis for all possible agents. Percept input, prior knowledge of team, nothing else.
    The 'getAction' method is required for all subclasses. '''
    def __init__(self, team, boardState=None):
        self.team = team
    def getBoardState(self, board): # get percepts
        self.boardState = board
    
class naiveAgent(player):
    '''agent that plays moves at random, believing all to be of equal value.'''
    def getAction(self, moveList):
        return randint(0, len(moveList)-1)

class humanAgent(player):
    '''not actually an agent, but a human player, choosing moves based on human input.'''
    def getAction(self, moveList):
        for i in range(len(moveList)):
            print(str(i+1) + ": " + str(moveList[i]))
        action = None
        while action == None:
            entry = input("Enter a number corresponding to a move\n(start col, row) -> (end col, row): ")
            if entry.isdigit():
                entry = int(entry)
                if entry <= len(moveList) and entry >= 1:
                    action = entry-1
                else:
                    print("Please enter a digit within the range " + str(1) + "-" + str(len(moveList)))
            else:
                print("You did not enter a number corresponding to a move. Please try again. Remember: intergers only.")
        return action

def displayBoard(board):
    '''board -> Array
    Returns an an array to be printed. Pieces are represented by 'w' or 'b', empty spaces by are 
    represented by ' '. This array visualizes the current board state.'''
    display = np.full((board.rows, board.cols)," ")
    for i in range(len(board.pieces)):
        display[board.pieces[i].row][board.pieces[i].col] = board.pieces[i].team
    return display

def doGame(player_1, player_2):
    winner = None
    b = board()
    b.populate()
    print(displayBoard(b))

    players = [player_1, player_2]
    playerText = ["white", "black"]

    i = 0
    while winner == None:
        currentPlayer = i%2
        nextPlayer = 1 - currentPlayer
        print(playerText[currentPlayer] + " to move\n--------------")
        pMove = b.generateMoves(players[currentPlayer].team)
        players[currentPlayer].getBoardState(b)
        choice = players[currentPlayer].getAction(pMove)
        b.move(pMove[choice])
        print(displayBoard(b))
        if b.getWinner(players[currentPlayer].team):
            winner = playerText[currentPlayer]
        i+=1

    return winner


#player_1 = naiveAgent("w")
#player_2 = naiveAgent("b")

#game = doGame(player_1, player_2)
        
#print(game + " wins")


