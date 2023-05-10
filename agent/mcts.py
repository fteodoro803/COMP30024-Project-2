import copy
import datetime
import math
import time
import random

from .gameboard import *

class Node:
    def __init__(self, state: GameBoard, parent=None):

        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0  # was wins, maybe change to score?

    def update(self, result):
        self.visits += 1
        self.score += result

    def addChild(self, childState):  # returns a Node but python doesn't let me add it as a typehint
        childNode = Node(childState, self)
        self.children.append(childNode)
        return childNode

    def isFullyExpanded(self) -> bool:
        return len(self.children) == len(self.state.getLegalMoves())

    def getBestChild(self):  # returns a Node but python doesn't let me add it as a typehint  | !!!!! also is kinda weird i think. it doesn't seem to choose THE best option
        choiceWeights = []
        constant = 2

        for child in self.children:
            choiceWeights.append((child.score / child.visits) + constant * math.sqrt((2 * math.log(self.visits) / child.visits)))

        return self.children[choiceWeights.index(max(choiceWeights))]

    def rollout(self):  # random moves to get to the point
        currentState = self.state
        # print(f"CurrentState 1: {currentState}")
        isTerminal = currentState.getWinner()[0]
        # print(f"isTerminal: {isTerminal}")
        while not isTerminal:
            possibleMoves = currentState.getLegalMoves()  # !!! i feel like this could be weird ,or the way it selects the random moves
            # print(possibleMoves)
            choice = random.choice(possibleMoves)
            currentState = choice[0]
            # print(f"CurrentState 2: {currentState}")
            isTerminal = choice[0].getWinner()
        return currentState.getWinner()[2]


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
            while searchNode.isFullyExpanded() and not state.getWinner()[0]:  # this part is never gone through
                searchNode = searchNode.getBestChild()  # UCB1 stuff
                state.updateBoard(searchNode.state.getCurrentPlayer(), searchNode.state.lastMove)  # changes board according to the best child

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