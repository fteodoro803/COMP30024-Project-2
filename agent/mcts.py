import math
import random

from .gameboard import *

class Node:
    def __init__(self, state: GameBoard, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0

    # updates Visits and Scores for each Node
    def update(self, result):
        self.visits += 1
        self.score += result

    # adds child Nodes to Self
    def addChild(self, childState):
        childNode = Node(childState, self)
        self.children.append(childNode)
        return childNode

    # checks if Node is fully expanded
    def isFullyExpanded(self) -> bool:
        return len(self.children) == len(self.state.getLegalMoves())

    # UCB1 Calculation
    def getBestChild(self):
        choiceWeights = []
        constant = 2

        for child in self.children:
            choiceWeights.append((child.score / child.visits) +
                                 constant * math.sqrt((2 * math.log(self.visits) / child.visits)))

        return self.children[choiceWeights.index(max(choiceWeights))]

    # Simulation of Game from Node
    def playout(self):  # random moves to get to the point\
        currentState = self.state
        isTerminal = currentState.getWinner()[0]
        while not isTerminal:
            possibleMoves = currentState.getLegalMoves()
            choice = random.choice(possibleMoves)
            currentState = choice[0]
            isTerminal = choice[0].getWinner()
        return currentState.getWinner()[2]


class MCTS:
    iterationLimit = 20
    def search(self, root_state: GameBoard):
        rootNode = Node(root_state)

        for temp in range(self.iterationLimit):  # change budget with time and space constraints
            searchNode = rootNode
            state = copy.deepcopy(root_state)

            # Select
            while searchNode.isFullyExpanded() and not state.getWinner()[0]:
                searchNode = searchNode.getBestChild()

                # updates board according to the best child
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

            # Playout
            result = searchNode.playout()

            # Back-Propagate
            while searchNode is not None:
                searchNode.update(result)
                searchNode = searchNode.parent

        # returns node with most visits and highest value
        return max(rootNode.children, key=lambda searchNode: searchNode.visits).state.lastMove


### REFERENCES ###
#   - Code adapted from https://webdocs.cs.ualberta.ca/~hayward/396/jem/mcts.html
#   - Code adapted from https://youtu.be/UXW2yZndl7U