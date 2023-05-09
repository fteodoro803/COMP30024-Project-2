import copy
import math
import time
import random

from referee.game import HexDir
from agent.gameboard import *


class Node:
    def __init__(self, board: GameBoard, parent, action):

        self.board = board
        self.isTerminal = self.isFullyExpanded = self.board.getWinner()[0]
        self.parent = parent
        self.playouts = 0
        self.score = 0
        self.children = {}
        self.move = action

class MCTS():

    def selectMove(self, initialState):
        self.root = Node(initialState, None, None)

        for iteration in range(1000):
            node = self.select(self.root)
            score = self.playout(node)
            self.backpropagate(node, score)

        try:
            return self.getBestMoves(self.root, 0)

        except:
            pass

    def select(self, node):
        while not node.board.getWinner()[0]:
            if node.isFullyExpanded:
                node = self.getBestMoves(node, 2)
            else:
                return self.expand(node)

        return node

    def expand(self, node: Node): #take player color into account
        # states = node.state.generateMoves()


        # get all the possible states of next player
        states = self.getNextMoves(node)  # GameBoards

        for state in states:
            if state.board not in node.children:
                new_node = Node(state[0], node, state[1])
                node.children[state[0]] = new_node

                if len(states) == len(node.children):
                    node.isFullyExpanded = True

                return new_node

    def playout(self, node: Node):

        newBoard = node.board
        while not newBoard.getWinner()[0]:
            try:
                newBoard = random.choice(self.getNextMoves(node))
            except:
                return 0

        if newBoard.getWinner()[1] == self.root.board.getNextPlayer():
            return 1
        elif newBoard.getWinner()[1] is None:
            return 0.5
        else:
            return -1


    def backpropagate(self, node, score):
        while node is not None:
            node.playouts += 1
            node.score += score
            node = node.parent

    def getBestMoves(self, node, explorationConstant):

        bestScore = float('-inf')
        bestMoves = []

        for childNode in node.children.values():
            currentPlayer = 0  # !!!!!!!!!!!!!!!!!!!!!!!!!!
            if childNode.board.getNextPlayer() == self.root.board.getNextPlayer():
                currentPlayer = 1
            elif childNode.board.getNextPlayer() != self.root.board.getNextPlayer():
                currentPlayer = -1

            UCB1 = currentPlayer * childNode.score / childNode.playouts + \
                        explorationConstant * math.sqrt(math.log(node.playouts / childNode.playouts))

            if UCB1 > bestScore:
                bestScore = UCB1
                bestMoves = [childNode]

            elif UCB1 == bestScore:
                bestMoves.append(childNode)

        return random.choice(bestMoves)

    def getNextMoves(self, node: Node):
        moves = []  # GameBoards

        nextPlayer = node.board.getNextPlayer()

        for spread in node.board.spreadOptions(nextPlayer):
            newBoard = copy.copy(node.board)
            newBoard.updateBoard(nextPlayer, SpreadAction(spread[0], spread[2]))
            moves.append((newBoard, SpreadAction(spread[0], spread[2])))

        for spawn in node.board.spawnOptions():  # creates future boards
            newBoard = copy.copy(node.board)
            newBoard.updateBoard(nextPlayer, SpawnAction(spawn))
            moves.append((newBoard, SpawnAction(spawn)))

        return moves