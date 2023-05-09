import copy
import datetime
import math
import time
import random

from agent.gameboard import *

class Node:
    def __init__(self, state: GameBoard, parent=None):

        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def update(self, result):
        self.visits += 1
        self.wins += result

    def addChild(self, childState):
        childNode = Node(childState, self)
        self.children.append(childNode)
        return childNode

    def isFullyExpanded(self):
        return len(self.children) == len(self.state.getLegalMoves())

    def getBestChild(self):
        choiceWeights = []
        constant = 2

        for child in self.children:
            choiceWeights.append((child.wins / child.visits) + constant * math.sqrt((2 * math.log(self.visits) / child.visits)))

        return self.children[choiceWeights.index(max(choiceWeights))]

    def rollout(self):  # random moves to get to the point
        currentState = self.state
        isTerminal = currentState.getWinner()[0]
        winner = None

        # does Simulations while board's State is not Terminal
        while not isTerminal:
            possible_moves = currentState.getLegalMoves()
            randomChoice = random.choice(possible_moves)

            # for choice in possible_moves:    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! heuristic???
            #     if choice.power > randomChoice.power:
            #         randomChoice = choice

            currentState.updateBoard(randomChoice[0], randomChoice[1])
            isTerminal = randomChoice[0]
            winner = randomChoice[1]

        if winner == True:
            return 1
        elif winner == False:
            return -1
        else:
            return 0  # maybe do a negative for a loss

class MCTS:
    def search(self, root_state: GameBoard, budget):
        # # Constraints
        # timeStart = datetime.time
        # timeout = timeStart + datetime.timedelta.__add__(timeLimit)

        root_node = Node(root_state)

        for temp in range(budget):  # change budget with time and space constraints
        # while time.time() < timeout:  # time limit
            searchNode = root_node
            state = copy.deepcopy(root_state)  # has to be deepcopy to individually make changes later on

            # Select
            while searchNode.isFullyExpanded() and not state.getWinner()[0]:
                searchNode = searchNode.getBestChild()
                state.updateBoard(searchNode.state.getCurrentPlayer(), searchNode.state.lastMove)

            # Expand
            if not searchNode.isFullyExpanded() and not state.getWinner()[0]:
                unexpandedMoves = [
                    move for move in state.getLegalMoves()
                    if not any(node.state.lastMove == move for node in searchNode.children)
                ]
                move = random.choice(unexpandedMoves)[1]

                state.updateBoard(searchNode.state.getCurrentPlayer(), move)
                state.lastMove = move  # adds the move to the GameBoard of the State
                searchNode = searchNode.addChild(state)

            # Simulate
            result = searchNode.rollout()

            # Back-Propagate
            while searchNode is not None:
                searchNode.update(result)
                searchNode = searchNode.parent

        # returns node with most visits and highest value
        return max(root_node.children, key=lambda searchNode: searchNode.visits).state.lastMove