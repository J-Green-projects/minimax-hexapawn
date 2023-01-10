from PawnEnvironment import *
import networkx as nx
from copy import *
import matplotlib.pyplot as plt

class miniMax():
    def __init__(self, team):
        self.team = team # must be either "w" or "b", opponent will be opposite
        self.opponent = [team for team in ["b", "w"] if team != self.team][0]
        self.graph = None

    def makeGraph(self, board):
        self.graph = nx.DiGraph(directed=True) # DiGraph for successors attribute when searching
        firstNode = deepcopy(board) # copy to prevent alteration of original board object
        self.graph.add_node(firstNode, endState = 0)

        pMove = board.generateMoves(self.team) # get moves, then get resultant boardstates
        for i in range(len(pMove)):
            bCopy = deepcopy(board)
            bCopy.move(pMove[i])
            if bCopy.getWinner(self.team):
                isWinner = 1000
            elif bCopy.getWinner(self.opponent):
                isWinner = -1000
            else:
                isWinner = 0
            node = bCopy
            self.graph.add_node(node, endState=isWinner)
            self.graph.add_edge(firstNode, node)

        for i in range(6): # must be even to ensure agent plays the final move, 8 is slow but provides best results
            teams = [self.opponent, self.team]
            currentTeam = i % 2 
            self.recursiveGraph(teams[currentTeam]) # this function requires a frontier > 1 node

    def recursiveGraph(self, team):
        '''minimax, str -> None
        plays an extra turn for every node at the frontier of the graph for a given team'''
        graph = self.graph
        newNodes = [x for x in graph.nodes() if graph.out_degree(x)==0 and graph.in_degree(x)==1 and graph.nodes[x]['endState'] == 0]
        
        for i in range(len(newNodes)): # newNodes are the graph's frontier
            pMove = newNodes[i].generateMoves(team) # same as first segment of makeGraph method
            for j in range(len(pMove)):
                bCopy = deepcopy(newNodes[i]) 
                bCopy.move(pMove[j]) 
                node = bCopy
                if bCopy.getWinner(team):
                    if team == self.team: # unlike makeGraph, team played may not be own team
                        isWinner = 1000
                    else: 
                        isWinner = -1000
                else:
                    isWinner = 0
                if node not in self.graph.nodes:
                    self.graph.add_node(node, endState=isWinner) # boardState + reward
                    self.graph.add_edge(newNodes[i], node)
                else:
                    self.graph.add_edge(newNodes[i], graph.nodes[node])

    def maxAlpha(self, n, alpha, beta):
        '''minimax, node -> tuple(boardState, int)
        selects the best possible outcome for the agent. If this doesn't end the game,
        go to the next turn with min (ie. the opponent) playing. Prunes moves that shouldn't occur.'''
        maxValue = float('-inf')
        if self.graph.nodes[n]['endState'] in {-1000, 1000}: # if going to win, report this. Written to accomodate future evaluation of non-terminal nodes
            return self.graph.nodes[n]['endState']
        for i in self.graph.successors(n):
            value = self.minAlpha(i, alpha, beta) # return min of next turn, which is max of turn after
            maxValue = max(maxValue, value) # if minValue from above higher than maxValue, return it
        
            if maxValue >= beta: # if move better/equal opponent's worst: return
                return maxValue
            if maxValue > alpha: # if move better than previous best, new best
                alpha = maxValue
        
        return maxValue

    def minAlpha(self, n, alpha, beta):
        '''minimax, node -> tuple(boardState, int)
        selects the worst possible outcome for the agent. If this doesn't end the game, 
        go to next turn with max (ie. agent) playing. Prunes moves that shouldn't occur.'''
        minValue = float('inf') # will be replaced by first actual integer, ie any endstate
        if self.graph.nodes[n]['endState'] in {-1000,1000}: # if going to lose, report this, Written to accomodate future evaluation of non-terminal nodes 
            return self.graph.nodes[n]['endState']
        for i in self.graph.successors(n):
            value = self.maxAlpha(i, alpha, beta) # return max of next turn, which is min of turn after
            minValue = min(minValue, value) # if maxValue from above lower than minvalue, return it
        
        if minValue <= alpha: # if move worse agent's worst, keep going
            return minValue

        if minValue < beta:  # if move worse for alpha than opponent's best, beta has new best
            beta = minValue
        
        return minValue
    
    def traverseGraph(self, board):
        '''minimax, boardState -> (best next board state, int)
        container for the whole minimax operation. Returns a boardstate
        that will need to be parsed with the boardStr operation'''
        bestValue = float('-inf') # worst possible score for agent
        bestState = None
        for successor in self.graph.successors(board):
            alpha = float('-inf') # worst possible score for alpha
            beta = float ('inf') # worst possible score for beta
            value = self.minAlpha(successor, alpha, beta) 
            if value > bestValue:
                bestState = successor
                bestValue = value
        return (bestState, value)