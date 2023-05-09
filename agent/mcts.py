import copy
import math
import time
import random

from referee.game import HexDir
from agent.gameboard import *


class Node:
    def __init__(self, board: GameBoard, parent, action):

        self.state = board
        self.isTerminal = self.isFullyExpanded = self.state.getWinner()[0]
        self.parent = parent
        self.playouts = 0
        self.score = 0
        self.children = {}
        self.move = action

class MCTS():

    def search(self, initialState) -> Action:
        self.root = Node(initialState, None, None)
        print(f"Board State (Start of MCTS): {self.root.state.board}")

        for iteration in range(3):
            node = self.select(self.root)
            # print(node)

            score = self.playout(node)
            self.backpropagate(node, score)

        bestMove = self.getBestMove(self.root, 0)
        print(f"bestMove: {bestMove}")

        try:
            return self.getBestMoves(self.root, 0)

        except:
            pass

        # return SpawnAction(HexPos(0,0))


    ### NODE SELECTION ###
    def select(self, node: Node) -> Node:
        while not node.state.getWinner()[0]:  # while there's no winner
            if node.isFullyExpanded:
                # print(f"NODE IS FULLY EXPANDED")
                node = self.getBestMove(node, 2)  # asdf why is this 2
            else:
                self.expand(node)
                # return self.expand(node)  # why is there even a return here? doesn't this cut the loop early?

        return node
        # if not node.isFullyExpanded and not node.isTerminal:
        #     self.expand(node)
        #
        # print(f"NODE IS FULLY EXPANDED")
        # bestNode = self.getBestMoves(node, 2)
        #
        # return bestNode

    def expand(self, node: Node): #take player color into account
        # states = node.state.generateMoves()


        # get all the possible states of next player
        states = self.getPossibleActions(node)  # GameBoards
        # print(f"numStates={len(states)}, numChildren={len(node.children)}")

        for state in states:
            # print(f"\tnumChildren={len(node.children)}")
            # print(f"\t(expand) currState={state}")
            expandedState = state[0]
            boardMove = state[1]
            # print(f"\t(expand) expandedState={expandedState}")

            if expandedState not in node.children:  # adds nodes to children
                new_node = Node(state[0], node, state[1])
                node.children[state[0]] = new_node

                if len(states) == len(node.children):
                    node.isFullyExpanded = True

                return new_node  # why do we return one of the children nodes? if the goal of this function is to expand on the current node?

        print("SOMETHING WENT HORRIBLY WRONG IF THIS PRINTED")

    # Returns an Array of possible Actions
    def getPossibleActions(self, node: Node) -> [GameBoard]:
        moves = []  # GameBoards

        nextPlayer = node.state.getNextPlayer()

        # for spread in node.state.spreadOptions(nextPlayer):
        #     newBoard = copy.deepcopy(node.state) # use deepcopy instead of copy or else all the boards will be the same
        #     newBoard.updateBoard(nextPlayer, SpreadAction(spread[0], spread[2]))
        #     moves.append((newBoard, SpreadAction(spread[0], spread[2])))

        for spawn in node.state.spawnOptions():  # creates future boards
            newBoard = copy.deepcopy(node.state)  # use deepcopy instead of copy or else all the boards will be the same
            newBoard.updateBoard(nextPlayer, SpawnAction(spawn))
            moves.append((newBoard, SpawnAction(spawn)))

        ## TESTING
        # print(f"LastNode State: {node.state.board}")
        #
        # # printing moves and their corresponding states test
        # for i in range(len(moves)):
        #     print(f"[{i}] Move: {moves[i][1]}, Board: \n{moves[i][0].board}")

        return moves

    def getBestMove(self, node: Node, explorationConstant):

        bestScore = float('-inf')
        bestMoves = []

        children = node.children.values()

        if node.playouts == 0:
            return random.choice(list(children))

        for childNode in children:
            currentPlayer = 0  # !!!!!!!!!!!!!!!!!!!!!!!!!!
            # print(childNode.board)
            if childNode.state.getNextPlayer() == self.root.state.getNextPlayer():
                currentPlayer = 1
            elif childNode.state.getNextPlayer() != self.root.state.getNextPlayer():
                currentPlayer = -1

            # if (childNode.playouts == 0):
            #     return childNode

            meanVisits = currentPlayer * childNode.score / (childNode.playouts+1)
            # print(f"playouts={node.playouts}, childnode.playouts={childNode.playouts+1}")
            root = math.log((node.playouts+1) / (childNode.playouts+1))  # asdfasdfasdf +1

            UCB1 = meanVisits + explorationConstant * math.sqrt(root)

            if UCB1 > bestScore:
                bestScore = UCB1
                bestMoves = [childNode]

            elif UCB1 == bestScore:
                bestMoves.append(childNode)

        print(f"numBestMoves={len(bestMoves)}")
        return random.choice(bestMoves)


    ### PLAYOUT ###
    def playout(self, node: Node):

        newBoard = node.state
        while not newBoard.getWinner()[0]:
            try:
                newBoard = random.choice(self.getPossibleActions(node))
            except:
                return 0

        if newBoard.getWinner()[1] == self.root.state.getNextPlayer():
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