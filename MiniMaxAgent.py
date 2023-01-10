from PawnEnvironment import *
from MiniMaxPawn import *

class miniMaxAgent(player):
    def getAction(self, moveList):
        ms1 = miniMax(self.team)
        ms1.makeGraph(self.boardState) # make graph to traverse

        root = [n for n in ms1.graph.nodes if n.boardStr() == self.boardState.boardStr()] # get node = to current board

        optimalMove = ms1.traverseGraph(root[0]) # do miniMax
        optimalMoveStr = optimalMove[0].boardStr() # turn graph node into str
        for i in range(len(moveList)):
            tempBoard = deepcopy(self.boardState)
            tempBoard.move(moveList[i])
            if tempBoard.boardStr() == optimalMoveStr:
                return i # return move that will get to optimal next board state

player_1 = miniMaxAgent("w")
player_2 = humanAgent("b") # humanAgent("b") to play against the miniMax agent

game = doGame(player_1, player_2)

print(game + " wins!")
